class AudienceNameGetter:
    def __init__(self, config) -> None:
        self.__config = config
        self.__user_friendly_part_length = 8

    def get_user_friendly_export_id(self) -> str:
        user_friendly_part = self.__config["export_id"][: self.__user_friendly_part_length].upper()
        return f"E-{user_friendly_part}"

    def get(self) -> str:
        return f"{self.get_user_friendly_export_id()} {self.__config['export_title']}"
