from asyncio import sleep

from googletrans import LANGUAGES, Translator

from . import BOTLOG, BOTLOG_CHATID, deEmojify
from .sql_helper.globals import addgvar, gvarstatus


@bot.on(admin_cmd(pattern="tl (.*)"))
@bot.on(sudo_cmd(pattern="tl (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if "trim" in event.raw_text:
        return
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "en"
    elif ";" in input_str:
        lan, text = input_str.split(";")
    else:
        await edit_delete(event, "يرجـى الـرد على الـرسالة للترجمة", time=5)
        return
    text = deEmojify(text.strip())
    lan = lan.strip()
    Translator()
    try:
        translated = await getTranslate(text, dest=lan)
        after_tr_text = translated.text
        output_str = f"الـترجمـة لـ {LANGUAGES[translated.src].title()} إلـى {LANGUAGES[lan].title()}:\
                \n`{after_tr_text}`"
        await edit_or_reply(event, output_str)
    except Exception as exc:
        await edit_delete(event, str(exc), time=5)



@bot.on(admin_cmd(pattern="lang trt (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="lang trt (.*)", allow_sudo=True))
async def lang(value):
    if value.fwd_from:
        return
    arg = value.pattern_match.group(1).lower()
    if arg in LANGUAGES:
        addgvar("TRT_LANG", arg)
        LANG = LANGUAGES[arg]
    else:
        await edit_or_reply(
            value,
            f"`Invalid Language code !!`\n`Available language codes for TRT`:\n\n`{LANGUAGES}`",
        )
        return
    await edit_or_reply(value, f"`Language for Translator changed to {LANG.title()}.`")
    if BOTLOG:
        await value.client.send_message(
            BOTLOG_CHATID, f"`Language for Translator changed to {LANG.title()}.`"
        )


# https://github.com/ssut/py-googletrans/issues/234#issuecomment-722379788
async def getTranslate(text, **kwargs):
    translator = Translator()
    result = None
    for _ in range(10):
        try:
            result = translator.translate(text, **kwargs)
        except Exception:
            translator = Translator()
            await sleep(0.1)
    return result


CMD_HELP.update(
    {
        "translate": "**Plugin :** `translate`\
         \n\n**•  Syntax : **`.tl LanguageCode <text/reply>`\
         \n**•  Function : **__Translates given language to destination language. For <text> use .tl LanguageCode ; <text>__\
         \n\n**•  Syntax : **`.trt <Reply/text>`\
         \n**•  Function : **__It will translate your messege__\
         \n\n**•  Syntax : **`.lang trt LanguageCode`\
         \n**•  Function : **__It will set default langaugeCode for __**trt**__ command__\
         \n\n**•  Check here ** [Language codes](https://telegra.ph/Language-codes-11-01)\
        "
    }
)
