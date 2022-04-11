from requests_html import HTMLSession

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
    display(html, base_selector, selectors)


def display(html, base_selector, selectors):
    for param_selector in selectors:
        path = base_selector + param_selector
        response = html.xpath(path)
        for data in response:
            print('{:<15}'.format(data.strip()), end='')
        print()


def get_html():
    session = HTMLSession()
    response = session.get("https://www.doviz.com")
    return response.html


if __name__ == '__main__':
    main()
