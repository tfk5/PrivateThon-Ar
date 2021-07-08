import os

from telethon.errors.rpcerrorlist import UsernameOccupiedError
from telethon.tl import functions
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest
from telethon.tl.functions.photos import DeletePhotosRequest, GetUserPhotosRequest
from telethon.tl.types import Channel, Chat, InputPhoto, User

# ====================== CONSTANT ===============================
INVALID_MEDIA = "امتداد الكيان الإعلامي غير صالح."
USERNAME_SUCCESS = "تم تغيير اسم المستخدم الخاص بك بنجاح ."
USERNAME_TAKEN = "أسم المستخدم مأخوذ مسبقا ."
# ===============================================================


@bot.on(admin_cmd(outgoing=True, pattern="username (.*)"))
async def update_username(username):
    """ For .username command, set a new username in Telegram. """
    newusername = username.pattern_match.group(1)
    try:
        await username.client(UpdateUsernameRequest(newusername))
        await username.edit(USERNAME_SUCCESS)
    except UsernameOccupiedError:
        await username.edit(USERNAME_TAKEN)


@bot.on(admin_cmd(outgoing=True, pattern="count$"))
async def count(event):
    """ For .count command, get profile stats. """
    u = 0
    g = 0
    c = 0
    bc = 0
    b = 0
    result = ""
    await event.edit("جـاري جلـب الاحصـائيات ..")
    dialogs = await event.client.get_dialogs(limit=None, ignore_migrated=True)
    for d in dialogs:
        currrent_entity = d.entity
        if isinstance(currrent_entity, User):
            if currrent_entity.bot:
                b += 1
            else:
                u += 1
        elif isinstance(currrent_entity, Chat):
            g += 1
        elif isinstance(currrent_entity, Channel):
            if currrent_entity.broadcast:
                bc += 1
            else:
                c += 1
        else:
            print(d)

    result += f"المـستخدمين :\t{u}\n"
    result += f"المجمـوعـات :\t{g}\n"
    result += f"المجـموعـات المـطورة :\t{c}\n"
    result += f"الـقنوات :\t{bc}\n"
    result += f"الـبوتات :\t{b}"

    await event.edit(result)



@bot.on(admin_cmd(pattern="myusernames$"))
async def _(event):
    if event.fwd_from:
        return
    result = await event.client(GetAdminedPublicChannelsRequest())
    output_str = "".join(
        f"- {channel_obj.title} @{channel_obj.username} \n"
        for channel_obj in result.chats
    )

    await event.edit(output_str)


CMD_HELP.update(
    {
        "profile": "Plugin : profile\
        \n\n•  Syntax : .username <new_username>\
        \n•  Function : __ Changes your Telegram username.__\
        \n\n•  Syntax : .pname <name>\
        \n•  Function : __ Changes your Telegram name.(First and last name will get split by the first space)__\
        \n\n•  Syntax : .ppic\
        \n•  Function : __ Reply with .setpfp or .ppic to an image to change your Telegram profie picture.__\
        \n\n•  Syntax : .pbio <new_bio>\
        \n•  Function : __ Changes your Telegram bio.__\
        \n\n•  Syntax : .delpfp or .delpfp <number>/<all>\
        \n•  Function : __ Deletes your Telegram profile picture(s).__\
        \n\n•  Syntax : .myusernames\
        \n•  Function : __ Shows usernames of your created channels and groups __\
        \n\n•  Syntax : .count\
        \n•  Function : __ Counts your groups, chats, bots etc...__"
    }
)
