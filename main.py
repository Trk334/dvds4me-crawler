import json
import re

import requests
from bs4 import BeautifulSoup


def find_max_url():
    url = 'https://dvds4me.com/collections/latest-titles'
    response = requests.get(url)
    max_url = 0

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        find_meta = soup.find_all()
        for i in find_meta:
            for line in i.text.splitlines():
                if "123…" in line:
                    max_url = int(line.split('123…')[1])
                break

    return max_url


def scrape_dvds4me():
    open('output.txt', 'w')
    if find_max_url() != 0:
        for i in range(find_max_url()):
            if i == 0:
                url = 'https://dvds4me.com/collections/latest-titles'
            else:
                url = 'https://dvds4me.com/collections/latest-titles' + "?page={}".format(i)

            response = requests.get(url)

            if response.status_code == 200:

                # find meta
                meta = ""
                soup = BeautifulSoup(response.text, 'html.parser')
                find_meta = soup.find_all(string=re.compile("var meta ="))
                for line in find_meta[0].splitlines():
                    if "var meta =" in line:
                        meta = line
                        break

                json_str = meta.split('=')[1].strip().rstrip(';')
                data = json.loads(json_str)

                for i in range(len(data['products'])):

                    sku = data['products'][i]['variants'][0]['sku']
                    price = data['products'][i]['variants'][0]['price']
                    parts = data['products'][i]['variants'][0]['name'].split('(')
                    if len(parts) == 1:
                        title = data['products'][i]['variants'][0]['name'].split(' DVD')[0]
                        format = "DVD"
                    else:
                        title = parts[0].strip()
                        format = parts[1].split(',')[0].strip()

                    with open('output.txt', 'a') as file:
                        file.write("Title of DVD: {},\n".format(title))
                        file.write("Cost USD: {},\n".format(float(price / 100)))
                        file.write("UPC: {},\n".format(sku))
                        file.write("Format: {},\n".format(format))

                    print("Title of DVD:", title)
                    print("Cost USD:", float(price / 100))
                    print("UPC:", sku)
                    print("Format:", format)



        else:
            print('Failed to retrieve webpage.')
    else:
        print('Failed to retrieve webpage.')


if __name__ == '__main__':
    scrape_dvds4me()
