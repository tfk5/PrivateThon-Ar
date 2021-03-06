import time
from platform import python_version

from telethon import version

from . import ALIVE_NAME, StartTime, catversion, get_readable_time, mention, reply_id

DEFAULTUSER = ALIVE_NAME or "MarkΒ²"
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
        cat_caption = f"- πππ°πππ :  Working\n"
        cat_caption += f"- ππ΄πππΈπΎπ½ :  7.7.7\n"
        cat_caption += f"- πππ½ππΈπΌπ΄ :  {uptime}\n"
        cat_caption += f"- πππ΄π :  {mention}\n"
        cat_caption += f"- π³π΄π :  [α΄α΄α΄ ](t.me/i_M_5)"
        await alive.client.send_file(
            alive.chat_id, CAT_IMG, caption=cat_caption, reply_to=reply_to_id
        )
        await alive.delete()
    else:
        await edit_or_reply(
            alive,
        	f"- πππ½ππΈπΌπ΄ :  {uptime}\n"
        f"- πππ΄π :  {mention}\n",
        )


def check_data_base_heal_th():
    # https://stackoverflow.com/a/41961968
    is_database_working = False
    output = "ΩΩ ΩΨͺΩ ΨͺΨΉΩΩΩ ΩΨ§ΨΉΨ―Ψ© Ψ¨ΩΨ§ΩΨ§Ψͺ"
    if not Config.DB_URI:
        return is_database_working, output
    from userbot.plugins.sql_helper import SESSION

    try:
        # to check database we will execute raw query
        SESSION.execute("SELECT 1")
    except Exception as e:
        output = f"β {str(e)}"
        is_database_working = False
    else:
        output = "- SuccessFully Work"
        is_database_working = True
    return is_database_working, output


CMD_HELP.update(
    {
        "1": "**ΨΉΨ―Ψ― Ψ§ΩΩΩΩ :** `1`\
      \n\n  β’  **Ψ§ΩΨ§ΩΨ± : **`.alive` \
      \n  β’  **ΩΩΨΉΩ : **__Ψ³ΩΨͺΩ ΨΉΨ±ΨΆ Ψ­Ψ§ΩΨ© Ψ§ΩΨ¨ΩΨͺ__\
      "
    }
)
