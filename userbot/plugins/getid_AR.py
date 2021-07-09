from telethon.utils import pack_bot_file_id


@bot.on(admin_cmd(pattern="(get_id|id)( (.*)|$)"))
@bot.on(sudo_cmd(pattern="(get_id|id)( (.*)|$)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(2)
    if input_str:
        try:
            p = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(event, f"- Error :  [{str(e)}]", 5)
        try:
            if p.first_name:
                return await edit_or_reply(
                    event, f"- USER ID :  [{input_str} {p.id}]"
                )
        except Exception:
            try:
                if p.title:
                    return await edit_or_reply(
                        event, f"- Chat-ID :  [{p.title} {p.id}]"
                    )
            except Exception as e:
                LOGS.info(str(e))
        await edit_or_reply(event, "- Error, Put correct user/id or replay")
    elif event.reply_to_msg_id:
        await event.get_input_chat()
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await edit_or_reply(
                event,
                f"- Chat-ID :  [{str(event.chat_id)}]\n- User-ID :  [{str(r_msg.sender_id)}]\n- File-ID : [{bot_api_file_id}]",
            )
        else:
            await edit_or_reply(
                event,
                f"- Chat-ID :  [{str(event.chat_id)}]\n- User-ID :  [{str(r_msg.sender_id)}]",
            )
    else:
        await edit_or_reply(event, f"- Chat-ID :  [{str(event.chat_id)}]")


CMD_HELP.update(
    {
        "getid": "**Plugin : **`getid`\
    \n\n  •  **Syntax : **`.get_id` or `.id`\
    \n  •  **Function : **__if given input then shows id of that given chat/channel/user else if you reply to user then shows id of the replied user \
    along with current chat id and if not replied to user or given input then just show id of the chat where you used the command__"
    }
)
