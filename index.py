import json
from datetime import datetime, timedelta

from Spreadsheet import Spreadsheet


def get_rasspisanie(spread_name, diapozone_work_days='A1:K32'):
    ss = Spreadsheet('pythonapp-360316.json', spread_name)

    def get_names_current_day(day: list, names, my_index):
        for count, pos in enumerate(day):
            if count == my_index:
                continue
            elif str(pos).isdigit():
                yield names[count]

    work_table = ss.get_work_days(diapozone_work_days)
    names = work_table[0][1:]
    work_table.pop(0)
    dates = ss.get_dates()
    my_index = names.index('Артур')
    for i, day in enumerate(work_table):
        try:
            date = day[0]
            dezhuniy = day[-1]
            my_day = day[my_index + 1]
            if not my_day or my_day == '*':
                yield [dates[i][0], 0, False, []]
            elif dates[i][0].isdigit():
                continue
            elif my_day and dezhuniy == "Артур":
                yield [dates[i][0], 11, True, get_names_current_day(day[1:-1], names, my_index)]
            elif my_day and dezhuniy != "Артур":
                yield [dates[i][0], 11, False, get_names_current_day(day[1:-1], names, my_index)]
        except IndexError:
            continue


def get_text_answer():
    tomorrow = datetime.strftime(datetime.now() + timedelta(days=1), '%d.%m.%Y')
    after_tomorrow = datetime.strftime(datetime.now() + timedelta(days=2), '%d.%m.%Y')
    text = ''

    months = ['Январь', "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
    current_date = datetime.strftime(datetime.now() + timedelta(days=1), '%m %Y').split()
    spread_name = f'{months[int(current_date[0]) - 1]} {current_date[1]}'
    print(spread_name)
    rasspisanie = get_rasspisanie(spread_name=spread_name)
    for day in rasspisanie:
        date, hours, pozdno, tehpods = day
        if tomorrow == date:
            names = ','.join(tehpods)
            if hours == 0:
                text = "Завтра отдыхаешь"
            elif hours > 0 and pozdno and tehpods:
                text = f"Завтра с 11 и с тобой {names}"
            elif hours > 0 and not pozdno and tehpods:
                text = f"Завтра с 8 и с тобой {names}"
            elif hours > 0 and pozdno and not tehpods:
                text = "Завтра с 8 и ты один"
            elif hours > 0 and not pozdno and not tehpods:
                text = "Завтра с 11 и ты один"
            else:
                text = "Завтра что-то непонятное"
            text += '\n'
        if after_tomorrow == date:
            names = ','.join(tehpods)
            if hours == 0:
                text += "Послезавтра отдыхаешь"
            elif hours > 0 and pozdno and tehpods:
                text += f"Послезавтра с 11 и с тобой {names}"
            elif hours > 0 and not pozdno and tehpods:
                text += f"Послезавтра с 8 и с тобой {names}"
            elif hours > 0 and pozdno and not tehpods:
                text += "Послезавтра с 8 и ты один"
            elif hours > 0 and not pozdno and not tehpods:
                text += "Послезавтра с 11 и ты один"
            else:
                text += "Послезавтра что-то непонятное"
    return text


def handler(event, context):
    response = {
        "version": event["version"],
        "session": event["session"],
        "response": {
            "end_session": True
        }
    }

    message = event["request"]["original_utterance"].lower()
    # if event["session"]["new"]:
    #    text = get_text_answer()
    #    response["response"]["text"] = text
    if message in ['работы', 'на 2 дня', 'расписание работы', 'работаю', "работает"]:
        text = get_text_answer()
        response["response"]["text"] = text
    return json.dumps(response)


