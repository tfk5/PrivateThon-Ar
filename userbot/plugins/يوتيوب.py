import asyncio
import os
import re
import time
from datetime import datetime
from pathlib import Path

from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import DocumentAttributeAudio
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

from . import hmention, progress, ytsearch


@bot.on(admin_cmd(pattern="yt(a|v)(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="yt(a|v)(?: |$)(.*)", allow_sudo=True))
async def download_video(v_url):
    """ For .ytdl command, download media from YouTube and many other sites. """
    url = v_url.pattern_match.group(2)
    if not url:
        rmsg = await v_url.get_reply_message()
        myString = rmsg.text
        url = re.search("(?P<url>https?://[^\s]+)", myString).group("url")
    if not url:
        await edit_or_reply(v_url, " ما الذي من المفترض أن أجده ؟  أعط الرابـط")
        return
    ytype = v_url.pattern_match.group(1).lower()
    v_url = await edit_or_reply(v_url, "**إحضار البيانات ، يرجى الانتظار...**")
    reply_to_id = await reply_id(v_url)
    if ytype == "a":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        video = False
        song = True
    elif ytype == "v":
        opts = {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
            "outtmpl": "%(id)s.mp4",
            "logtostderr": False,
            "quiet": True,
        }
        song = False
        video = True
    try:
        await v_url.edit("**  إحضار البيانـات ، يرجى الانتـظار **")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except DownloadError as DE:
        await v_url.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await v_url.edit(" محـتوى التنزيـل كان قصيرًا جدًا جـاري الارسـال")
        return
    except GeoRestrictedError:
        await v_url.edit(
            "** الفيديـو غير متـاح من موقـعك الجغرافـي بسبب القيود الجغرافية التي يفرضهـا موقع الويب**"
        )
        return
    except MaxDownloadsReached:
        await v_url.edit("** تم الوصـول إلى الحـد الأقـصى لعدد التـنزيـلات**")
        return
    except PostProcessingError:
        await v_url.edit("** حـدث خـطأ أثناء معالجـة ما بعد**")
        return
    except UnavailableVideoError:
        await v_url.edit("** الوسـائـط غير متوفـرة بالتنسـيق المطـلوب**")
        return
    except XAttrMetadataError as XAME:
        await v_url.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await v_url.edit("** حـدث خـطأ أثناء معالجـة ما بعد**")
        return
    except Exception as e:
        await v_url.edit(f"{str(type(e)): {str(e)}}")
        return
    c_time = time.time()
    catthumb = Path(f"{ytdl_data['id']}.jpg")
    if not os.path.exists(catthumb):
        catthumb = Path(f"{ytdl_data['id']}.webp")
    if not os.path.exists(catthumb):
        catthumb = None
    if song:
        await v_url.edit(
            f"** التحضـير لتحـميل الأغنـية**:`\
        \n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*"
        )
        await v_url.client.send_file(
            v_url.chat_id,
            f"{ytdl_data['id']}.mp3",
            supports_streaming=True,
            thumb=catthumb,
            reply_to=reply_to_id,
            attributes=[
                DocumentAttributeAudio(
                    duration=int(ytdl_data["duration"]),
                    title=str(ytdl_data["title"]),
                    performer=str(ytdl_data["uploader"]),
                )
            ],
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d, t, v_url, c_time, " جــاري تحميـل ..", f"{ytdl_data['title']}.mp3"
                )
            ),
        )
        os.remove(f"{ytdl_data['id']}.mp3")
    elif video:
        await v_url.edit(
            f"** التحـضير لتحميـل الفيـديو:**\
        \n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*"
        )
        await v_url.client.send_file(
            v_url.chat_id,
            f"{ytdl_data['id']}.mp4",
            reply_to=reply_to_id,
            supports_streaming=True,
            caption=ytdl_data["title"],
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d, t, v_url, c_time, " ... جـاري تحميل ..", f"{ytdl_data['title']}.mp4"
                )
            ),
        )
        os.remove(f"{ytdl_data['id']}.mp4")
    if catthumb:
        os.remove(catthumb)
    await v_url.delete()


@bot.on(admin_cmd(pattern="yts(?: |$)(\d*)? ?(.*)", command="yts"))
@bot.on(sudo_cmd(pattern="yts(?: |$)(\d*)? ?(.*)", command="yts", allow_sudo=True))
async def yt_search(event):
    if event.fwd_from:
        return
    if event.is_reply and not event.pattern_match.group(2):
        query = await event.get_reply_message()
        query = str(query.message)
    else:
        query = str(event.pattern_match.group(2))
    if not query:
        return await edit_delete(
            event, "** الـرد على رسالـة أو تمريـر استعـلام للبحـث**"
        )
    video_q = await edit_or_reply(event, "** جـاري البـحث...**")
    if event.pattern_match.group(1) != "":
        lim = int(event.pattern_match.group(1))
        if lim <= 0:
            lim = int(10)
    else:
        lim = int(10)
    try:
        full_response = await ytsearch(query, limit=lim)
    except Exception as e:
        return await edit_delete(video_q, str(e), time=10, parse_mode=parse_pre)
    reply_text = f"**•  Search Query:**\n`{query}`\n\n**•  Results:**\n{full_response}"
    await edit_or_reply(video_q, reply_text)


@bot.on(admin_cmd(pattern="insta (.*)"))
@bot.on(sudo_cmd(pattern="insta (.*)", allow_sudo=True))
async def kakashi(event):
    if event.fwd_from:
        return
    chat = "@instasavegrambot"
    link = event.pattern_match.group(1)
    if "www.instagram.com" not in link:
        await edit_or_reply(
            event, "` I need a Instagram link to download it's Video...`(*_*)"
        )
    else:
        start = datetime.now()
        catevent = await edit_or_reply(event, "**Downloading.....**")
    async with event.client.conversation(chat) as conv:
        try:
            msg_start = await conv.send_message("/start")
            response = await conv.get_response()
            msg = await conv.send_message(link)
            video = await conv.get_response()
            details = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await catevent.edit("**Error:** `unblock` @instasavegrambot `and retry!`")
            return
        await catevent.delete()
        cat = await event.client.send_file(
            event.chat_id,
            video,
        )
        end = datetime.now()
        ms = (end - start).seconds
        await cat.edit(
            f"<b><i>➥ Video uploaded in {ms} seconds.</i></b>\n<b><i>➥ Uploaded by :- {hmention}</i></b>",
            parse_mode="html",
        )
    await event.client.delete_messages(
        conv.chat_id, [msg_start.id, response.id, msg.id, video.id, details.id]
    )


CMD_HELP.update(
    {
        "تحميل رابط": "**Plugin :** `تحميل رابط`\
    \n\n  •  **Syntax :** `.yta link`\
    \n  •  **Function : **__downloads the audio from the given link(Suports the all sites which support youtube-dl)__\
    \n\n  •  **Syntax : **`.ytv link`\
    \n  •  **Function : **__downloads the video from the given link(Suports the all sites which support youtube-dl)__\
    \n\n  •  **Syntax : **`.yts query`/`.yts count query`\
    \n  •  **Function : **__Fetches youtube search results with views and duration with required no of count results by default it fetches 10 results__\
    \n\n  •  **Syntax : **`.insta` <link>\
    \n  •  **Function : **__Downloads the video from the given instagram link__\
    "
    }
)
