import asyncio
import os
import time
from datetime import datetime

from . import progress, reply_id

thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "thumb_image.jpg"


@bot.on(admin_cmd(pattern="rename (.*)"))
@bot.on(sudo_cmd(pattern="rename (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    catevent = await edit_or_reply(
        event,
        "**جـاري اعـادة تـعين اسـم الـملف 𖠕**",
    )
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        file_name = input_str
        reply_message = await event.get_reply_message()
        c_time = time.time()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await event.client.download_media(
            reply_message,
            downloaded_file_name,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, catevent, c_time, "حـاول مجـددآ 𖠕", file_name)
            ),
        )
        end = datetime.now()
        ms = (end - start).seconds
        if os.path.exists(downloaded_file_name):
            await catevent.edit(
                f"**تم تنزيل الملف بتنسيق {ms} ثـواني.**\n**مكان الملف : **`{downloaded_file_name}` 𖠕"
            )
        else:
            await catevent.edit("Error Occurred\n {}".format(input_str))
    else:
        await catevent.edit(
            "**Syntax : ** `.rename file.name` as reply to a Telegram media"
        )


CMD_HELP.update(
    {
        "rename": "**Plugin : **`rename`\
        \n\n  •  **Syntax : **`.rename filename`\
        \n  •  **Function : **__Reply to media with above command to save in your server with that given filename__\
        \n\n  •  **Syntax : **`.rnup filename`\
        \n  •  **Function : **__Reply to media with above command to rename and upload the file with given name as steam__\
        \n\n  •  **Syntax : **`.rnupf filename`\
        \n  •  **Function : **__Reply to media with above command to rename and upload the file with given name as file__\
        "
    }
)
