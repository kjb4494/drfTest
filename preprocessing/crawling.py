import requests
from bs4 import BeautifulSoup
from preprocessing.enums import Modifiers


def get_modifier_list_from_eu4_wiki(with_default_value=False):
    req = requests.get('https://eu4.paradoxwikis.com/Modifier_list')

    if not req.ok:
        raise ConnectionError

    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    modifier_tables = soup.find_all(
        'table',
        {'class': ['wikitable', 'sortable', 'jquery-tablesorter']}
    )[:len(Modifiers)]

    modifier_list = []

    for idx, modifier_table in enumerate(modifier_tables):
        trs = modifier_table.find_all('tr')
        tr_th, tr_tds = trs[0], trs[1:]
        modifier_names = [th.text.strip().lower().replace(' ', '_') for th in tr_th.find_all('th')]
        for tr_td in tr_tds:
            tds = tr_td.find_all('td')
            modifier_values = [td.text.strip().replace('<', '&lt;').replace('>', '&gt;') for td in tds]
            modifier = {
                'm_type': Modifiers(idx).name
            }
            for i in range(len(modifier_names)):
                modifier[modifier_names[i]] = modifier_values[i]
            if with_default_value:
                try:
                    modifier['default_value'] = float(modifier['example'].split()[-1])
                except:
                    modifier['default_value'] = 1.0
            modifier_list.append(modifier)
    return modifier_list


def get_country_list_from_eu4_wiki(with_img_url=False):
    req = requests.get('https://eu4.paradoxwikis.com/Countries')

    if not req.ok:
        raise ConnectionError

    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    country_table = soup.find_all(
        'table',
        {'class': ['wikitable', 'sortable', 'jquery-tablesorter']}
    )[0]
    trs = country_table.find_all('tr')
    tr_tds = trs[1:]
    image_src_base = 'https://eu4.paradoxwikis.com'
    country_list = []
    for tr_td in tr_tds:
        tds = tr_td.find_all('td')
        _, raw_country_info, raw_country_tag, _, _ = tds
        country_name = raw_country_info.find_all('a')[1].text.strip()
        country_tag = raw_country_tag.text.strip()
        img_src = image_src_base + raw_country_info.a.img.attrs['src']
        img_name = img_src.split('/')[-1]
        country = {
            'country_name': country_name,
            'country_tag': country_tag,
            'img_name': img_name
        }
        if with_img_url:
            country['img_src'] = img_src
        country_list.append(country)
    return country_list


def code_test():
    from pprint import pprint as prt
    # prt(get_modifier_list_from_eu4_wiki())
    # prt(get_modifier_list_from_eu4_wiki(with_default_value=True))
    prt(get_country_list_from_eu4_wiki())
    prt(get_country_list_from_eu4_wiki(with_img_url=True))


if __name__ == '__main__':
    code_test()
