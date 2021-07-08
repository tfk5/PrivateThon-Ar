from geopy.geocoders import Nominatim
from telethon.tl import types

from userbot import CMD_HELP
from userbot.utils import sudo_cmd


@bot.on(admin_cmd(pattern="gps ?(.*)"))
async def gps(event):
    if event.fwd_from:
        return
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    input_str = event.pattern_match.group(1)

    if not input_str:
        return await event.edit("ماذا يجب أن أجد أعطني الموقع. 𖠕")

    await event.edit("تـم العـثور عـلى")

    geolocator = Nominatim(user_agent="catuserbot")
    geoloc = geolocator.geocode(input_str)

    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        await reply_to_id.reply(
            input_str, file=types.InputMediaGeoPoint(types.InputGeoPoint(lat, lon))
        )
        await event.delete()
    else:
        await event.edit("عـذرا لـم أجـد المـكان المـحدد 𖠕")


@bot.on(sudo_cmd(pattern="gps ?(.*)", allow_sudo=True))
async def gps(event):
    if event.fwd_from:
        return
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    input_str = event.pattern_match.group(1)

    if not input_str:
        return await event.reply("ماذا يجب أن أجد أعطني الموقع. 𖠕")

    cat = await event.reply("تـم العـثور عـلى 𖠕")

    geolocator = Nominatim(user_agent="catuserbot")
    geoloc = geolocator.geocode(input_str)

    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        await reply_to_id.reply(
            input_str, file=types.InputMediaGeoPoint(types.InputGeoPoint(lat, lon))
        )
        await cat.delete()
    else:
        await cat.edit("عـذرا لـم أجـد 𖠕")


CMD_HELP.update(
    {
        "gps": "`.gps` <location name> :\
      \nUSAGE: sends you a map with the given location as pin \
      "
    }
)
