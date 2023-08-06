# flake8: noqa
# -*- coding: utf-8 -*-
# Copyright (C) 2020 Unbabel
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .regression_metric_multi_ref import RegressionMetricMultiReference
from .base import CometModel

import os
import yaml

str2model = {
    "regression_metric_multi_ref": RegressionMetricMultiReference,
}



def load_from_checkpoint(checkpoint_path: str) -> CometModel:
    """Loads models from a checkpoint path.
    :param checkpoint_path: Path to a model checkpoint.

    :return: Returns a COMET model.
    """
    if not os.path.exists(checkpoint_path):
        raise Exception(f"Invalid checkpoint path: {checkpoint_path}")

    hparams_file = "/".join(checkpoint_path.split("/")[:-2] + ["hparams.yaml"])
    if os.path.exists(hparams_file):
        with open(hparams_file) as yaml_file:
            hparams = yaml.load(yaml_file.read(), Loader=yaml.FullLoader)
        model_class = str2model[hparams["class_identifier"]]
        model = model_class.load_from_checkpoint(checkpoint_path, **hparams)
        return model
    else:
        raise Exception("hparams.yaml file is missing!")
