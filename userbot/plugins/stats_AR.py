import base64
import time

from telethon.tl.custom import Dialog
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import Channel, Chat, User

# =========================================================== #
#                           STRINGS                           #
# =========================================================== #
STAT_INDICATION = "`جـاري جمع معـلوماتك 𖠕`"
CHANNELS_STR = "**قائمة القنوات التي أنت فيها موجودون هنا **\n\n"
CHANNELS_ADMINSTR = "**قائمة القنوات التي تديرها هنا **\n\n"
CHANNELS_OWNERSTR = "**قائمة القنوات التي تمتلك فيها هنا **\n\n"
GROUPS_STR = "**قائمة المجموعات التي أنت فيها موجود هنا **\n\n"
GROUPS_ADMINSTR = "**قائمة المجموعات التي تكون مسؤولاً فيها هنا **\n\n"
GROUPS_OWNERSTR = "**قائمة المجموعات التي تمتلك فيها هنا **\n\n"
# =========================================================== #
#                                                             #
# =========================================================== #


@bot.on(admin_cmd(pattern="stat$"))
@bot.on(sudo_cmd(pattern="stat$", allow_sudo=True))
async def stats(event):
    cat = await edit_or_reply(event, STAT_INDICATION)
    start_time = time.time()
    private_chats = 0
    bots = 0
    groups = 0
    broadcast_channels = 0
    admin_in_groups = 0
    creator_in_groups = 0
    admin_in_broadcast_channels = 0
    creator_in_channels = 0
    unread_mentions = 0
    unread = 0
    dialog: Dialog
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            broadcast_channels += 1
            if entity.creator or entity.admin_rights:
                admin_in_broadcast_channels += 1
            if entity.creator:
                creator_in_channels += 1
        elif (
            isinstance(entity, Channel)
            and entity.megagroup
            or not isinstance(entity, Channel)
            and not isinstance(entity, User)
            and isinstance(entity, Chat)
        ):
            groups += 1
            if entity.creator or entity.admin_rights:
                admin_in_groups += 1
            if entity.creator:
                creator_in_groups += 1
        elif not isinstance(entity, Channel) and isinstance(entity, User):
            private_chats += 1
            if entity.bot:
                bots += 1
        unread_mentions += dialog.unread_mentions_count
        unread += dialog.unread_count
    stop_time = time.time() - start_time
    full_name = inline_mention(await event.client.get_me())
    response = f"𖠕 **مـعلومات حـول 🔜 {full_name}** \n\n"
    response += f"**الـدردشات الخـاصة:** {private_chats} \n"
    response += f"   𖠕 `المـستخدمون: {private_chats - bots}` \n"
    response += f"   𖠕 `عـدد البـوتات: {bots}` \n"
    response += f"**المجـموعات:** {groups} \n"
    response += f"**القـنوات:** {broadcast_channels} \n"
    response += f"**الأدمنـية في المـجموعات:** {admin_in_groups} \n"
    response += f"   𖠕 `المنشـئ: {creator_in_groups}` \n"
    response += f"   𖠕 `حـقوق المسؤول: {admin_in_groups - creator_in_groups}` \n"
    response += f"**ادمـن في القنـوات:** {admin_in_broadcast_channels} \n"
    response += f"   𖠕 `المنشـئ: {creator_in_channels}` \n"
    response += (
        f"   𖠕 `حـقوق المسـؤول: {admin_in_broadcast_channels - creator_in_channels}` \n"
    )
    response += f"**الغيـر مقروئـه:** {unread} \n"
    response += f"**التـاكات الغـير مقـروئة:** {unread_mentions} \n\n"
    response += f"𖠕 عدد الـدقائق : {stop_time:.02f}s \n"
    await cat.edit(response)


CMD_HELP.update(
    {
        "stats": "**Plugin : **`stats`\
    \n\n  •  **Syntax : **`.stat`\
    \n  •  **Function : **__Shows you the count of  your groups, channels, private chats...etc__\
    \n\n  •  **Syntax : **`.stat (g|ga|go)`\
    \n  •  **Function : **__Shows you the list of all groups  in which you are if you use g , all groups in which you are admin if you use ga and all groups created by you if you use go__\
    \n\n  •  **Syntax : **`.stat (c|ca|co)`\
    \n  •  **Function : **__Shows you the list of all channels in which you are if you use c , all channels in which you are admin if you use ca and all channels created by you if you use co__\
    \n\n  •  **Syntax : **`.ustat (reply/userid/username)`\
    \n  •  **Function : **__Shows the list of public groups of that paticular user__\
    "
    }
)
