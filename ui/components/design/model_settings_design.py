from config.configuration import Configuration
from ui.components.design.base_designs import ScrollDesign
from ui.components.design.icon_design import IconDesign
from ui.components.motion_editor import MotionEditor
from ui.components.setting_cards import *


class ModelSettingsDesign(ScrollDesign, IconDesign):

    def __init__(self, config: Configuration):
        super().__init__()
        self.resource_dir = config.resource_dir.value
        self.card_changeModel = ChangeModelSettingCard(config.model_name,
                                                       config.model_list,
                                                       FluentIcon.PEOPLE,
                                                       "模型")

        expandable = ExpandGroupSettingCard(FluentIcon.PLAY, "动作组")
        self.motionEditor = MotionEditor(config.model3Json)
        self.btn_save = PrimaryPushButton("保存")
        expandable.addGroupWidget(self.motionEditor)
        expandable.addGroupWidget(self.btn_save)

        self.vBoxLayout.addWidget(self.card_changeModel)
        self.vBoxLayout.addWidget(expandable)
        self.vBoxLayout.addStretch(1)
