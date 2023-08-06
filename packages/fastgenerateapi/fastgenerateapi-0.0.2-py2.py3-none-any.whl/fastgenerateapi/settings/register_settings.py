from fastgenerateapi.settings.settings import SettingsModel

settings = SettingsModel()


def register_settings(global_settings: SettingsModel) -> None:
    global settings
    settings = global_settings

    return



