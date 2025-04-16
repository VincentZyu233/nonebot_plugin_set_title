import os

from nonebot import require

require("nonebot_plugin_alconna")

from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from arclet.alconna import Alconna, Option, Args
from nonebot_plugin_alconna import Alconna, on_alconna, Match, UniMessage, At, CommandMeta, Image
from nonebot import on_command


usage_string = "\tqst=\"qwq_set_special_title\" \n\t\t用法: qst <头衔:str> [用户:At]" 

# 第一种用法：qst <touxian:str> (修改自己)
qst_set_self = on_alconna(
    Alconna(
        [""],
        "qst",
        Args["touxian", str],
        meta=CommandMeta(
            description="直接设置自己的群头衔",
        ),
    )
)

@qst_set_self.handle()
async def qst_set_self_handle(touxian: Match[str], bot: Bot, event: Event):
    try:
        await qst_set_self.send("set self")
        await bot.set_group_special_title(
            group_id=event.group_id,
            user_id=event.get_user_id(),
            special_title=touxian.result,
            duration=1
        )
    except Exception as e:
        await qst_set_self.send(f"qst failed (self). \n\te = {e}")


# 第二种用法：qst <touxian:str> <user:at> (修改指定用户)
qst_set_other = on_alconna(
    Alconna(
        [""],
        "qst",
        Args["touxian", str]["target", At],
        meta=CommandMeta(
            description="设置指定用户的群头衔",
            usage=usage_string,
            example="\tqs 这是一个头衔qwq @VincentZyu",
            author="VincentZyu",
            fuzzy_match=False,
            raise_exception=True
        ),
    )
)

@qst_set_other.handle()
async def qst_set_other_handle(touxian: Match[str], target: Match[At], bot: Bot, event: Event):
    target_qqid = target.result.target
    try:
        await qst_set_self.send("set other")
        await bot.set_group_special_title(
            group_id=event.group_id,
            user_id=target_qqid,
            special_title=touxian.result,
            duration=1
        )
    except Exception as e:
        await qst_set_other.send(f"qst failed (other). \n\te = {e}")



qst_help_command = on_alconna(
    Alconna(
        "qst_help"
    )
)

@qst_help_command.handle()
async def handle_qst_help():
    print("on_command: qst_help")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(current_dir, "code.png")
    await qst_help_command.send(
        MessageSegment.text("source code↓") +
        MessageSegment.image(img_path)
    )