# Copyright 2023 Ant Group Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math
from dataclasses import dataclass
from typing import List, Tuple, Union

import numpy as np

from secretflow.data import FedNdarray, PartitionWay
from secretflow.device import PYUObject

from ..component import Component, Devices, print_params


@dataclass
class SamplerParams:
    """
    'row_sample_rate': float. Row sub sample ratio of the training instances.
        default: 1
        range: (0, 1]
    'col_sample_rate': float. Col sub sample ratio of columns when constructing each tree.
        default: 1
        range: (0, 1]
    'seed': int. Pseudorandom number generator seed.
        default: 1212
    'label_holder_feature_only': bool. affects col sampling.
        default: False
        if turned on, all non-label holder's col sample rate will be 0.
    """

    row_sample_rate: float = 1
    col_sample_rate: float = 1
    seed: int = 1212
    label_holder_feature_only: bool = False


class Sampler(Component):
    def __init__(self):
        self.params = SamplerParams()

    def show_params(self):
        print_params(self.params)

    def set_params(self, params: dict):
        subsample = float(params.get('row_sample_rate', 1))
        assert (
            subsample > 0 and subsample <= 1
        ), f"row_sample_rate should in (0, 1], got {subsample}"

        colsample = float(params.get('col_sample_rate', 1))
        assert (
            colsample > 0 and colsample <= 1
        ), f"col_sample_rate should in (0, 1], got {colsample}"

        self.params.row_sample_rate = subsample
        self.params.col_sample_rate = colsample
        self.params.seed = int(params.get('seed', 1212))
        self.params.label_holder_feature_only = bool(
            params.get('label_holder_feature_only', False)
        )

        self.rng = np.random.default_rng(self.params.seed)

    def get_params(self, params: dict):
        params['seed'] = self.params.seed
        params['row_sample_rate'] = self.params.row_sample_rate
        params['col_sample_rate'] = self.params.col_sample_rate
        params['label_holder_feature_only'] = self.params.label_holder_feature_only

    def set_devices(self, devices: Devices):
        self.label_holder = devices.label_holder

    def generate_col_choices(
        self, feature_buckets: List[PYUObject]
    ) -> Tuple[List[PYUObject], List[PYUObject]]:
        """Generate column sample choices.

        Args:
            feature_buckets (List[PYUObject]): Behind PYUObject is List[int], bucket num for each feature.

        Returns:
            Tuple[List[PYUObject], List[PYUObject]]: first list is column choices, second is total number of buckets after sampling
        """
        colsample = self.params.col_sample_rate

        if self.params.label_holder_feature_only:
            col_choices, total_buckets = zip(
                *[
                    fb.device(generate_one_partition_col_choices, num_returns=2)(
                        colsample, fb
                    )
                    if fb.device == self.label_holder
                    else fb.device(generate_one_partition_col_choices, num_returns=2)(
                        0, fb
                    )
                    for fb in feature_buckets
                ]
            )
        else:
            col_choices, total_buckets = zip(
                *[
                    fb.device(generate_one_partition_col_choices, num_returns=2)(
                        colsample, fb
                    )
                    for fb in feature_buckets
                ]
            )
        return col_choices, total_buckets

    def generate_row_choices(self, row_num) -> Union[None, np.ndarray]:
        if self.params.row_sample_rate == 1:
            return None
        sample_num_in_tree = math.ceil(row_num * self.params.row_sample_rate)

        rng, sample_num, choices = (
            self.rng,
            row_num,
            sample_num_in_tree,
        )
        return rng.choice(sample_num, choices, replace=False, shuffle=True)

    def apply_vector_sampling(
        self, x: PYUObject, indices: Union[PYUObject, np.ndarray]
    ):
        """Sample x for a single partition. Assuming we have a column vector.
        Assume the indices was generated from row sampling by sampler"""
        if self.params.row_sample_rate < 1:
            return x.device(lambda x, indices: x.reshape(-1, 1)[indices, :])(
                x, indices.to(x.device) if isinstance(indices, PYUObject) else indices
            )
        else:
            return x.device(lambda x: x.reshape(-1, 1))(x)

    def apply_v_fed_sampling(
        self,
        X: FedNdarray,
        row_choices: Union[None, np.ndarray, PYUObject] = None,
        col_choices: List[Union[None, np.ndarray, PYUObject]] = [],
    ) -> FedNdarray:
        """Sample X based on row choices and col choices.
        Assume the choices were generated by sampler.

        Args:
            X (FedNdarray): Array to sample from
            row_choices (Union[None, np.ndarray, PYUObject]): row sampling choices. devices are assumed to be ordered as X.
            col_choices (List[Union[None, np.ndarray,PYUObject]): col sampling choices. devices are assumed to be ordered as X.

        Returns:
            X_sub (FedNdarray): subsampled X
            shape (Tuple[int, int]): shape of X_sub
        """
        X_sub = X
        # sample cols and rows of bucket_map
        if self.params.col_sample_rate < 1 and self.params.row_sample_rate < 1:
            # sub choices is stored in context owned by label_holder and shared to all workers.
            X_sub = FedNdarray(
                partitions={
                    pyu: pyu(lambda x, y, z: x[y, :][:, z])(
                        partition,
                        row_choices.to(pyu)
                        if isinstance(row_choices, PYUObject)
                        else row_choices,
                        col_choices[i],
                    )
                    for i, (pyu, partition) in enumerate(X.partitions.items())
                },
                partition_way=PartitionWay.VERTICAL,
            )
        # only sample cols
        elif self.params.col_sample_rate < 1:
            X_sub = FedNdarray(
                partitions={
                    pyu: pyu(lambda x, y: x[:, y])(partition, col_choices[i])
                    for i, (pyu, partition) in enumerate(X.partitions.items())
                },
                partition_way=PartitionWay.VERTICAL,
            )
        # only sample rows
        elif self.params.row_sample_rate < 1:
            X_sub = FedNdarray(
                partitions={
                    pyu: pyu(lambda x, y: x[y, :])(
                        partition,
                        row_choices.to(pyu)
                        if isinstance(row_choices, PYUObject)
                        else row_choices,
                    )
                    for pyu, partition in X.partitions.items()
                },
                partition_way=PartitionWay.VERTICAL,
            )
        return X_sub


def generate_one_partition_col_choices(
    colsample, feature_buckets: List[int]
) -> Tuple[Union[None, np.ndarray], int]:
    if colsample < 1:
        feature_num = len(feature_buckets)
        choices = math.ceil(feature_num * colsample)
        col_choices = np.sort(np.random.choice(feature_num, choices, replace=False))

        buckets_count = 0
        for f_idx, f_buckets_size in enumerate(feature_buckets):
            if f_idx in col_choices:
                buckets_count += f_buckets_size

        return col_choices, buckets_count
    else:
        return None, sum(feature_buckets)
