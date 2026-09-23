"""Per-language data for the life behavior reference plugin."""

from . import grc, ja, la, zh

_MODULES = {"zh": zh, "la": la, "grc": grc, "ja": ja}
BEHAVIORS = {code: module.BEHAVIORS for code, module in _MODULES.items()}
# 三种旧译文与中文原始十条按相同顺序维护，用于回溯其中文分类。
CANONICAL_ACTIONS = {
    code: dict(zip(behaviors, BEHAVIORS["zh"]))
    for code, behaviors in BEHAVIORS.items()
}
DEPT = {
    key: {code: module.DEPT[key] for code, module in _MODULES.items()}
    for key in zh.DEPT
}
HELP_COMMANDS = {code: module.HELP_COMMAND for code, module in _MODULES.items()}
HELP_TEXT = {code: module.HELP_TEXT for code, module in _MODULES.items()}
ACADEMIC_CLASSIFICATION_VALUES = {
    code: module.ACADEMIC_CLASSIFICATION_VALUES for code, module in _MODULES.items()
}
ACADEMIC_PHASE_LABELS = {
    code: module.ACADEMIC_PHASE_LABELS for code, module in _MODULES.items()
}
AUTHOR_LABELS = {code: module.AUTHOR_LABEL for code, module in _MODULES.items()}
HELP_KEYWORD = zh.HELP_KEYWORD
CATEGORY_TREE = zh.CATEGORY_TREE
