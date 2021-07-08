# corona virus stats for catuserbot
from covid import Covid

from . import covidindia


@bot.on(admin_cmd(pattern="covid(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="covid(?: |$)(.*)", allow_sudo=True))
async def corona(event):
    if event.pattern_match.group(1):
        country = (event.pattern_match.group(1)).title()
    else:
        country = "World"
    catevent = await edit_or_reply(event, "`جـاري جلب معلـومات كـورنا عـن هذا البـلد 𖠕...`")
    covid = Covid(source="worldometers")
    try:
        country_data = covid.get_status_by_country_name(country)
    except ValueError:
        country_data = ""
    if country_data:
        hmm1 = country_data["confirmed"] + country_data["new_cases"]
        hmm2 = country_data["deaths"] + country_data["new_deaths"]
        data = ""
        data += f"\n⚠️ الحالات المؤكدة   : <code>{hmm1}</code>"
        data += f"\n😔 النشطة           : <code>{country_data['active']}</code>"
        data += f"\n⚰️ الميتين         : <code>{hmm2}</code>"
        data += f"\n🤕 حالات الحرجة          : <code>{country_data['critical']}</code>"
        data += f"\n😊 المتعافي   : <code>{country_data['recovered']}</code>"
        data += f"\n💉 مجموع الاختبارات    : <code>{country_data['total_tests']}</code>"
        data += f"\n🥺 حالات جديدة   : <code>{country_data['new_cases']}</code>"
        data += f"\n😟 الموتى الجدد : <code>{country_data['new_deaths']}</code>"
        await catevent.edit(
            "<b>Corona Virus Info of {}:\n{}</b>".format(country, data),
            parse_mode="html",
        )
    else:
        data = await covidindia(country)
        if data:
            cat1 = int(data["new_positive"]) - int(data["positive"])
            cat2 = int(data["new_death"]) - int(data["death"])
            cat3 = int(data["new_cured"]) - int(data["cured"])
            result = f"<b>Corona virus info of {data['state_name']}\
                \n\n⚠️ الحالات المؤكدة   : <code>{data['new_positive']}</code>\
                \n😔 النشطة           : <code>{data['new_active']}</code>\
                \n⚰️ الميتين         : <code>{data['new_death']}</code>\
                \n😊 حالات الحرجة   : <code>{data['new_cured']}</code>\
                \n🥺 المتعافي   : <code>{cat1}</code>\
                \n😟 الموتى الجدد : <code>{cat2}</code>\
                \n😃 علاجه جديد  : <code>{cat3}</code> </b>"
            await catevent.edit(result, parse_mode="html")
        else:
            await edit_delete(
                catevent,
                "`معلومات عن فيروس كورونا من {} غير متوفر أو غير قادر على الجلب`".format(
                    country
                ),
                5,
            )


CMD_HELP.update(
    {
        "covid": "**Plugin : **`covid`\
        \n\n  •  **Syntax : **`.covid <country name>`\
        \n  •  **Function :** __Get an information about covid-19 data in the given country.__\
        \n\n  •  **Syntax : **`.covid <state name>`\
        \n  •  **Function :** __Get an information about covid-19 data in the given state of India only.__\
        "
    }
)
