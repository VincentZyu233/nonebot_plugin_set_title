from nonebot import require

require("nonebot_plugin_alconna")

from nonebot.adapters.onebot.v11 import Bot, Event
from arclet.alconna import Alconna, Option, Args
from nonebot_plugin_alconna import Alconna, on_alconna, Match, UniMessage, At

qst_command = on_alconna(
    Alconna(
        [""], 
        "qst", 
        Args["touxian?", str]["target?", At]
    )
)


@qst_command.assign(
    "touxian"
)
async def qst_handle(
    touxian: Match[str], 
    target: Match[At],
    bot: Bot, 
    event: Event
):    
    if not touxian.available:
        return
    
    # target_qqid = target.result.target if target.available else event.get_user_id()
    target_qqid = event.get_user_id()
    if target.available:
        target_qqid = target.result.target
    
    qst_command.set_path_arg("touxian", touxian.result)
    qst_command.set_path_arg("target_qqid", target_qqid)
    
    # await qst_command.send(f"[debug] \n\t touxian = {touxian.result} \n\t target = {target_qqid}")

    try:
        # await qst_command.send("[debug] 111")
        await bot.set_group_special_title(
            group_id = event.group_id,
            user_id = target_qqid,
            special_title = touxian.result,
            duration = 1
        )
    except Exception as e:
        await qst_command.send(f"qst failed. \n\te = {e}")


@qst_command.got_path(
    "touxian", 
    prompt=UniMessage.template("{:At(user, $event.get_user_id())} 请输入头衔"),
)
async def qst_got(
    touxian: str,
    bot: Bot, 
    event: Event
):
    # assert touxian
    if qst_command.get_path_arg("touxian", default=None) is not None:
        return

    try:
        # await qst_command.send("[debug] 222")
        await bot.set_group_special_title(
            group_id = event.group_id,
            user_id = event.get_user_id(),
            # special_title = "foooooooooooooooooooooooqwerty",
            special_title = touxian,
            duration = 1
        )
    except Exception as e:
        await qst_command.send(f"qst failed. \n\te = {e}")


    