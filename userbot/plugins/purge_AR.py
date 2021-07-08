# Userbot module for purging unneeded messages(usually spam or ot).

from asyncio import sleep

from telethon.errors import rpcbaseerrors

from ..utils import errors_handler
from . import BOTLOG, BOTLOG_CHATID

purgelist = {}


@bot.on(admin_cmd(pattern="purge(?: |$)(.*)"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="purge(?: |$)(.*)"))
@errors_handler
async def fastpurger(event):
    if event.fwd_from:
        return
    chat = await event.get_input_chat()
    msgs = []
    count = 0
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if reply:
        if input_str and input_str.isnumeric():
            count += 1
            async for msg in event.client.iter_messages(
                event.chat_id,
                limit=(int(input_str) - 1),
                offset_id=reply.id,
                reverse=True,
            ):
                msgs.append(msg)
                count += 1
                msgs.append(event.reply_to_msg_id)
                if len(msgs) == 100:
                    await event.client.delete_messages(chat, msgs)
                    msgs = []
        elif input_str:
            return await edit_or_reply(
                event, f"**هنـاك خطـأ**\n`{input_str} ليس عددًا صحيحًا.  استخدم بناء الجملة الصحيح.`"
            )
        else:
            async for msg in event.client.iter_messages(
                chat, min_id=event.reply_to_msg_id
            ):
                msgs.append(msg)
                count += 1
                msgs.append(event.reply_to_msg_id)
                if len(msgs) == 100:
                    await event.client.delete_messages(chat, msgs)
                    msgs = []
    else:
        await edit_or_reply(
            event,
            "`لـم يتـم تحـديد رسـالة 𖠕.`",
        )
        return
    if msgs:
        await event.client.delete_messages(chat, msgs)
    await event.delete()
    hi = await event.client.send_message(
        event.chat_id,
        "اكـتمل حـذف رسائل بنجـاح 𖠕 \nمـعلومات الحـذف 𖠕 " + str(count) + " messages.` 𖠕",
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "حـذف الـرسائـل \n`معـلومات الحـذف " + str(count) + " تـم الانتـهاء بنـجاح 𖠕.`",
        )
    await sleep(5)
    await hi.delete()


@bot.on(admin_cmd(pattern="purgefrom$"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="purgefrom$"))
@errors_handler
async def purge_from(event):
    if event.fwd_from:
        return
    reply = await event.get_reply_message()
    if reply:
        reply_message = await reply_id(event)
        purgelist[event.chat_id] = reply_message
        await edit_delete(
            event,
            "`تم وضع علامة على هذه الرسالة للحذف.  قم بالرد على رسالة أخرى باستخدام purgeto لحذف جميع الرسائل بينهما 𖠕`",
        )
    else:
        await edit_delete(event, "`الرد على رسالة لإعلامي بما يجب حذفه 𖠕.`")


@bot.on(admin_cmd(pattern="purgeto$"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="purgeto$"))
@errors_handler
async def purge_to(event):
    chat = await event.get_input_chat()
    if event.fwd_from:
        return
    reply = await event.get_reply_message()
    try:
        from_message = purgelist[event.chat_id]
    except KeyError:
        return await edit_delete(
            event,
            "`قم أولاً بتمييز الرسالة بمسح من ثم وضع علامة purgeto. لذلك ، يمكنني الحذف بين الرسائل`",
        )
    if not reply or not from_message:
        return await edit_delete(
            event,
            "`قم أولاً بتمييز الرسالة بمسح من ثم وضع علامة purgeto. لذلك ، يمكنني الحذف بين الرسائل 𖠕`",
        )
    try:
        to_message = await reply_id(event)
        msgs = []
        count = 0
        async for msg in event.client.iter_messages(
            event.chat_id, min_id=(from_message - 1), max_id=(to_message + 1)
        ):
            msgs.append(msg)
            count += 1
            msgs.append(event.reply_to_msg_id)
            if len(msgs) == 100:
                await event.client.delete_messages(chat, msgs)
                msgs = []
        if msgs:
            await event.client.delete_messages(chat, msgs)
        await edit_delete(
            event,
            "`تـم اكتـمال الحـذف الاستثنائـي 𖠕!\nالمـحذوفات 𖠕 " + str(count) + " messages.` 𖠕",
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "حـذف الاستـثنائي 𖠕 \n`حـذف لـ " + str(count) + " تـم بنـجاح 𖠕.`",
            )
    except Exception as e:
        await edit_delete(event, f"**عـذرا يـوجد هنـاك خطـأ**\n`{str(e)}` 𖠕")


@bot.on(admin_cmd(pattern="purgeme"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="purgeme"))
@errors_handler
async def purgeme(event):
    if event.fwd_from:
        return
    message = event.text
    count = int(message[9:])
    i = 1

    async for message in event.client.iter_messages(event.chat_id, from_user="me"):
        if i > count + 1:
            break
        i += 1
        await message.delete()

    smsg = await event.client.send_message(
        event.chat_id,
        "**الـحذف اكـتمـل 𖠕**` الـحذف " + str(count) + " رسـائل 𖠕.`",
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "حـذف رسائـلي \n`لـ حذف " + str(count) + " انتـهى بنجـاح 𖠕.`",
        )
    await sleep(5)
    await smsg.delete()


@bot.on(admin_cmd(pattern="del(?: |$)(.*)"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="del(?: |$)(.*)"))
@errors_handler
async def delete_it(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    msg_src = await event.get_reply_message()
    if msg_src:
        if input_str and input_str.isnumeric():
            await event.delete()
            await sleep(int(input_str))
            try:
                await msg_src.delete()
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID, "#حـذف \n`تم حذف الرسالة بنجاح 𖠕`"
                    )
            except rpcbaseerrors.BadRequestError:
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "`حسنًا ، لا يمكنني حذف رسالة.  أنا لست مشرفًا 𖠕`",
                    )
        elif input_str:
            if not input_str.startswith("var"):
                await edit_or_reply(event, "`حسنًا ، الوقت الذي ذكرته غير صالح.`")
        else:
            try:
                await msg_src.delete()
                await event.delete()
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID, "#حـذف \n`تم حذف الرسالة بنجاح 𖠕`"
                    )
            except rpcbaseerrors.BadRequestError:
                await edit_or_reply(event, "`حسنًا ، لا يمكنني حذف رسالة 𖠕`")
    else:
        if not input_Str:
            await event.delete()


CMD_HELP.update(
    {
        "purge": "**Plugin : **`purge`\
        \n\n•  **Syntax : **`.purge <count> reply`\
        \n•  **Function : **__Deletes the x(count) amount of messages from the replied message if you don't use count then deletes all messages from there.__\
        \n\n•  **Syntax : **`.purgefrom reply`\
        \n•  **Function : **__Will Mark that message as oldest message of interval to delete messages.__\
        \n\n•  **Syntax : **`.purgeto reply`\
        \n•  **Function : **__Will Mark that message as newest message of interval to delete messages and will delete all messages in that interval.__\
        \n\n•  **Syntax : **`.purgeme <count>`\
        \n•  **Function : **__Deletes x(count) amount of your latest messages.__\
        \n\n•  **Syntax : **`.del <count> reply`\
        \n•  **Function : **__Deletes the message you replied to in x(count) seconds if count is not used then deletes immediately.__"
    }
)
