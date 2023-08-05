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
"""
The following includes OpenLLM configuration and excerpt from
[instruct_pipeline.py](https://huggingface.co/databricks/dolly-v2-3b/blob/main/instruct_pipeline.py)
"""
from __future__ import annotations

import openllm


class DollyV2Config(
    openllm.LLMConfig,
    default_timeout=3600000,
    trust_remote_code=True,
    url="https://github.com/databrickslabs/dolly",
):
    """Databricks’ Dolly is an instruction-following large language model trained on the Databricks
    machine learning platform that is licensed for commercial use.

    Based on pythia-12b, Dolly is trained on ~15k instruction/response fine tuning records databricks-dolly-15k
    generated by Databricks employees in capability domains from the InstructGPT paper, including brainstorming,
    classification, closed QA, generation, information extraction, open QA and summarization.

    dolly-v2-12b is not a state-of-the-art model, but does exhibit surprisingly high quality instruction
    following behavior not characteristic of the foundation model on which it is based.

    Refer to [Databricks's Dolly page](https://github.com/databrickslabs/dolly) for more information.
    """

    return_full_text: bool = openllm.LLMConfig.Field(
        False, description="Whether to return the full prompt to the users."
    )
    use_default_prompt_template: bool = False

    class GenerationConfig:
        temperature: float = 0.9
        top_p: float = 0.92
        top_k: int = 0
        max_new_tokens: int = 256


START_DOLLY_V2_COMMAND_DOCSTRING = """\
Run a LLMServer for dolly-v2 model and pretrained.

\b
> See more information about dolly-v2 at [databricks/dolly-v2-3b](https://huggingface.co/databricks/dolly-v2-3b)

\b
## Usage

Currently, dolly-v2 only supports PyTorch. Make sure ``torch`` is available in your system.

\b
Dolly-v2 Runner will use databricks/dolly-v2-3b as the default model. To change any to any other dolly-v2
saved pretrained, or a fine-tune dolly-v2, provide ``OPENLLM_DOLLY_V2_PRETRAINED='databricks/dolly-v2-7b'``
"""

INSTRUCTION_KEY = "### Instruction:"
RESPONSE_KEY = "### Response:"
END_KEY = "### End"
INTRO_BLURB = (
    "Below is an instruction that describes a task. Write a response that appropriately completes the request."
)

# NOTE: This is the prompt that is used for generating responses using an already
# trained model.  It ends with the response key, where the job of the model is to provide
# the completion that follows it (i.e. the response itself).
DEFAULT_PROMPT_TEMPLATE = """{intro}
{instruction_key}
{instruction}
{response_key}
""".format(
    intro=INTRO_BLURB,
    instruction_key=INSTRUCTION_KEY,
    instruction="{instruction}",
    response_key=RESPONSE_KEY,
)
