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


from torch.utils.data import Dataset


class VerticallyAugmentedDataset(Dataset):
    def __init__(
        self,
        first_party_dataset: Dataset,
    ):
        """
        A wrapper for a Dataset that provides first-party data. Adds additional
        information to the batch returned by the internal dataset, which
        provides necessary context for `ArcusVerticalDataLoaderWrapper` to
        fetch the relevant external data.

        Args:
            first_party_dataset: The first-party dataset to wrap.

        __getitem__ adds the index of the internal dataset to the current
            batch.
        """

        if isinstance(first_party_dataset, VerticallyAugmentedDataset):
            assert False, "VerticalDatasetWrapper cannot be nested."

        self.first_party_dataset = first_party_dataset

        super().__init__()

    # Keep all existing methods of self.first_party_dataset except those
    # overriden here.
    def __getattr__(self, attr):
        if hasattr(self.first_party_dataset, attr):
            return getattr(self.first_party_dataset, attr)

        raise AttributeError(f"Attribute {attr} not found.")

    def __getitem__(self, index: int):
        internal_batch = self.first_party_dataset[index]
        return internal_batch, index

    def __len__(self):
        return len(self.first_party_dataset)
