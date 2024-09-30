import uuid

from qfluentwidgets import ConfigItem, QConfig, RangeConfigItem, RangeValidator, BoolValidator

from app import settings, define
from core.model3json import Model3Json


class Configuration(QConfig):
    model_list: list = list()
    model3Json: Model3Json = Model3Json()

    model_name: ConfigItem = ConfigItem(
        "model",
        "name",
        "Hiyori" if settings.LIVE2D_VERSION == define.Live2DVersion.V3 else "kasumi2")
    resource_dir: ConfigItem = ConfigItem(
        "model",
        "resource_dir",
        "Resources/v3" if settings.LIVE2D_VERSION == define.Live2DVersion.V3 else "Resources/v2")
    motion_interval: RangeConfigItem = RangeConfigItem("model", "motion_interval", 10, RangeValidator(5, 86400))
    auto_repair: ConfigItem = ConfigItem("model", "auto_repair", False, BoolValidator())
    drawX: RangeConfigItem = RangeConfigItem("model", "drawX", 0.0, RangeValidator(-2.0, 2.0))
    drawY: RangeConfigItem = RangeConfigItem("model", "drawY", 0.0, RangeValidator(-2.0, 2.0))
    lip_sync: RangeConfigItem = RangeConfigItem("model", "lip_sync", 1.0, RangeValidator(0.01, 1000.0))
    scale: RangeConfigItem = RangeConfigItem("model", "scale", 1.0, RangeValidator(0.01, 1000.0))

    click_transparent: ConfigItem = ConfigItem("mouse", "click_transparent", True, BoolValidator())
    enable: ConfigItem = ConfigItem("mouse", "enable", True, BoolValidator())
    track_enable: ConfigItem = ConfigItem("mouse", "eye_tracking", True, BoolValidator())

    width: RangeConfigItem = RangeConfigItem("scene", "width", 400, RangeValidator(1, 10000))
    height: RangeConfigItem = RangeConfigItem("scene", "height", 500, RangeValidator(1, 10000))
    stay_on_top: ConfigItem = ConfigItem("scene", "stay_on_top", False, BoolValidator())
    visible: ConfigItem = ConfigItem("scene", "visible", True, BoolValidator())
    fps: RangeConfigItem = RangeConfigItem("scene", "fps", 30, RangeValidator(1, 120))
    lastX: RangeConfigItem = RangeConfigItem("scene", "lastX", 0, RangeValidator(0, 10000))
    lastY: RangeConfigItem = RangeConfigItem("scene", "lastY", 0, RangeValidator(0, 10000))

    icon_path: ConfigItem = ConfigItem("systray", "icon", "Resources/icon.png")

    volume: RangeConfigItem = RangeConfigItem("audio", "volume", 100, RangeValidator(0, 100))

    # chat api
    chatServer: ConfigItem = ConfigItem("server", "server", "")
    textPath: ConfigItem = ConfigItem("server", "textPath", "")
    voicePath: ConfigItem = ConfigItem("server", "voicePath", "")

    user: ConfigItem = ConfigItem("chat", "user", default="user")
    charaId: ConfigItem = ConfigItem("chat", "charaId", default="toyama kasumi")
    chatId: ConfigItem = ConfigItem("chat", "chatId", default=str(uuid.uuid4()))
