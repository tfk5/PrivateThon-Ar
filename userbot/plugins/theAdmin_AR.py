from asyncio import sleep

from telethon import functions
from telethon.errors import (
    BadRequestError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChatAdminRights, ChatBannedRights, MessageMediaPhoto

from ..utils import errors_handler
from . import BOTLOG, BOTLOG_CHATID, LOGS, get_user_from_event
from .sql_helper.mute_sql import is_muted, mute, unmute

# =================== CONSTANT ===================

PP_TOO_SMOL = "**𖠕 الصـورة صغيـرة جدًا**"
PP_ERROR = "**𖠕 فشـل أثنـاء معالجـة الصـورة**"
NO_ADMIN = "**𖠕 انـا لسـت مـديرآ فـي هـذا المجموعـة**"
NO_PERM = "**𖠕 عـذرا ليـست لدي صـلاحيات كـافية**"
CHAT_PP_CHANGED = "**𖠕 تـم تغير صورة المـجموعة**"
INVALID_MEDIA = "**𖠕 الـعامل غير صـالح**"

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

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

# ================================================


@bot.on(admin_cmd(pattern="setgpic$"))
@bot.on(sudo_cmd(pattern="setgpic$", allow_sudo=True))
@errors_handler
async def set_group_photo(gpic):
    if gpic.fwd_from:
        return
    if not gpic.is_group:
        await edit_or_reply(gpic, "**𖠕 انـا لسـت مـديرآ فـي هـذا المجموعـة**.")
        return
    replymsg = await gpic.get_reply_message()
    await gpic.get_chat()
    photo = None
    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await gpic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split("/"):
            photo = await gpic.client.download_file(replymsg.media.document)
        else:
            await edit_or_reply(gpic, INVALID_MEDIA)
    sandy = None
    if photo:
        try:
            await gpic.client(
                EditPhotoRequest(gpic.chat_id, await gpic.client.upload_file(photo))
            )
            await edit_or_reply(gpic, CHAT_PP_CHANGED)
            sandy = True
        except PhotoCropSizeSmallError:
            await edit_or_reply(gpic, PP_TOO_SMOL)
        except ImageProcessFailedError:
            await edit_or_reply(gpic, PP_ERROR)
        except Exception as e:
            await edit_or_reply(gpic, f"**Error : **`{str(e)}`")
        if BOTLOG and sandy:
            await gpic.client.send_message(
                BOTLOG_CHATID,
                "#GROUPPIC\n"
                f"**مجموعة تغيير الموافقة المسبقة عن علم**"
                f"المحادثة: {gpic.chat.title}(`{gpic.chat_id}`)",
            )


@bot.on(admin_cmd(pattern="promote(?: |$)(.*)", command="promote"))
@bot.on(sudo_cmd(pattern="promote(?: |$)(.*)", command="promote", allow_sudo=True))
@errors_handler
async def promote(promt):
    if promt.fwd_from:
        return
    if not promt.is_group:
        await edit_or_reply(promt, "**𖠕 لاأعـتقد أن هذا مجمـوعة**")
        return
    chat = await promt.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(promt, NO_ADMIN)
        return
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )
    catevent = await edit_or_reply(promt, "**𖠕 تم رفع مشرف بنجاح **")
    user, rank = await get_user_from_event(promt, catevent)
    if not rank:
        rank = "Admin"
    if not user:
        return
    try:
        await promt.client(EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await catevent.edit("**تم الترقية بنجاح 𖠕**")
    except BadRequestError:
        await catevent.edit(NO_PERM)
        return
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID,
            "#PROMOTE\n"
            f"المعرف: [{user.first_name}](tg://user?id={user.id})\n"
            f"المحادثة: {promt.chat.title}(`{promt.chat_id}`)",
        )


