from asyncio import sleep

from telethon.errors import ChatAdminRequiredError, UserAdminInvalidError
from telethon.tl import functions
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsKicked,
    ChatBannedRights,
    UserStatusEmpty,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusOffline,
    UserStatusOnline,
    UserStatusRecently,
)

from . import BOTLOG, BOTLOG_CHATID

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


@bot.on(admin_cmd(outgoing=True, pattern="kickme$"))
async def kickme(leave):
    await leave.edit("جـاري الخـروج من المجـموعة 𖠕")
    await leave.client.kick_participant(leave.chat_id, "me")



@bot.on(admin_cmd(pattern="unbanall ?(.*)"))
@bot.on(sudo_cmd(pattern="unbanall ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str:
        LOGS.info("TODO: Not yet Implemented")
    else:
        if event.is_private:
            return False
        et = await edit_or_reply(event, "جـاري مسـح المحظـورين 𖠕.")
        p = 0
        async for i in event.client.iter_participants(
            event.chat_id, filter=ChannelParticipantsKicked, aggressive=True
        ):
            rights = ChatBannedRights(until_date=0, view_messages=False)
            try:
                await event.client(
                    functions.channels.EditBannedRequest(event.chat_id, i, rights)
                )
            except Exception as ex:
                await et.edit(str(ex))
            else:
                p += 1
        await et.edit("{}: {} مسـح المحـظورين".format(event.chat_id, p))


@bot.on(admin_cmd(pattern="ikuck ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="ikuck ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return False
    input_str = event.pattern_match.group(1)
    if input_str:
        chat = await event.get_chat()
        if not chat.admin_rights and not chat.creator:
            await edit_or_reply(event, "`عـذرا انت لسـت ادمن هنـا`")
            return False
    p = 0
    b = 0
    c = 0
    d = 0
    e = []
    m = 0
    n = 0
    y = 0
    w = 0
    o = 0
    q = 0
    r = 0
    et = await edit_or_reply(event, "جـاري جـمع المـعلومـات 🔰.")
    async for i in event.client.iter_participants(event.chat_id):
        p += 1
        #
        # Note that it's "reversed". You must set to ``True`` the permissions
        # you want to REMOVE, and leave as ``None`` those you want to KEEP.
        rights = ChatBannedRights(until_date=None, view_messages=True)
        if isinstance(i.status, UserStatusEmpty):
            y += 1
            if "y" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("أحتاج امتيازات المسؤول لأداء هذا الإجراء!")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusLastMonth):
            m += 1
            if "m" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("أحتاج امتيازات المسؤول لأداء هذا الإجراء!")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusLastWeek):
            w += 1
            if "w" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("أحتاج امتيازات المسؤول لأداء هذا الإجراء!")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusOffline):
            o += 1
            if "o" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("أحتاج امتيازات المسؤول لأداء هذا الإجراء!")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if isinstance(i.status, UserStatusOnline):
            q += 1
            if "q" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("أحتاج امتيازات المسؤول لأداء هذا الإجراء!")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if isinstance(i.status, UserStatusRecently):
            r += 1
            if "r" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("أحتاج امتيازات المسؤول لأداء هذا الإجراء!")
                    e.append(str(e))
                    break
        if i.bot:
            b += 1
            if "b" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("أحتاج امتيازات المسؤول لأداء هذا الإجراء!")
                    e.append(str(e))
                    break
                else:
                    c += 1
        elif i.deleted:
            d += 1
            if "d" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("أحتاج امتيازات المسؤول لأداء هذا الإجراء!")
                    e.append(str(e))
        elif i.status is None:
            n += 1
    if input_str:
        required_string = """المـطرودين {} / {} الاعـضاء
الحسابات المحذوفة : {}
حالة المستخدم فارغة : {}
النشطـون منذ شـهر : {}
النشـطون منذ أسبوع : {}
الغـير نشـط : {}
النـشطون الان : {}
النشـطون قبـل قليـل : {}
البـوتات : {}
مـلاحظة : {}"""
        await et.edit(required_string.format(c, p, d, y, m, w, o, q, r, b, n))
        await sleep(5)
    await et.edit(
        """Total: {} users
الحسابات المحذوفة: {}
حالة المستخدم فارغة : {}
الحسابات النشطـون منذ شـهر : {}
النشطـون منذ أسبوع : {}
الـغير نشـطون : {}
النـشطون الان: {}
النشطـون قبـل قليـل: {}
البـوتات : {}
مـلاحظة : {}""".format(
            p, d, y, m, w, o, q, r, b, n
        )
    )


# Ported by ©[telethon-Ar](t.me/iqthon) and ©[dav](t.me/klanr)
@bot.on(admin_cmd(pattern=f"zombies ?(.*)"))
@bot.on(sudo_cmd(pattern="zombies ?(.*)", allow_sudo=True))
async def rm_deletedacc(show):
    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = "`لـم يتـم العـثور علـى حسـابات محـذوفـة 𖠕`"
    if con != "clean":
        event = await edit_or_reply(
            show, "جـاري البـحث عـن الحسـابات المـحذوفه 𖠕...`"
        )
        async for user in show.client.iter_participants(show.chat_id):
            if user.deleted:
                del_u += 1
                await sleep(0.5)
        if del_u > 0:
            del_status = f"__لـقد وجـدت__ **{del_u}** __مـجموع الحـسابات المحـذوفه ,\
                           \nلـتنضيف الحسابات المـحذوفة أرسـل أمر __ `.zombies clean`"
        await event.edit(del_status)
        return
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_delete(show, "انـا لـست أدمـن هنـا !`", 5)
        return
    event = await edit_or_reply(
        show, "`حذف الحسابات المحذوفة...\nحسنـا جـاري الحـذف ⛔`"
    )
    del_u = 0
    del_a = 0
    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client.kick_participant(show.chat_id, user.id)
                await sleep(0.5)
                del_u += 1
            except ChatAdminRequiredError:
                await edit_delete(event, "عـذرا هذا ليـس مجموعة`", 5)
                return
            except UserAdminInvalidError:
                del_a += 1
    if del_u > 0:
        del_status = f"المـحذوفين **{del_u}** عـدد المـحذوفين(s)"
    if del_a > 0:
        del_status = f"المـحذوفين **{del_u}** عدد المـحذوفين(s) \
        \n**{del_a}** لا تتم إزالة حسابات المشرف المحذوفة"
    await edit_delete(event, del_status, 5)
    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID,
            f"#CLEANUP\
            \n{del_status}\
            \nCHAT: {show.chat.title}(`{show.chat_id}`)",
        )


async def ban_user(chat_id, i, rights):
    try:
        await bot(functions.channels.EditBannedRequest(chat_id, i, rights))
        return True, None
    except Exception as exc:
        return False, str(exc)


CMD_HELP.update(
    {
        "groupactions": "**Plugin : **`groupactions`\
    \n\n•  **Syntax : **`.kickme`\
    \n•  **Function : **__Throws you away from that chat_\
    \n\n•  **Syntax : **``\
    \n•  **Function : **__To kick all users except admins from the chat__\
    \n\n•  **Syntax : **``\
    \n•  **Function : **__To ban all users except admins from the chat__\
    \n\n•  **Syntax : **`.unbanall`\
    \n•  **Function : **__Unbans everyone who are blocked in that group __\
    \n\n•  **Syntax : **`.ikuck`\
    \n•  **Function : **__stats of the group like no of users no of deleted users.__\
    \n\n•  **Syntax : **`.zombies`\
    \n•  **Function : **__Searches for deleted accounts in a group. Use `.zombies clean` to remove deleted accounts from the group.__"
    }
)
