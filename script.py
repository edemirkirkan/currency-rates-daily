from requests_html import HTMLSession
from datetime import date
import json


def main():
    run()


def run():
    base_selector = '/html/body/header/div[@class="header-secondary"]/div[@class="header-container"]' \
                    '/div[@class="market-data"]/div[@class="item"]/a '
    name_selector = '/span[@class="name"]/text()'
    value_selector = '/span[@class="value"]/text()'
    change_rate_selector = '/div[contains(@class, "change-rate")]/text()'
    change_amount_selector = '/div[@class="change-amount"]/span/text()'

    selectors = {'name': name_selector,
                 'value': value_selector,
                 'change-rate': change_rate_selector,
                 'change-amount': change_amount_selector}

    html = get_html()
    daily_data = get_daily_data(html, base_selector, selectors)
    write_json(daily_data)


def get_daily_data(html, base_selector, selectors):
    daily_data = {}
    today = date.today()
    today_date = today.strftime("%d-%b-%Y")
    daily_data['date'] = today_date

    names = html.xpath(base_selector + selectors['name'])
    values = html.xpath(base_selector + selectors['value'])
    change_rates = html.xpath(base_selector + selectors['change-rate'])
    change_amounts = html.xpath(base_selector + selectors['change-amount'])

    data_list = []
    for i in range(len(names)):
        data_list.append({'name': names[i].strip(),
                          'value': values[i].strip(),
                          'change-rate': change_rates[i].strip(),
                          'change-amount': change_amounts[i].strip()})
    daily_data['data'] = data_list
    return daily_data


def json_create():
    with open(file='daily_currency.json', mode='w') as outfile:
        json.dump([], outfile)


def write_json(json_data):
    with open('daily_currency.json', 'ab+') as file:
        file.seek(0, 2)
        if not file.tell():
            file.write(json.dumps([json_data], indent=4, ensure_ascii=False).encode())
        else:
            file.seek(-2, 2)
            file.truncate()
            json_string = ',\n' + json.dumps(json_data, indent=4, ensure_ascii=False)
            json_string = '\t'.join(json_string.splitlines(True)) + '\n]'
            file.write(json_string.encode())


def get_html():
    session = HTMLSession()
    response = session.get("https://www.doviz.com")
    return response.html


if __name__ == '__main__':
    main()
