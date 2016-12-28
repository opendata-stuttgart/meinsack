from bs4 import BeautifulSoup
import requests
import re


def get_districts_stuttgart():
    url = 'http://onlinestreet.de/strassen/in-Stuttgart.html'
    data = requests.get(url).content
    soup = BeautifulSoup(data, 'html.parser')
    for table in soup.findAll('table'):
        if 'blz' in table.get("class"):
            for index, tr in enumerate(table.findAll('tr')):
                if index == 0:
                    continue
                yield tr
            break


def extract_district_from_tr(tr):
    data = list(tr.children)
    return {
        'name': data[0].a.text,
        'url_onlinestreet': data[0].a['href'],
        'city': 'Stuttgart',
        'number_of_streets': data[1].text
    }


def add_district_to_database(data):
    from main.models import District
    district, created = District.objects.get_or_create(**data)
    return district


def get_streets_from_district(district):
    url = district.url_onlinestreet
    data = requests.get(url).text

    soup = BeautifulSoup(data, 'html.parser')
    for table in soup.findAll('table'):
        if 'strassen' in table.get('class'):
            for index, tr in enumerate(table.findAll('tr')):
                if index == 0:
                    continue
                yield tr


def normalize_street(street):
    if street.endswith('tr.'):
        street = street[:-1] + "aße"
    return street


def extract_street_from_tr(tr):
    data = list(tr.children)
    p = re.compile(r'(?P<street>.*)\s+(?P<zipcode>[0-9]{5})\s+(?P<city>.*)')
    x = re.search(p, data[0].a.text)
    if not x:
        return None
    return {
        'url_onlinestreet': data[0].a['href'],
        'name': normalize_street(x.groupdict().get('street')),
        'city': x.groupdict().get('city'),
        'zipcode': x.groupdict().get('zipcode'),
    }


def add_street_to_database(data, district):
    from main.models import Street, ZipCode
    if not data:
        return None
    zipcode = data.pop("zipcode")
    zipcode, created = ZipCode.objects.get_or_create(zipcode=zipcode)
    data["zipcode"] = zipcode
    street, created = Street.objects.get_or_create(district=district, **data)
    return street


def replace_umlauts(string):
    for i, j in (('ß', 'ss'), ('ä', 'ae'), ('ü', 'ue'), ('ö', 'oe')):
        x = string.replace(i, j)
        if x != string:
            yield x


def get_possible_street_variants(street_name):
    result = [street_name]

    result += list(replace_umlauts(street_name))

    other_spacing_variant = None
    if normalize_street(street_name) != street_name:
        other_spacing_variant = normalize_street(street_name)
    if street_name.endswith('traße'):
        other_spacing_variant = street_name[:-3] + "."
    if other_spacing_variant:
        result += [other_spacing_variant]
        result += list(replace_umlauts(other_spacing_variant))

    other_spacing_variant = None
    p = re.compile(r'(.*)[^\w]S(tra[ss|ß]e)')
    x = re.findall(p, street_name)
    if x:
        other_spacing_variant = "{}s{}".format(x[0][0], x[0][1])
    p = re.compile(r'(.*[^\s])s(tra[ss|ß]e)')
    x = re.findall(p, street_name)
    if x:
        other_spacing_variant = "{} S{}".format(x[0][0], x[0][1])
    if other_spacing_variant:
        if normalize_street(other_spacing_variant) != other_spacing_variant:
            result += [normalize_street(street_name)]
        if other_spacing_variant.endswith('traße'):
            x = other_spacing_variant[:-3] + "."
            result += list(replace_umlauts(x))
            result += [x]
        result += [other_spacing_variant]
        result += list(replace_umlauts(other_spacing_variant))

    return set(result)


def call_schaal_und_mueller_for_district_id(street, fixture=False):
    if fixture:
        import responses

