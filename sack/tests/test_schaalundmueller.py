import pytest
import os

from main.utils import call_schaal_und_mueller_for_district_id, call_schaal_und_mueller_district


@pytest.fixture
def schaalundmueller_ulmerstrasse():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'fixtures/',
                        'schaalundmueller_ulmerstrasse.html')


@pytest.fixture
def schaalundmueller_daimlerstrasse():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'fixtures/',
                        'schaalundmueller_daimlerstrasse.html')


@pytest.fixture
def schaalundmueller_district_6():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'fixtures/',
                        'schaalundmueller_district_6.html')


@pytest.fixture
def mocked_ulmerstrasse():
    from main.models import District, Street, ZipCode
    dis = District.objects.create(name="Wangen",
                                  city='Stuttgart',
                                  number_of_streets=1,
                                  url_onlinestreet="http://google.de")
    street = Street.objects.create(name="Ulmer Str.",
                                   city='Stuttgart',
                                   district=dis,
                                   zipcode=ZipCode.objects.create(zipcode="70327"),
                                   url_onlinestreet="http://google.de")
    return street


@pytest.fixture
def mocked_daimlerstrasse():
    from main.models import District, Street, ZipCode
    dis = District.objects.create(name="Bad Canstatt",
                                  city='Stuttgart',
                                  number_of_streets=1,
                                  url_onlinestreet="http://google.de")
    street = Street.objects.create(name="Daimlerstr.",
                                   city='Stuttgart',
                                   district=dis,
                                   zipcode=ZipCode.objects.create(zipcode="70372"),
                                   url_onlinestreet="http://google.de")
    return street


@pytest.mark.django_db
class TestSchaalundmuellerCrawler:

    def test_ulmerstrasse(self, mocked_ulmerstrasse, schaalundmueller_ulmerstrasse):
        assert call_schaal_und_mueller_for_district_id(
            mocked_ulmerstrasse,
            fixture=schaalundmueller_ulmerstrasse) == 6
        assert mocked_ulmerstrasse.schaalundmueller_district_id == 6

    @pytest.mark.skip
    def test_ulmerstrasse_live(self, mocked_ulmerstrasse, schaalundmueller_ulmerstrasse):
        assert call_schaal_und_mueller_for_district_id(mocked_ulmerstrasse) == 6
        assert mocked_ulmerstrasse.schaalundmueller_district_id == 6

    def test_daimlerstrasse(self, mocked_daimlerstrasse, schaalundmueller_daimlerstrasse):
        assert call_schaal_und_mueller_for_district_id(
            mocked_daimlerstrasse,
            fixture=schaalundmueller_daimlerstrasse) == 12
        assert mocked_daimlerstrasse.schaalundmueller_district_id == 12

    @pytest.mark.skip
    def test_daimlerstrasse_live(self, mocked_daimlerstrasse, schaalundmueller_daimlerstrasse):
        assert call_schaal_und_mueller_for_district_id(mocked_daimlerstrasse) == 12
        assert mocked_daimlerstrasse.schaalundmueller_district_id == 12

    @pytest.mark.skip
    def test_district_6_live(self):
        d = call_schaal_und_mueller_district(6)
        assert d['area'] == "Hafen, Unter- und Obertürkheim, Wangen"
        assert '.201' in d['dates'][0]

    def test_district_6(self, schaalundmueller_district_6):
        d = call_schaal_und_mueller_district(6, schaalundmueller_district_6)
        assert d['area'] == "Hafen, Unter- und Obertürkheim, Wangen"
        assert '12.12.2016' in d['dates']


@pytest.mark.django_db
class TestSchaalundmuellerDataImporter:

    @pytest.fixture
    def schaal_und_mueller_areas(self):
        from main.models import Area
        for index, area in enumerate(('Frauenkopf, Hedelfingen (ohne Hafen), Sillenbuch, Riedenberg',
                                      'Feuerbach, Killesberg, Weißenhof',
                                      'Möhringen',
                                      'Stuttgart-West (ohne Kräherwald, Solitude, Wildpark)',
                                      'Stammheim, Weilimdorf',
                                      'Hafen, Unter- und Obertürkheim, Wangen',
                                      'Münster, Steinhaldenfeld, Zuffenhausen',
                                      'Stuttgart-Süd',
                                      'Stuttgart-Ost (ohne Frauenkopf)',
                                      'Vaihingen (ohne Büsnau, Dürrlewang)',
                                      'Bad Cannstatt I (ohneSteinhaldenfeld), Mühlhausen',
                                      'Bad Cannstatt II (ohne Steinhaldenfeld)',
                                      'Stuttgart-Mitte, Stuttgart-Nord (ohne Killesberg, Weißenhof)',
                                      'Birkach, Botnang, Plieningen',
                                      'Büsnau, Degerloch, Dürrlewang, Kräherwald,Solitude, Wildpark')):
            Area.objects.create(description=area, district_id=index, bag_type='gelb', collector='Schaal+Mueller')

    def test_import(self, schaal_und_mueller_areas):
        from main.models import District, Area
        fn = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'main', 'data', 'stuttgart_2017.txt')
        from main.utils import parse_schaal_und_mueller_csv_data
        parse_schaal_und_mueller_csv_data(fn, 2017)
