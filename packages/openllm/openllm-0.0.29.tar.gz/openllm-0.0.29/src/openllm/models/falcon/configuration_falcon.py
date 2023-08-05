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

import openllm


class FalconConfig(
    openllm.LLMConfig,
    name_type="lowercase",
    trust_remote_code=True,
    requires_gpu=True,
    default_timeout=3600000,
    url="https://falconllm.tii.ae/",
    requirements=["einops", "xformers", "safetensors"],
):
    """Falcon-7B is a 7B parameters causal decoder-only model built by
    TII and trained on 1,500B tokens of [RefinedWeb](https://huggingface.co/datasets/tiiuae/falcon-refinedweb)
    enhanced with curated corpora. It is made available under the TII Falcon LLM License.

    Refer to [Falcon's HuggingFace page](https://huggingface.co/tiiuae/falcon-7b) for more information.
    """

    use_default_prompt_template: bool = False

    class GenerationConfig:
        max_new_tokens: int = 200
        top_k: int = 10
        num_return_sequences: int = 1
        eos_token_id: int = 11  # NOTE: Get from tokenizer.eos_token_id


START_FALCON_COMMAND_DOCSTRING = """\
Run a LLMServer for FalconLM model and pretrained.

\b
> See more information about falcon at [tiiuae/falcon-7b](https://huggingface.co/tiiuae/falcon-7b)

\b
## Usage

Currently, FalconLM only supports PyTorch. Make sure ``torch`` is available in your system.

\b
FalconLM Runner will use tiiuae/falcon-7b as the default model. To change any to any other FalconLM
saved pretrained, or a fine-tune FalconLM, provide ``OPENLLM_FALCON_PRETRAINED='tiiuae/falcon-7b-instruct'``
"""

DEFAULT_PROMPT_TEMPLATE = """{context}
{user_name}: {instruction}
{agent}:
"""
