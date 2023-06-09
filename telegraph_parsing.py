import requests
from bs4 import BeautifulSoup


url_base = 'https://telegra.ph/'
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
years = ['21', '22', '23']
key_words = ['new']

valid_urls = []


def check_spam(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    meta_description = soup.select_one('meta[property="og:description"]')['content']

    post_data = meta_description.split()
    post_author = soup.select_one('meta[property="article:author"]')['content']

    # list of authors you'd like to ignore
    block_authors = [""]

    # list of some same text which could be in spam posts
    block = [""]

    length = len(meta_description)

    # empty articles
    if 1 < length < 10:
        return 0

    # Могут быть только изображения, что интересно
    if not post_data:
        return 1

    # deleting just first element (по шаблону спам там)
    for b in block:
        if post_data[0] == b:
            return 0

    # те кто нас задолбал
    for a in block_authors:
        if post_author == a:
            return 0
    return 1


def main() -> list:

    for word in key_words:
        for year in years:
            for month in months:
                url = f'{url_base}{word}-{month}-{year}'
                response = requests.get(url)
                code = response.status_code
                if code == 200:

                    if check_spam(response):
                        print('VALID!', url)
                        valid_urls.append(url)

                    # When article name same telegraph url look like:
                    # https://telegra.ph/post-01-21-2, https://telegra.ph/post-01-21-3 etc
                    i = 2
                    url2 = f'{url}-{i}'
                    response = requests.get(url2)
                    code = response.status_code
                    while code == 200:

                        i += 1
                        if check_spam(response):
                            print('VALID!', url2)
                            valid_urls.append(url2)

                        url2 = f'{url}-{i}'
                        response = requests.get(url2)
                        code = response.status_code
    file_name = 'valid_urls'
    with open(file_name, 'w') as f:
        info = ('\n').join(valid_urls)
        f.write(info)

    print('DONE')
    return valid_urls

urls = main()

