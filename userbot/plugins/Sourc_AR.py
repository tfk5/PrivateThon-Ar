import time
from platform import python_version

from telethon import version

from . import ALIVE_NAME, StartTime, catversion, get_readable_time, mention, reply_id

DEFAULTUSER = ALIVE_NAME or "Mark²"
CAT_IMG = Config.ALIVE_PIC or "https://i.top4top.io/p_2016j6gmf0.jpg"
CUSTOM_ALIVE_TEXT = Config.CUSTOM_ALIVE_TEXT or "- PrivateThon"
EMOJI = Config.CUSTOM_ALIVE_EMOJI or "{][}"


@bot.on(admin_cmd(outgoing=True, pattern="alive$"))
@bot.on(sudo_cmd(pattern="alive$", allow_sudo=True))
async def amireallyalive(alive):
    if alive.fwd_from:
        return
    reply_to_id = await reply_id(alive)
    uptime = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    if CAT_IMG:
        cat_caption = f"- 𝚂𝚃𝙰𝚃𝚄𝚂 :  Working\n"
        cat_caption += f"- 𝚅𝙴𝚁𝚂𝙸𝙾𝙽 :  7.7.7\n"
        cat_caption += f"- 𝚁𝚄𝙽𝚃𝙸𝙼𝙴 :  {uptime}\n"
        cat_caption += f"- 𝚄𝚂𝙴𝚁 :  {mention}\n"
        cat_caption += f"- 𝙳𝙴𝚅 :  [ᴅᴇᴠ](t.me/i_M_5)"
        await alive.client.send_file(
            alive.chat_id, CAT_IMG, caption=cat_caption, reply_to=reply_to_id
        )
        await alive.delete()
    else:
        await edit_or_reply(
            alive,
        	f"- 𝚁𝚄𝙽𝚃𝙸𝙼𝙴 :  {uptime}\n"
        f"- 𝚄𝚂𝙴𝚁 :  {mention}\n",
        )


def check_data_base_heal_th():
    # https://stackoverflow.com/a/41961968
    is_database_working = False
    output = "لم يتم تعيين قاعدة بيانات"
    if not Config.DB_URI:
        return is_database_working, output
    from userbot.plugins.sql_helper import SESSION

    try:
        # to check database we will execute raw query
        SESSION.execute("SELECT 1")
    except Exception as e:
        output = f"❌ {str(e)}"
        is_database_working = False
    else:
        output = "- SuccessFully Work"
        is_database_working = True
    return is_database_working, output


CMD_HELP.update(
    {
        "1": "**عدد الملف :** `1`\
      \n\n  •  **الامر : **`.alive` \
      \n  •  **يفعل : **__سيتم عرض حالة البوت__\
      "
    }
)
