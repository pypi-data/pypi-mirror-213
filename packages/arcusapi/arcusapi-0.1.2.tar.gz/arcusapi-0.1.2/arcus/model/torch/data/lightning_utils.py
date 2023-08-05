# Copyright [2023] [Arcus Inc.]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from typing import Callable, Dict, Optional, Sequence, TypedDict, Union

import pytorch_lightning as pl
from pytorch_lightning.utilities.exceptions import MisconfigurationException
from pytorch_lightning.utilities.types import (
    EVAL_DATALOADERS,
    TRAIN_DATALOADERS,
)
from torch.utils.data import DataLoader

from arcus.model.torch.data.data_client import VerticalExternalDataClient
from arcus.model.torch.data.data_loader import wrap_dataloader_vertical
from arcus.model.torch.data.data_types import DATALOADER_TYPES, SplitType

__all__ = [
    "TrainerDataLoaders",
    "construct_lightning_module_loaders_dict",
    "wrap_lightningmodule_loaders_vertical",
    "wrap_dataloaders_vertical",
    "wrap_module_and_trainer_dataloaders_vertical",
]


class TrainerDataLoaders(TypedDict):
    """
    The dataloaders that can be passed to a Trainer.
    """

    train_dataloaders: Optional[
        Union[TRAIN_DATALOADERS, pl.LightningDataModule]
    ]
    val_dataloaders: Optional[Union[EVAL_DATALOADERS, pl.LightningDataModule]]
    test_dataloaders: Optional[Union[EVAL_DATALOADERS, pl.LightningDataModule]]
    predict_dataloaders: Optional[
        Union[EVAL_DATALOADERS, pl.LightningDataModule]
    ]


def construct_lightning_module_loaders_dict(
    module: Union[pl.LightningModule, pl.LightningDataModule],
) -> Dict[SplitType, Callable[[], DataLoader]]:
    """
    Returns a dictionary of the LightningModule's dataloaders that are
    defined. The keys are the SplitType of each dataloader.
    """
    loaders = {}
    for loader_name in SplitType:
        loader = getattr(
            module, f"{loader_name.value.lower()}_dataloader", None
        )
        if loader is not None:
            loaders[loader_name] = loader
    return loaders


def _loader_factory(
    loader_fn: Callable[[], DataLoader]
) -> Callable[[], DataLoader]:
    """
    Returns a factory function that returns the loader_fn when called.
    """

    def factory() -> Callable[[], DataLoader]:
        return loader_fn

    return factory


def wrap_lightningmodule_loaders_vertical(
    module: Union[pl.LightningModule, pl.LightningDataModule],
    external_data_client: Optional[VerticalExternalDataClient] = None,
    join_tensor_index: int = 0,
) -> None:
    """
    Wraps the LightningModule's dataloaders with a
    VerticallyAugmentedDataLoader which fetches external data from the
    provided VerticalExternalDataClient.

    Args:
        module: The LightningModule to wrap.
        external_data_client: The VerticalExternalDataClient to use to
            fetch external data.
        join_tensor_index: The index of the tensor in the dataloader's
            dataset that should be used to join the external data.
    Returns:
        None
    """
    if external_data_client is None:
        return

    loader_fns = construct_lightning_module_loaders_dict(module)

    for loader_name, loader in loader_fns.items():
        try:
            wrapped_loader_fn = wrap_dataloader_vertical(
                loader(),
                external_data_client,
                loader_name,
                join_tensor_index=join_tensor_index,
            )

            setattr(
                module,
                f"{loader_name.value.lower()}_dataloader",
                _loader_factory(wrapped_loader_fn),
            )
        except MisconfigurationException:
            # in the case that the dataloader is not yet initialized, we
            # cannot wrap it. In this case, we just continue.
            continue


def wrap_dataloaders_vertical(
    dataloaders: Union[TRAIN_DATALOADERS, EVAL_DATALOADERS],
    external_data_client: Optional[VerticalExternalDataClient] = None,
    loader_split_type: Optional[SplitType] = None,
    join_tensor_index: int = 0,
) -> Union[TRAIN_DATALOADERS, EVAL_DATALOADERS]:
    """
    Wraps the dataloaders with a VerticallyAugmentedDataLoader which fetches
    external data from the provided VerticalExternalDataClient. If the
    dataloaders are a sequence or dictionary, this function will recursively
    wrap the dataloaders.

    Args:
        dataloaders: The dataloaders to wrap.
        external_data_client: The VerticalExternalDataClient to use to
            fetch external data.
        loader_split_type: The SplitType of the dataloader.
        join_tensor_index: The index of the tensor in the dataloader's
            dataset that should be used to join the external data.
    Returns:
        The wrapped dataloaders.
    """

    if isinstance(dataloaders, DataLoader):
        return wrap_dataloader_vertical(
            dataloaders,
            external_data_client,
            loader_split_type,
            join_tensor_index=join_tensor_index,
        )
    elif isinstance(dataloaders, Sequence):
        return [
            wrap_dataloaders_vertical(
                dls, external_data_client, loader_split_type, join_tensor_index
            )
            for dls in dataloaders
        ]
    elif isinstance(dataloaders, Dict):
        return {
            k: wrap_dataloaders_vertical(
                dls, external_data_client, loader_split_type, join_tensor_index
            )
            for k, dls in dataloaders.items()
        }
    else:
        raise ValueError(f"Unknown dataloaders type: {type(dataloaders)}")


def wrap_module_and_trainer_dataloaders_vertical(
    model: pl.LightningModule,
    dataloaders: TrainerDataLoaders,
    datamodule: Optional[pl.LightningDataModule] = None,
    external_data_client: Optional[VerticalExternalDataClient] = None,
    join_tensor_index: int = 0,
) -> TrainerDataLoaders:
    """
    Wraps a given LightningModule's data loaders and provided dataloaders
    to a Trainer with VerticallyAugmentedDataLoaders which fetch external
    using the provided VerticalExternalDataClient.

    Args:
        model: The LightningModule to wrap.
        dataloaders: The dataloaders provided to the Trainer.
        datamodule: The LightningDataModule provided to the Trainer.
        external_data_client: The VerticalExternalDataClient to use to
            fetch external data.
        join_tensor_index: The index of the tensor in the dataloader's
            dataset that should be used to join the external data.
    Returns:
        The wrapped version of the Trainer's dataloaders.
    """
    return_dataloaders = TrainerDataLoaders()
    if external_data_client is None:
        return dataloaders

    wrap_lightningmodule_loaders_vertical(
        model, external_data_client, join_tensor_index
    )
    if datamodule is not None:
        wrap_lightningmodule_loaders_vertical(
            datamodule, external_data_client, join_tensor_index
        )

    for loader_name, loader in dataloaders.items():
        if loader is None:
            continue
        if isinstance(loader, pl.LightningDataModule):
            wrap_lightningmodule_loaders_vertical(
                loader,
                external_data_client,
                join_tensor_index,
            )
            return_dataloaders[loader_name] = loader
        else:
            return_dataloaders[loader_name] = wrap_dataloaders_vertical(
                loader,
                external_data_client,
                DATALOADER_TYPES[loader_name],
                join_tensor_index,
            )

    return return_dataloaders