@bot.on(admin_cmd(pattern="demote(?: |$)(.*)", command="demote"))
@bot.on(sudo_cmd(pattern="demote(?: |$)(.*)", command="demote", allow_sudo=True))
@errors_handler
async def demote(dmod):
    if dmod.fwd_from:
        return
    if not dmod.is_group:
        await edit_or_reply(dmod, "**𖠕 لاأعـتقد أن هذا مجمـوعة**")
        return
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(dmod, NO_ADMIN)
        return
    catevent = await edit_or_reply(dmod, "**𖠕 تم حذف الاشراف بنجاح **")
    rank = "admeme"
    user = await get_user_from_event(dmod, catevent)
    user = user[0]
    if not user:
        return
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    try:
        await dmod.client(EditAdminRequest(dmod.chat_id, user.id, newrights, rank))
    except BadRequestError:
        await catevent.edit(NO_PERM)
        return
    await catevent.edit("**𖠕 تم حذف الاشراف بنجاح **")
    if BOTLOG:
        await dmod.client.send_message(
            BOTLOG_CHATID,
            "#DEMOTE\n"
            f"المعرف: [{user.first_name}](tg://user?id={user.id})\n"
            f"المحادثة: {dmod.chat.title}(`{dmod.chat_id}`)",
        )


@bot.on(admin_cmd(pattern="ban(?: |$)(.*)", command="ban"))
@bot.on(sudo_cmd(pattern="ban(?: |$)(.*)", command="ban", allow_sudo=True))
@errors_handler
async def ban(bon):
    if bon.fwd_from:
        return
    if not bon.is_group:
        await edit_or_reply(bon, "𖠕 لاأعـتقد أن هذا مجمـوعة")
        return
    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(bon, NO_ADMIN)
        return
    catevent = await edit_or_reply(bon, "`Whacking the pest!`")
    user, reason = await get_user_from_event(bon, catevent)
    if not user:
        return
    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        await catevent.edit(NO_PERM)
        return
    try:
        reply = await bon.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        await catevent.edit(
            "**𖠕 عـذرا ليـست لدي صـلاحيات كـافية**"
        )
        return
    if reason:
        await catevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)}` لقـد تـم حظـرة من المـجموعة : !!`\n**السبب : : **`{reason}`"
        )
    else:
        await catevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)} `لقـد تـم حظـرة من المـجموعة !!`"
        )
    if BOTLOG:
        await bon.client.send_message(
            BOTLOG_CHATID,
            "#BAN\n"
            f"المعرف: [{user.first_name}](tg://user?id={user.id})\n"
            f"المحادثة: {bon.chat.title}(`{bon.chat_id}`)",
        )


@bot.on(admin_cmd(pattern="unban(?: |$)(.*)", command="unban"))
@bot.on(sudo_cmd(pattern="unban(?: |$)(.*)", command="unban", allow_sudo=True))
@errors_handler
async def nothanos(unbon):
    if unbon.fwd_from:
        return
    if not unbon.is_group:
        await edit_or_reply(unbon, "𖠕 لاأعـتقد أن هذا مجمـوعة")
        return
    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(unbon, NO_ADMIN)
        return
    catevent = await edit_or_reply(unbon, "**𖠕 جـاري فـك الحظر ..**")
    user = await get_user_from_event(unbon, catevent)
    user = user[0]
    if not user:
        return
    try:
        await unbon.client(EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await catevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)} `𖠕 تـم فـك الحـظر الان`"
        )
        if BOTLOG:
            await unbon.client.send_message(
                BOTLOG_CHATID,
                "#UNBAN\n"
                f"المعرف: [{user.first_name}](tg://user?id={user.id})\n"
                f"المحادثة: {unbon.chat.title}(`{unbon.chat_id}`)",
            )
    except UserIdInvalidError:
        await catevent.edit("**اوة**")


@bot.on(admin_cmd(incoming=True))
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        try:
            await event.delete()
        except Exception as e:
            LOGS.info(str(e))


