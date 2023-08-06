from typing import List


class SFMCFieldNameFixer:
    def __init__(self):
        self.__field_name_max_length = 128

    def fix_name(self, field_name: str) -> str:
        return field_name[: self.__field_name_max_length]

    def fix_names(self, field_names: List[str]) -> List[str]:
        return [self.fix_name(field_name) for field_name in field_names]
