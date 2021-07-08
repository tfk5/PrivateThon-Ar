

"""
----------------------------------------------------------------
All Thenks goes to Emily ( The creater of This Plugin)
\nSome credits goes to me ( @klanr ) for ported this plugin
\nand `klanr for` Helping me @iqthon .
----------------------------------------------------------------

Type `.poto` for get **All profile pics of that User**
\nOr type `.poto (number)` to get the **desired number of photo of a User** .
"""


name = "Profile Photos"


@bot.on(admin_cmd(pattern="poto ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="poto ?(.*)", allow_sudo=True))
async def potocmd(event):
    uid = "".join(event.raw_text.split(maxsplit=1)[1:])
    user = await event.get_reply_message()
    chat = event.input_chat
    if user:
        photos = await event.client.get_profile_photos(user.sender)
        u = True
    else:
        photos = await event.client.get_profile_photos(chat)
        u = False
    if uid.strip() == "":
        uid = 1
        if int(uid) > (len(photos)):
            return await edit_delete(
                event, "عـذرا الشـخص لايـضع صور 𖠕"
            )
        send_photos = await event.client.download_media(photos[uid - 1])
        await event.client.send_file(event.chat_id, send_photos)
    elif uid.strip() == "all":
        if len(photos) > 0:
            await event.client.send_file(event.chat_id, photos)
        else:
            try:
                if u:
                    photo = await event.client.download_profile_photo(user.sender)
                else:
                    photo = await event.client.download_profile_photo(event.input_chat)
                await event.client.send_file(event.chat_id, photo)
            except Exception:
                return await edit_delete(event, "هذا المستخدم ليس لديه صور لتظهر لك 𖠕")
    else:
        try:
            uid = int(uid)
            if uid <= 0:
                await edit_or_reply(
                    event, "الـرقم غـير صحـيح 𖠕"
                )
                return
        except BaseException:
            await edit_or_reply(event, "خـطأ 𖠕")
            return
        if int(uid) > (len(photos)):
            return await edit_delere(
                event, "هـذا المستـخدم ليـس لديـة صـور لتـضهر لـك 𖠕"
            )

        send_photos = await event.client.download_media(photos[uid - 1])
        await event.client.send_file(event.chat_id, send_photos)
    await event.delete()


CMD_HELP.update(
    {
        "poto": """**Plugin : **`poto`

•  **Syntax : **`.poto`
•  **Function : **__reply to user to get his profile pic use command along \
with profile pic number to get desired pic else use .poto all to get all if you dont reply then gets group pics__"""
    }
)
