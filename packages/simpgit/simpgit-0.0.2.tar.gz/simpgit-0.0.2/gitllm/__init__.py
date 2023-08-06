from gitllm.git import GitLLM
from enum import Enum


class ServiceEnum(str, Enum):
    SAVE = "save"
    SHARE = "share"
