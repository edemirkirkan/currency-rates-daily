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

    selectors = [name_selector, value_selector, change_rate_selector, change_amount_selector]

    html = get_html()
    daily_data = get_daily_data(html, base_selector, selectors)
    write_json(daily_data)


def get_daily_data(html, base_selector, selectors):
    params = [html.xpath(base_selector + param_selector) for param_selector in selectors]

    currency_data = [{'name': name.strip(),
                      'value': value.strip(),
                      'change-rate': change_rate.strip(),
                      'change-amount': change_amount.strip()}
                     for name, value, change_rate, change_amount in zip(*params)]

    today = date.today().strftime("%d-%b-%Y")
    daily_data = {'date': today, 'data': currency_data}
    return daily_data


def write_json(json_data):
    with open('daily_currency.json', 'ab+') as file:
        file.seek(0, 2)
        if not file.tell():
            file.write(json.dumps([json_data], indent=4, ensure_ascii=False).encode())
            return

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
