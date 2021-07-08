import asyncio
import os
from datetime import datetime
from pathlib import Path

from ..utils import load_module, remove_plugin
from . import ALIVE_NAME, CMD_LIST, SUDO_LIST

DELETE_TIMEOUT = 5
thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"


@bot.on(admin_cmd(pattern="install$"))
@bot.on(sudo_cmd(pattern="install$", allow_sudo=True))
async def install(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await event.client.download_media(
                await event.get_reply_message(),
                "userbot/plugins/",
            )
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                await edit_or_reply(
                    event,
                    f"المـلف مثـبت 𖠕 `{os.path.basename(downloaded_file_name)}`",
                )
            else:
                os.remove(downloaded_file_name)
                await edit_or_reply(
                    event, "ان الـملـف مثـبت بـلفعـل 𖠕"
                )
        except Exception as e:
            await edit_or_reply(event, str(e))
            os.remove(downloaded_file_name)
    await asyncio.sleep(DELETE_TIMEOUT)
    await event.delete()


@bot.on(admin_cmd(pattern=r"load (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"load (.*)", allow_sudo=True))
async def load(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match.group(1)
    try:
        try:
            remove_plugin(shortname)
        except BaseException:
            pass
        load_module(shortname)
        await edit_or_reply(event, f"تم التحميل بنجاح {shortname}")
    except Exception as e:
        await edit_or_reply(
            event,
            f"لا يمكن التحميل {shortname} بسبب الخطأ التالي.\n{str(e)}",
        )


@bot.on(admin_cmd(pattern=r"send (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"send (.*)", allow_sudo=True))
async def send(event):
    if event.fwd_from:
        return
    reply_to_id = await reply_id(event)
    thumb = None
    if os.path.exists(thumb_image_path):
        thumb = thumb_image_path
    input_str = event.pattern_match.group(1)
    the_plugin_file = f"./userbot/plugins/{input_str}.py"
    if os.path.exists(the_plugin_file):
        start = datetime.now()
        caat = await event.client.send_file(
            event.chat_id,
            the_plugin_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            thumb=thumb,
        )
        end = datetime.now()
        ms = (end - start).seconds
        await event.delete()
        await caat.edit(
            f"__**𖠕 اسـم المـلف:- {input_str} .**__\n__**𖠕 تـم الـرفع {ms} ثـانية.**__\n__**➥ تـم الـرفع بـواسطة :-**__ {DEFAULTUSER}"
        )
    else:
        await edit_or_reply(event, "404: المـلف غيـر مـوجود 𖠕")


@bot.on(admin_cmd(pattern=r"unload (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"unload (.*)", allow_sudo=True))
async def unload(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match.group(1)
    try:
        remove_plugin(shortname)
        await edit_or_reply(event, f"تـم الـمسح {shortname} بنـجاح 𖠕")
    except Exception as e:
        await edit_or_reply(event, f"تـم مسـح بنـجاح {shortname}\n{str(e)} 𖠕")


@bot.on(admin_cmd(pattern=r"uninstall (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"uninstall (.*)", allow_sudo=True))
async def unload(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match.group(1)
    path = Path(f"userbot/plugins/{shortname}.py")
    if not os.path.exists(path):
        return await edit_delete(
            event, f"لا يوجد مكون إضافي مع مسار {path} لإلغاء تثبيته 𖠕"
        )
    os.remove(path)
    if shortname in CMD_LIST:
        CMD_LIST.pop(shortname)
    if shortname in SUDO_LIST:
        SUDO_LIST.pop(shortname)
    if shortname in CMD_HELP:
        CMD_HELP.pop(shortname)
    try:
        remove_plugin(shortname)
        await edit_or_reply(event, f"{shortname} تم إلغاء التثبيت بنجاح 𖠕")
    except Exception as e:
        await edit_or_reply(event, f"تم الإزالة بنجاح {shortname}\n{str(e)} 𖠕")


CMD_HELP.update(
    {
        "corecmds": """**Plugin : **`corecmds`

  •  **Syntax : **`.install`
  •  **Function : **__Reply to any external plugin to install in bot__ 
  
  •  **Syntax : **`.load <plugin name>`
  •  **Function : **__To load that plugin again__
  
  •  **Syntax : **`.send <plugin name>`  
  •  **Function : **__to send any plugin__
  
  •  **Syntax : **`.unload <plugin name>`
  •  **Function : **__To stop functioning of that plugin__ 
  
  •  **Syntax : **`.uninstall <plugin name>`
  •  **Function : **__To stop functioning of that plugin and remove that plugin from bot__ 
  
**Note : **__To unload a plugin permenantly from bot set __`NO_LOAD`__ var in heroku with that plugin name with space between plugin names__"""
    }
)