@bot.on(admin_cmd(pattern="gggmute(?: |$)(.*)", command="gggmute"))
@bot.on(sudo_cmd(pattern="gggmute(?: |$)(.*)", command="gggmute", allow_sudo=True))
async def startmute(event):
    if event.fwd_from:
        return
    if event.is_private:
        await event.edit("**𖠕 جاري كتم المـستخدم**")
        await sleep(2)
        await event.get_reply_message()
        userid = event.chat_id
        replied_user = await event.client(GetFullUserRequest(userid))
        chat_id = event.chat_id
        if is_muted(userid, chat_id):
            return await event.edit(
                "**𖠕 هذا المستخدم مكتوم بالفعل في هذه الدردشة**"
            )
        try:
            mute(userid, chat_id)
        except Exception as e:
            await event.edit(f"**هنـاك خطـأ **\n`{str(e)}`")
        else:
            await event.edit("**𖠕 تـم كتـم المسـتخدم بنجـاح**")
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#PM_MUTE\n"
                f"**المعرف :** [{replied_user.user.first_name}](tg://user?id={userid})\n",
            )
    else:
        chat = await event.get_chat()
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == bot.uid:
            return await edit_or_reply(event, "**𖠕 اعتـذر لايمكنني كتـم نفـسي**")
        if is_muted(user.id, event.chat_id):
            return await edit_or_reply(
                event, ""
            )
        try:
            admin = chat.admin_rights
            creator = chat.creator
            if not admin and not creator:
                await edit_or_reply(
                    event, "**𖠕 عـذرا ليـست لدي صـلاحيات كـافية**"
                )
                return
            result = await event.client(
                functions.channels.GetParticipantRequest(
                    channel=event.chat_id, user_id=user.id
                )
            )
            try:
                if result.participant.banned_rights.send_messages:
                    return await edit_or_reply(
                        event,
                        "**𖠕 هذا المستخدم مكتوم بالفعل في هذه الدردشة**",
                    )
            except Exception as e:
                LOGS.info(str(e))
            await event.client(EditBannedRequest(event.chat_id, user.id, MUTE_RIGHTS))
        except UserAdminInvalidError:
            if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
                if chat.admin_rights.delete_messages is not True:
                    return await edit_or_reply(
                        event,
                        "𖠕 عـذرا ليـست لدي صـلاحيات كـافية",
                    )
            elif "creator" not in vars(chat):
                return await edit_or_reply(
                    event, "𖠕 عـذرا ليـست لدي صـلاحيات كـافية"
                )
            try:
                mute(user.id, event.chat_id)
            except Exception as e:
                return await edit_or_reply(event, f"**هنـاك خطـأ**\n`{str(e)}`")
        except Exception as e:
            return await edit_or_reply(event, f"**هنـاك خطأ : **`{str(e)}`")
        if reason:
            await edit_or_reply(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} `الان مكـتوم فـي : {event.chat.title}`\n"
                f"`السـبب:`{reason}",
            )
        else:
            await edit_or_reply(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} `الان مكـتوم فـي {event.chat.title}`\n",
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#MUTE\n"
                f"**المعرف :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**المحـادثة :** {event.chat.title}(`{event.chat_id}`)",
            )


@bot.on(admin_cmd(pattern="gggunmute(?: |$)(.*)", command="gggunmute"))
@bot.on(sudo_cmd(pattern="gggunmute(?: |$)(.*)", command="gggunmute", allow_sudo=True))
async def endmute(event):
    if event.fwd_from:
        return
    if event.is_private:
        await event.edit("**𖠕 جاري كتم المـستخدم**")
        await sleep(1)
        userid = event.chat_id
        replied_user = await event.client(GetFullUserRequest(userid))
        chat_id = event.chat_id
        if not is_muted(userid, chat_id):
            return await event.edit(
                "**𖠕 لـم يتـم كتـم هذا المسـتخدم في المجـموعـة**"
            )
        try:
            unmute(userid, chat_id)
        except Exception as e:
            await event.edit(f"**Error **\n`{str(e)}`")
        else:
            await event.edit(
                "**𖠕 لقـد تم مسـح الكتـم من المسـتخدم**"
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#PM_UNMUTE\n"
                f"**المعرف :** [{replied_user.user.first_name}](tg://user?id={userid})\n",
            )
    else:
        user = await get_user_from_event(event)
        user = user[0]
        if not user:
            return
        try:
            if is_muted(user.id, event.chat_id):
                unmute(user.id, event.chat_id)
            else:
                result = await event.client(
                    functions.channels.GetParticipantRequest(
                        channel=event.chat_id, user_id=user.id
                    )
                )
                try:
                    if result.participant.banned_rights.send_messages:
                        await event.client(
                            EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS)
                        )
                except Exception:
                    return await edit_or_reply(
                        event,
                        "𖠕 عـذرا ليـست لدي صـلاحيات كـافية",
                    )
        except Exception as e:
            return await edit_or_reply(event, f"**Error : **`{str(e)}`")
        await edit_or_reply(
            event,
            f"{_format.mentionuser(user.first_name ,user.id)} `لقـد تم مسـح الكـتم {event.chat.title}`",
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNMUTE\n"
                f"**المعرف :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**المحادثة :** {event.chat.title}(`{event.chat_id}`)",
            )


