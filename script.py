from requests_html import HTMLSession
from datetime import datetime, timedelta, date
from threading import Timer
import time, json


def main():
    json_data = {'daily_rates':[]}

    while True:
        now = datetime.now()
        run_at = now + timedelta(hours=0.01)
        delay = (run_at - now).total_seconds()
        Timer(delay, run(json_data)).start()
        time.sleep(120)


def run(json_data):
    update_json(json_data)
    output_json(json_data)


def update_json(json_data):
    base_selector = '/html/body/header/div[@class="header-secondary"]/div[@class="header-container"]' \
                    '/div[@class="market-data"]/div[@class="item"]/a '
    name_selector = '/span[@class="name"]/text()'
    value_selector = '/span[@class="value"]/text()'
    change_rate_selector = '/div[contains(@class, "change-rate")]/text()'
    change_amount_selector = '/div[@class="change-amount"]/span/text()'

    selectors = {'name' : name_selector, 
    'value' : value_selector, 
    'change-rate' : change_rate_selector, 
    'change-amount' : change_amount_selector}

    html = get_html()
    daily_data = get_daily_json(html, base_selector, selectors)
    json_data['daily_rates'].append(daily_data) 


def get_daily_json(html, base_selector, selectors):
    json = {}
    today = date.today()
    today_date = today.strftime("%d-%b-%Y")
    json['date'] = today_date
    
    names = html.xpath(base_selector + selectors['name'])
    values = html.xpath(base_selector + selectors['value'])
    change_rates = html.xpath(base_selector + selectors['change-rate'])
    change_amounts = html.xpath(base_selector + selectors['change-amount'])

    data_list = []
    for i in range(len(names)):
        data_list.append({'name' : names[i].strip(), 
        'value': values[i].strip(), 
        'change-rate' : change_rates[i].strip(), 
        'change-amount' : change_amounts[i].strip()})
    json['data'] = data_list
    return json


def output_json(json_data):
    json_string = json.dumps(json_data, indent=4, ensure_ascii=False)
    with open('daily_currency.json', 'w') as outfile:
        outfile.write(json_string)


def get_html():
    session = HTMLSession()
    response = session.get("https://www.doviz.com")
    return response.html


if __name__ == '__main__':
    main()
