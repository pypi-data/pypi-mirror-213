from enum import Enum


class LabelEntryType(str, Enum):
    LABEL = "label"
    ALIAS = "alias"
    CATEGORY = "category"
    PARENT = "parent"
    MODERATION = "moderation"
