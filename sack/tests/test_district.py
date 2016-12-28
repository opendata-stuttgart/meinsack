import os.path
import pytest
import responses

from main.utils import (
    add_street_to_database,
    extract_district_from_tr,
    extract_street_from_tr,
    get_streets_from_district,
    normalize_street,
)


@pytest.fixture
def stuttgart_streets_hausen():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'fixtures/',
                        'stuttgart_streets_hausen.html')


@pytest.fixture
def stuttgart_streets_hausen_process(mocked_streets_hausen):
    from main.models import District
    for index, tr in enumerate(mocked_streets_hausen):
        x = extract_street_from_tr(tr)
        add_street_to_database(x, District.objects.first())


@pytest.fixture
def mocked_streets_hausen(stuttgart_districts_process, stuttgart_streets_hausen):
    from main.models import District
    dis = District.objects.get(name="Hausen")
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, dis.url_onlinestreet,
                 status=200, body=open(stuttgart_streets_hausen).read(), content_type='text/html')
        return list(get_streets_from_district(dis))


@pytest.mark.django_db
class TestDistrict():

    def test_district_import(self, mocked_district):
        assert len(mocked_district) == 56

    def test_extract_district_from_tr(self, mocked_district):
        for index, tr in enumerate(mocked_district):
            x = extract_district_from_tr(tr)
            assert isinstance(x, dict)
            assert 'name' in x
            break  # one is enough

    def test_add_district_to_database(self, stuttgart_districts_process):
        from main.models import District
        assert District.objects.count() == 56
        assert District.objects.filter(name="Bad Cannstatt")


@pytest.mark.django_db
class TestStreet():

    def test_extract_street_from_tr(self, mocked_streets_hausen):
        for index, tr in enumerate(mocked_streets_hausen):
            x = extract_street_from_tr(tr)
            assert x['name'] == 'Gerlinger Straße'
            assert x['zipcode'] == '70499'
            assert x['city'] == 'Stuttgart-Hausen'
            break  # one is enough

    def test_add_district_to_database(self, stuttgart_streets_hausen_process):
        from main.models import Street
        assert Street.objects.count() == 7
        assert Street.objects.filter(name="Gerlinger Straße")


class TestNormlizingStreet():
    @pytest.mark.parametrize(('name', 'name_normalized'), (
        ('Gerlinger Str.', 'Gerlinger Straße'),
        ('Gerlingerstr.', 'Gerlingerstraße'),
    ))
    def test_normalize_street(self, name, name_normalized):
        assert normalize_street(name) == name_normalized