#    if street.schaalundmueller_district_id:
#        return
    street_list = get_possible_street_variants(street.name)
    url = 'http://www.schaal-mueller.de/GelberSackinStuttgart.aspx'

    if fixture:
        with responses.RequestsMock() as rsps:
            rsps.add(responses.POST, 'http://www.schaal-mueller.de/GelberSackinStuttgart.aspx',
                     status=200, body=open(fixture).read(),
                     content_type='text/html')
            resp = requests.post(url)
    else:
        resp = requests.post(url)
    soup = BeautifulSoup(resp.text.encode(resp.encoding).decode('utf-8'))
    viewstate = soup.select("#__VIEWSTATE")[0]['value']
    stategenerator = soup.select("#__VIEWSTATEGENERATOR")[0]['value']
    stateencrypted = soup.select("#__VIEWSTATEENCRYPTED")[0]['value']
    eventvalidation = soup.select("#__EVENTVALIDATION")[0]['value']

    for street_name in street_list:
        payload = {
            '__VIEWSTATEGENERATOR': stategenerator,
            '__VIEWSTATEENCRYPTED': stateencrypted,
            '__VIEWSTATE': viewstate,
            '__EVENTVALIDATION': eventvalidation,
            'dnn$ctr491$View$txtZIP': street.zipcode.zipcode,
            'dnn$ctr491$View$txtStreet': street_name,
            'dnn$ctr491$View$btSearchStreets': 'suchen',
        }
        if fixture:
            with responses.RequestsMock() as rsps:
                rsps.add(responses.POST, 'http://www.schaal-mueller.de/GelberSackinStuttgart.aspx',
                         status=200, body=open(fixture).read(),
                         content_type='text/html')
                resp = requests.post(url, data=payload)
        else:
            resp = requests.post(url, data=payload)
        text = resp.text.encode(resp.encoding).decode('utf-8')
        x = re.findall(r"javascript:__doPostBack\('ThatStreet', '(\d+)'\)", text)
        if x:
            street.schaalundmueller_district_id = int(x[0])
            street.save()
            return int(x[0])


def call_schaal_und_mueller_district(district_id, fixture=False):
    if fixture:
        import responses

    url = 'http://www.schaal-mueller.de/GelberSackinStuttgart.aspx'

    payload = {'__EVENTTARGET': 'ThatStreet'}
    payload['__EVENTARGUMENT'] = str(district_id)
    if fixture:
        with responses.RequestsMock() as rsps:
            rsps.add(responses.POST, 'http://www.schaal-mueller.de/GelberSackinStuttgart.aspx',
                     status=200, body=open(fixture).read(),
                     content_type='text/html')
            resp = requests.post(url, data=payload)
    else:
        resp = requests.post(url, data=payload)

    soup = BeautifulSoup(resp.text.encode(resp.encoding).decode('utf-8'))
    div = soup.find('div', {'id': 'dnn_ctr491_View_panResults'})
    if div:
        area_name = None
        if div.find('span'):
            area_name = div.find('span', {'id': 'dnn_ctr491_View_lblResults'}).text
        if div.find('table'):
            dates = [span.text for span in div.find('table').findAll('span')]
            return {
                'area': area_name,
                'dates': dates
            }


def parse_schaal_und_mueller_csv_data(filename, year):
    regex = r"(.*)\ ([0-9\.]*)\ (Mo.|Di.|Mi.|Do.|Fr.)\ ([0-9\.\ ]*)"
    from main.models import Area
    with open(filename, 'r') as fp:
        for line in fp.readlines():
            if line.startswith('#'):
                continue
            # find weekday and split on it
            area = re.findall(regex, line)[0][0]
            a = Area.objects.filter(description=area).first()
            if not a:
                for in_db, in_csv in (
                        ('Birkach, Botnang, Plieningen', 'Birkach, Plieningen, Botnang'),
                        ('Frauenkopf, Hedelfingen (ohne Hafen), Sillenbuch, Riedenberg', 'Frauenkopf, Hedelfingen (ohne Hafen) Sillenbuch (mit Riedenberg)'),
                        ('Stuttgart-West (ohne Kräherwald, Solitude, Wildpark)', 'Stuttgart-West (ohne Kräherwald, Solitude,Wildpark)'),
                        ('Bad Cannstatt I (ohneSteinhaldenfeld), Mühlhausen', 'Bad Cannstatt I (ohneSteinhaldenfeld) Mühlhausen'),
                        ('Büsnau, Degerloch, Dürrlewang, Kräherwald,Solitude, Wildpark', 'Büsnau, Degerloch, Dürrlewang,Kräherwald,Solitude, Wildpark'),
                ):
                    if area == in_csv:
                        a = Area.objects.filter(description=in_db).first()
            if not a:
                assert 'Area not found'
