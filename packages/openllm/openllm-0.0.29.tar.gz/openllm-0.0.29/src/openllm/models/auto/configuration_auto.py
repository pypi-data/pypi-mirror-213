# Copyright 2023 BentoML Team. All rights reserved.
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

from __future__ import annotations

import types
import typing as t
from collections import OrderedDict

import inflection

import openllm

if t.TYPE_CHECKING:
    ConfigOrderedDict = OrderedDict[str, openllm.LLMConfig]
else:
    ConfigOrderedDict = OrderedDict

# NOTE: This is the entrypoint when adding new model config
CONFIG_MAPPING_NAMES = OrderedDict(
    [
        ("flan_t5", "FlanT5Config"),
        ("dolly_v2", "DollyV2Config"),
        ("chatglm", "ChatGLMConfig"),
        ("starcoder", "StarCoderConfig"),
        ("falcon", "FalconConfig"),
        ("stablelm", "StableLMConfig"),
    ]
)


class _LazyConfigMapping(ConfigOrderedDict):
    def __init__(self, mapping: OrderedDict[str, str]):
        self._mapping = mapping
        self._extra_content: dict[str, t.Any] = {}
        self._modules: dict[str, types.ModuleType] = {}

    def __getitem__(self, key: str):
        if key in self._extra_content:
            return self._extra_content[key]
        if key not in self._mapping:
            raise KeyError(key)
        value = self._mapping[key]
        module_name = inflection.underscore(key)
        if module_name not in self._modules:
            self._modules[module_name] = openllm.utils.ModelEnv(module_name).module
        if hasattr(self._modules[module_name], value):
            return getattr(self._modules[module_name], value)

        # Some of the mappings have entries model_type -> config of another model type. In that case we try to grab the
        # object at the top level.
        return getattr(openllm, value)

    def keys(self):
        return list(self._mapping.keys()) + list(self._extra_content.keys())

    def values(self):
        return [self[k] for k in self._mapping.keys()] + list(self._extra_content.values())

    def items(self):
        return [(k, self[k]) for k in self._mapping.keys()] + list(self._extra_content.items())

    def __iter__(self):
        return iter(list(self._mapping.keys()) + list(self._extra_content.keys()))

    def __contains__(self, item: t.Any):
        return item in self._mapping or item in self._extra_content

    def register(self, key: str, value: t.Any):
        """
        Register a new configuration in this mapping.
        """
        if key in self._mapping.keys():
            raise ValueError(f"'{key}' is already used by a OpenLLM config, pick another name.")
        self._extra_content[key] = value


CONFIG_MAPPING = _LazyConfigMapping(CONFIG_MAPPING_NAMES)


class AutoConfig:
    def __init__(self, *_: t.Any, **__: t.Any):
        raise EnvironmentError("Cannot instantiate Config. Please use `Config.for_model(model_name)` instead.")

    @classmethod
    def for_model(cls, model_name: str, **attrs: t.Any) -> openllm.LLMConfig:
        model_name = inflection.underscore(model_name)
        if model_name in CONFIG_MAPPING:
            return CONFIG_MAPPING[model_name].model_construct_env(**attrs)
        raise ValueError(
            f"Unrecognized configuration class for {model_name}. "
            f"Model name should be one of {', '.join(CONFIG_MAPPING.keys())}."
        )
