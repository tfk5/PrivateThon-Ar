"""
idea from lynda and rose bot
made by @klanr
"""
from telethon.errors import BadRequestError
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

from ..utils import errors_handler
from . import BOTLOG, BOTLOG_CHATID, extract_time, get_user_from_event

# =================== CONSTANT ===================
NO_ADMIN = "- Error, You not admin "
NO_PERM = NO_ADMIN


@bot.on(admin_cmd(pattern=r"tmute(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"tmute(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def tmuter(catty):
    chat = await catty.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    # If not admin and not creator, return
    if not admin and not creator:
        await edit_or_reply(catty, NO_ADMIN)
        return
    catevent = await edit_or_reply(catty, "جـاري الكـتم المؤقت ..")
    user, reason = await get_user_from_event(catty, catevent)
    if not user:
        return
    if reason:
        reason = reason.split(" ", 1)
        hmm = len(reason)
        cattime = reason[0]
        reason = reason[1] if hmm == 2 else None
    else:
        await catevent.edit("- Error, You must write date like 3h")
        return
    self_user = await catty.client.get_me()
    ctime = await extract_time(catty, cattime)
    if not ctime:
        await catevent.edit(
            f"Invalid time type specified. Expected m , h , d or w not as {cattime}"
        )
        return
    if user.id == self_user.id:
        await catevent.edit(f"- Error, You can't")
        return
    try:
        await catevent.client(
            EditBannedRequest(
                catty.chat_id,
                user.id,
                ChatBannedRights(until_date=ctime, send_messages=True),
            )
        )
        # Announce that the function is done
        if reason:
            await catevent.edit(
                await catevent.edit(
                f"Successfully muted for: {cattime}"
            )
            )
            if BOTLOG:
                MarkZobregAlFred10_8788 = 0
        else:
            await catevent.edit(
                "Successfully muted"
            )
            if BOTLOG:
                MarkZo176bregAlFred10_8788 = 0
        # Announce to logging group
    except UserIdInvalidError:
        return await catevent.edit("لايمكنـني كتـم نفسـي")
    except UserAdminInvalidError:
        return await catevent.edit(
            "إما أنك لست مسؤولاً أو أنك حاولت تجاهل مسؤول لم تقم بترقيته "
        )
    except Exception as e:
        return await catevent.edit(f"`{str(e)}`")


@bot.on(admin_cmd(pattern="tban(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="tban(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def ban(catty):
    chat = await catty.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    # If not admin and not creator, return
    if not admin and not creator:
        await edit_or_reply(catty, NO_ADMIN)
        return
    catevent = await edit_or_reply(catty, "`جـاري الحظر مؤقت ....`")
    user, reason = await get_user_from_event(catty, catevent)
    if not user:
        return
    if reason:
        reason = reason.split(" ", 1)
        hmm = len(reason)
        cattime = reason[0]
        reason = reason[1] if hmm == 2 else None
    else:
        await catevent.edit("اذا لم تكن لديك معلومة عن الحظر المؤقت أرسل أمر `.info tadmin`")
        return
    self_user = await catty.client.get_me()
    ctime = await extract_time(catty, cattime)
    if not ctime:
        await catevent.edit(
            f"نوع الوقت المحدد غير صالح.  المتوقع m ، h ، d أو w ليس كما هو {cattime}"
        )
        return
    if user.id == self_user.id:
        await catevent.edit(f"Sorry, I can't ban myself")
        return
    await catevent.edit("- Error")
    try:
        await catty.client(
            EditBannedRequest(
                catty.chat_id,
                user.id,
                ChatBannedRights(until_date=ctime, view_messages=True),
            )
        )
    except UserAdminInvalidError:
        return await catevent.edit(
            "إما أنك لست مسؤولاً أو أنك حاولت حظر مسؤول لم تقم بترقيته"
        )
    except BadRequestError:
        await catevent.edit(NO_PERM)
        return
    # Helps ban group join spammers more easily
    try:
        reply = await catty.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        await catevent.edit(
            "لـيس لدي حقـوق كـافية "
        )
        return
    # Delete message and then tell that the command
    # is done gracefully
    # Shout out the ID, so that fedadmins can fban later
    if reason:
        await catevent.edit(
            f"- Successfully banned for: {cattime}"
        )
        if BOTLOG:
            MarkZobreg19AlFred10_8788 = 0
    else:
        await catevent.edit(
            f"- Successfully banned for: {cattime}"
        )
        if BOTLOG:
            Mark762Zobreg1AlFred10_8788 = 0


CMD_HELP.update(
    {
        "tadmin": "**Plugin :** `tadmin`\
      \n\n•  **Syntax : **`.tmute <reply/username/userid> <time> <reason>`\
      \n•  **Function : **__Temporary mutes the user for given time.__\
      \n\n•  **Syntax : **`.tban <reply/username/userid> <time> <reason>`\
      \n•  **Function : **__Temporary bans the user for given time.__\
      \n\n•  **Time units : ** __(2m = 2 minutes) ,(3h = 3hours)  ,(4d = 4 days) ,(5w = 5 weeks)\
      These times are example u can use anything with those units __"
    }
)
