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


from typing import Dict, List, Optional, Union

import torch

from arcus.api_client import APIClient, ArcusResponse
from arcus.model.shared.config import Config
from arcus.model.shared.data import (
    ExternalFeatureType,
    ProjectCandidateMetadata,
)
from arcus.model.torch.data.data_types import SplitType
from arcus.model.torch.data.tensor import ExternalDataTensor


class VerticalExternalDataClient:
    """
    Client for fetching external data from Arcus to vertically (i.e.
    feature-wise) augment first-party data passed.

    Args:
        project_candidate_metadata: ProjectCandidateMetadata object
            containing information about the project and candidate.
    """

    def __init__(
        self,
        project_candidate_metadata: ProjectCandidateMetadata,
    ):
        self.external_data: Dict[SplitType, ExternalDataTensor] = {}
        self.project_candidate_metadata = project_candidate_metadata

        self.external_data_dim: int = project_candidate_metadata.get_data_dim()
        self.feature_type: ExternalFeatureType = (
            project_candidate_metadata.get_feature_type()
        )
        self.candidate_id: str = project_candidate_metadata.get_candidate_id()

        self.config: Config = project_candidate_metadata.get_config()
        self.api_client = APIClient(self.config)

    def _fetch_external_data(
        self,
        loader_split_type: SplitType,
    ) -> ExternalDataTensor:
        response: ArcusResponse = self.api_client.request(
            "GET",
            "model/data/features",
            params={
                "project_id": self.config.get_project_id(),
                "candidate_id": self.candidate_id,
                "loader_split_type": loader_split_type.value,
            },
        )

        if not response.status_ok:
            raise Exception("Unable to fetch external data from Arcus.")

        external_data_tensor: torch.Tensor = torch.tensor(
            response.data["data"], dtype=torch.float32
        )

        assert (
            len(external_data_tensor.shape) == 2
        ), "External data must be 2-dimensional."

        assert self.external_data_dim == external_data_tensor.shape[1], (
            "External data must have the same number of "
            + "dimensions as the model expects. "
            + f"Expected {self.external_data_dim},"
            + f" got {external_data_tensor.shape[1]}."
        )
        return ExternalDataTensor(external_data_tensor, self.feature_type)

    def fetch_batch(
        self,
        index: Union[int, List[int], slice, torch.Tensor],
        loader_split_type: Optional[SplitType] = SplitType.TRAIN,
    ) -> ExternalDataTensor:
        """
        Fetch a batch of external data from Arcus.
        Args:
            index: Index or indices of the batch to fetch.
            loader_split_type: The split type of the data loader from which
                the batch is being fetched. This is used to determine which
                external data to fetch from Arcus.
        Returns:
            A batch of external data, as an ExternalDataTensor.
        """
        if loader_split_type not in self.external_data:
            external_data = self._fetch_external_data(loader_split_type)
            self.external_data[loader_split_type] = external_data

        return self.external_data[loader_split_type][index]

    def __len__(self):
        return sum([len(v) for v in self.external_data.values()])

    def __repr__(self):
        return (
            f"Arcus {self.feature_type} data with "
            + f"{self.external_data_dim} dimensions."
        )

    def __str__(self) -> str:
        return self.__repr__()

    def is_raw(self) -> bool:
        return self.feature_type is ExternalFeatureType.RAW

    def is_embedding(self) -> bool:
        return self.feature_type is ExternalFeatureType.EMBEDDING

    @property
    def shape(self) -> torch.Size:
        return torch.Size([len(self), self.external_data_dim])

    def get_external_data_dim(self) -> int:
        return self.external_data_dim

    def get_feature_type(self) -> ExternalFeatureType:
        return self.feature_type