@bot.on(admin_cmd(pattern="kick(?: |$)(.*)", command="kick"))
@bot.on(sudo_cmd(pattern="kick(?: |$)(.*)", command="kick", allow_sudo=True))
@errors_handler
async def kick(usr):
    if usr.fwd_from:
        return
    if not usr.is_group:
        await edit_or_reply(usr, "𖠕 لاأعـتقد أن هذا مجمـوعة")
        return
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(usr, NO_ADMIN)
        return
    user, reason = await get_user_from_event(usr)
    if not user:
        return
    catevent = await edit_or_reply(usr, "𖠕 جـاري الحـظر ...")
    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(0.5)
    except Exception as e:
        await catevent.edit(NO_PERM + f"\n{str(e)}")
        return
    if reason:
        await catevent.edit(
            f"`تـم الطرد ` [{user.first_name}](tg://user?id={user.id})`!`\nReason: {reason}"
        )
    else:
        await catevent.edit(f"`تـم الطرد` [{user.first_name}](tg://user?id={user.id})`!`")
    if BOTLOG:
        await usr.client.send_message(
            BOTLOG_CHATID,
            "#KICK\n"
            f"المعرف: [{user.first_name}](tg://user?id={user.id})\n"
            f"المحادثة: {usr.chat.title}(`{usr.chat_id}`)\n",
        )


@bot.on(admin_cmd(pattern="pin($| (.*))", command="pin"))
@bot.on(sudo_cmd(pattern="pin($| (.*))", command="pin", allow_sudo=True))
@errors_handler
async def pin(msg):
    if msg.fwd_from:
        return
    if not msg.is_private:
        await msg.get_chat()
    to_pin = msg.reply_to_msg_id
    if not to_pin:
        return await edit_delete(msg, "`Reply to a message to pin it.`", 5)
    options = msg.pattern_match.group(1)
    is_silent = False
    if options == "loud":
        is_silent = True
    try:
        await msg.client.pin_message(msg.chat_id, to_pin, notify=is_silent)
    except BadRequestError:
        return await edit_delete(msg, NO_PERM, 5)
    except Exception as e:
        return await edit_delete(msg, f"`{str(e)}`", 5)
    await edit_delete(msg, "**𖠕 تـم التثـبيت بنـجاح**", 3)
    user = await get_user_from_id(msg.sender_id, msg)
    if BOTLOG and not msg.is_private:
        try:
            await msg.client.send_message(
                BOTLOG_CHATID,
                "#PIN\n"
                f"الادمـن: [{user.first_name}](tg://user?id={user.id})\n"
                f"المحـادثـة: {msg.chat.title}(`{msg.chat_id}`)\n"
                f"قـائمة: {is_silent}",
            )
        except Exception as e:
            LOGS.info(str(e))


