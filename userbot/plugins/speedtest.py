"""Check your internet speed powered by speedtest.net
Syntax: .speedtest
Available Options: image, file, text"""
from datetime import datetime

import speedtest

from . import reply_id


@bot.on(admin_cmd(pattern="speedtest ?(.*)"))
@bot.on(sudo_cmd(pattern="speedtest ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    as_text = False
    as_document = False
    if input_str == "image":
        as_document = False
    elif input_str == "file":
        as_document = True
    elif input_str == "text":
        as_text = True
    catevent = await edit_or_reply(
        event, "`يـرجى الانتضـار لجـلب سـرعة الانـترنيت لديـك 📶`"
    )
    start = datetime.now()
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    response = s.results.dict()
    download_speed = response.get("download")
    upload_speed = response.get("upload")
    ping_time = response.get("ping")
    client_infos = response.get("client")
    i_s_p = client_infos.get("isp")
    i_s_p_rating = client_infos.get("isprating")
    reply_msg_id = await reply_id(event)
    try:
        response = s.results.share()
        speedtest_image = response
        if as_text:
            await catevent.edit(
                """`سـرعة الانـترنيت لديـك هيـة {} بالـثانية 📳`

`الـتحميل : {}`
`الـرفع : {}`
`الـبنك : {}`
`مزود خدمة الإنترنت : {}`
`تقييم ISP : {}`""".format(
                    ms,
                    convert_from_bytes(download_speed),
                    convert_from_bytes(upload_speed),
                    ping_time,
                    i_s_p,
                    i_s_p_rating,
                )
            )
        else:
            await event.client.send_file(
                event.chat_id,
                speedtest_image,
                caption="**سـرعة الانتـرنيت ** اكتـملت  {} ثانيـة 📳".format(ms),
                force_document=as_document,
                reply_to=reply_msg_id,
                allow_cache=False,
            )
            await event.delete()
    except Exception as exc:
        await catevent.edit(
            """**سـرعة الانتـرنيت** اكـتمل خـلال {} ثانـية
الـتحميل : {}
الـرفع : {}
البنـك : {}

__With the Following ERRORs__
{}""".format(
                ms,
                convert_from_bytes(download_speed),
                convert_from_bytes(upload_speed),
                ping_time,
                str(exc),
            )
        )


def convert_from_bytes(size):
    power = 2 ** 10
    n = 0
    units = {0: "", 1: "kilobytes", 2: "megabytes", 3: "gigabytes", 4: "terabytes"}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"


CMD_HELP.update(
    {
        "speedtest": """**Plugin : **`speedtest`

  •  **Syntax : **`.speedtest text/image/file`
  •  **function : **__Shows your server speed in the given format if nothing is given then shows as image__"""
    }
)
