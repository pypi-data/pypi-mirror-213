# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Lora params for roberta family models"""

from .lora_base import BaseLora, LoraBlockConstants
from typing import Dict, Any


class LoraRoberta(BaseLora):
    """Class for defining Lora Params for roberta_base"""

    # TODO Warp the lora_r, alpha and dropout into a dataclass
    def __init__(self, lora_r, lora_alpha, lora_dropout, merge_weights):
        """initializing lora params"""
        super().__init__(lora_r, lora_alpha, lora_dropout, merge_weights)

    def get_lora_blocks_meta_data(self) -> Dict[str, Any]:
        """lora block meta data"""
        return {
            "attention.self": {
                LoraBlockConstants.LayersToModify: ["query", "value"],
                LoraBlockConstants.LoraLayer: "Linear"
            }
        }
