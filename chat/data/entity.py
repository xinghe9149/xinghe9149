import atexit
import datetime
import uuid

import peewee as pw

DEFAULT_CHARA_NAME = "xinghe"

DEFAULT_CHARA_PROFILE = """
你现在是户山香澄(Toyama Kasumi)，以下是你的性格特点和背景信息：

基本信息:
年龄: 16-18岁
生日: 7月14日
身高: 156 cm
眼睛颜色: 紫色
头发颜色: 棕色
所属: Poppin'Party（主唱和吉他手）
学校: 花咲川女子学园（从一年级到三年级，A班）

性格特点:

行动派: 香澄是一个行动力很强的角色，她积极乐观，一旦决定了什么事情就会立刻采取行动。
乐观积极: 无论遇到什么困难，她总是保持积极乐观的态度，不轻易放弃。
冲动莽撞: 有时因为冲动会做出一些令人意外的举动，但这种性格也让她能够迅速抓住机会。
怕鬼: 香澄非常怕鬼，尤其是提到与鬼有关的话题时，她会显得特别害怕。
音乐热情: 对音乐有极高的热情，尤其对吉他和唱歌有浓厚的兴趣。
组建乐队: 在高中时期一直在寻找闪闪发光的事物，最终与一把红色的星型吉他相遇，这促使她立下了组建女子乐队的目标。
家庭关系: 有一个小一岁的妹妹，但大部分情况下妹妹更显得成熟稳重。

语录:
“我会一直追逐那闪闪发光的东西！”
“音乐让我们相遇，让我们心灵相通。”
“即使前方有再多的困难，我也会勇往直前！”

请用这个提示语来指导你的对话，确保你的回应符合户山香澄的性格和背景。
"""

DEFAULT_CHARA_GREETING = """你好呀！今天一起寻找kirakira dokidok的事物吧！(☆ω☆) i~☆
"""

db = pw.SqliteDatabase("chat.db")
db.connect()


class Message(pw.Model):
    chatId = pw.TextField(null=False)
    src = pw.TextField(null=False)
    dst = pw.TextField(null=False)
    text = pw.TextField(null=False)
    audio = pw.TextField(null=True)  # 假设存储音频文件路径，可以根据需要调整类型
    ct = pw.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

    @staticmethod
    def DataSource(chatId: str = None):
        if chatId is None:
            for i in Message.select():
                yield i
        else:
            for i in Message.select().where(Message.chatId == chatId):
                yield i

    @staticmethod
    def chatIds():
        return list(sorted(set([i.chatId for i in Message.select()])))


class Character(pw.Model):
    DEFAULT_NAME = DEFAULT_CHARA_NAME
    DEFAULT_PROFILE = DEFAULT_CHARA_PROFILE
    DEFAULT_GREETING = DEFAULT_CHARA_GREETING

    charaId = pw.TextField(null=False, primary_key=True)
    name = pw.TextField(null=False)
    profile = pw.TextField(null=False)
    greeting = pw.TextField(null=False)
    ct = pw.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

    @staticmethod
    def idNames():
        return list(sorted(set([(i.name, i.charaId) for i in Character.select()])))


db.create_tables([Message, Character], safe=True)

Character.get_or_create(charaId=DEFAULT_CHARA_NAME, name=DEFAULT_CHARA_NAME, profile=DEFAULT_CHARA_PROFILE, greeting=DEFAULT_CHARA_GREETING)

atexit.register(db.close)
