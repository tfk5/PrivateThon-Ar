import asyncio
import io
import os
from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE

if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
    os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)




@bot.on(admin_cmd(pattern="date$"))
@bot.on(sudo_cmd(pattern="date$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    #    dirname = event.pattern_match.group(1)
    #    tempdir = "localdir"
    cmd = "date"
    #    if dirname == tempdir:
    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        eply_to_id = event.reply_to_msg_id
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id,
            )
            await event.delete()
    else:
        event = await edit_or_reply(event, OUTPUT)


@bot.on(admin_cmd(pattern="env$"))
async def _(event):
    if event.fwd_from:
        return
    cmd = "env"
    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        eply_to_id = event.reply_to_msg_id

    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = (
        f"**[Telethon-AR](tg://need_update_for_some_feature/) Environment Module:**\n\n\n{o}"
    )
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id,
            )
            await event.delete()
    else:
        event = await edit_or_reply(event, OUTPUT)



CMD_HELP.update(
    {
        "execmod": "**Plugin : **`execmod`\
    \n\n**Syntax :** `.pips query`\
    \n**Usage : **Searches your pip modules\
    \n\n**Syntax : **`.sucide`\
    \n**Usage : **Deletes all your folders and files in the bot\
    \n\n**Syntax : **`.plugins`\
    \n**Usage : **Shows you the list of modules that are in bot\
    \n\n**Syntax : **`.date`\
    \n**Usage : **Shows you the date of today\
    \n\n**Syntax : **`.env`\
    \n**Usage : **Shows you the list of all your heroku vars\
    \n\n**Syntax : **`.fast`\
    \n**Usage : **speed calculator\
    \n\n**Syntax : **`.fortune`\
    \n**Usage : **Fortune teller\
    \n\n**Syntax : **`.qquote`\
    \n**Usage : **Random quote generator\
    \n\n**Syntax : **`.fakeid`\
    \n**Usage : **Random fakeid generator\
    \n\n**Syntax : **`.kwot`\
    \n**Usage : **An awesome random quote generator.\
    \n\n**Syntax : **`.qpro`\
    \n**Usage : **Programming Quotes\
    "
    }
)