@bot.on(admin_cmd(pattern="unpin($| (.*))", command="unpin"))
@bot.on(sudo_cmd(pattern="unpin($| (.*))", command="unpin", allow_sudo=True))
@errors_handler
async def pin(msg):
    if msg.fwd_from:
        return
    if not msg.is_private:
        await msg.get_chat()
    to_unpin = msg.reply_to_msg_id
    options = (msg.pattern_match.group(1)).strip()
    if not to_unpin and options != "all":
        await edit_delete(msg, "**𖠕 الرد على رسالة لإلغاء تثبيتها**", 5)
        return
    if to_unpin and not options:
        try:
            await msg.client.unpin_message(msg.chat_id, to_unpin)
        except BadRequestError:
            return await edit_delete(msg, NO_PERM, 5)
        except Exception as e:
            return await edit_delete(msg, f"`{str(e)}`", 5)
    elif options == "all":
        try:
            await msg.client.unpin_message(msg.chat_id)
        except BadRequestError:
            return await edit_delete(msg, NO_PERM, 5)
        except Exception as e:
            return await edit_delete(msg, f"`{str(e)}`", 5)
    else:
        return await edit_delete(
            msg, "**الرد على رسالة لإلغاء تثبيتها**", 5
        )
    await edit_delete(msg, "**𖠕 تـم فـك الـحظر بنـجاح**", 3)
    user = await get_user_from_id(msg.sender_id, msg)
    if BOTLOG and not msg.is_private:
        try:
            await msg.client.send_message(
                BOTLOG_CHATID,
                "#UNPIN\n"
                f"**الادمـن : **[{user.first_name}](tg://user?id={user.id})\n"
                f"**المحـادثـة : **{msg.chat.title}(`{msg.chat_id}`)\n",
            )
        except Exception as e:
            LOGS.info(str(e))


@bot.on(admin_cmd(pattern="iundlt$", command="iundlt"))
@bot.on(sudo_cmd(pattern="iundlt$", command="iundlt", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.is_group:
        await edit_or_reply(event, "**𖠕 لاأعـتقد أن هذا مجمـوعة**")
        return
    c = await event.get_chat()
    if c.admin_rights or c.creator:
        a = await event.client.get_admin_log(
            event.chat_id, limit=5, edit=False, delete=True
        )
        deleted_msg = "الرسـائل المحـذوفة فـي هذا المـجموعـة"
        for i in a:
            deleted_msg += "\n👉`{}`".format(i.old.message)
        await edit_or_reply(event, deleted_msg)
    else:
        await edit_or_reply(
            event, "**𖠕 عـذرا ليـست لدي صـلاحيات كـافية**"
        )
        await sleep(3)
        try:
            await event.delete()
        except Exception as e:
            LOGS.info(str(e))


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj


CMD_HELP.update(
    {
        "اوامر الادمن": "**Plugin : **`اوامر الادمن`\
        \n\n  •  **Syntax : **`.setgpic` <reply to image>\
        \n  •  **Usage : **Changes the group's display picture\
        \n\n  •  **Syntax : **`.promote` <username/reply> <custom rank (optional)>\
        \n  •  **Usage : **Provides admin rights to the person in the chat.\
        \n\n  •  **Syntax : **`.demote `<username/reply>\
        \n  •  **Usage : **Revokes the person's admin permissions in the chat.\
        \n\n  •  **Syntax : **`.ban` <username/reply> <reason (optional)>\
        \n  •  **Usage : **Bans the person off your chat.\
        \n\n  •  **Syntax : **`.unban` <username/reply>\
        \n  •  **Usage : **Removes the ban from the person in the chat.\
        \n\n  •  **Syntax : **`.mute` <username/reply> <reason (optional)>\
        \n  •  **Usage : **Mutes the person in the chat, works on admins too.\
        \n\n  •  **Syntax : **`.unmute` <username/reply>\
        \n  •  **Usage : **Removes the person from the muted list.\
        \n\n  •  **Syntax : **`.pin `<reply> or `.pin loud`\
        \n  •  **Usage : **Pins the replied message in Group\
        \n\n  •  **Syntax : **`.unpin `<reply> or `.unpin all`\
        \n  •  **Usage : **Unpins the replied message in Group\
        \n\n  •  **Syntax : **`.kick `<username/reply> \
        \n  •  **Usage : **kick the person off your chat.\
        \n\n  •  **Syntax : **`.iundlt`\
        \n  •  **Usage : **display last 5 deleted messages in group."
    }
)
