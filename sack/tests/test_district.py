import responses
import os.path
import pytest
from main.utils import get_districts_stuttgart, add_district_to_database, extract_district_from_tr, extract_street_from_tr, get_streets_from_district


@pytest.fixture
def stuttgart_districts():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'fixtures/',
                        'stuttgart_districts.html')


@pytest.fixture
def stuttgart_streets_hausen():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'fixtures/',
                        'stuttgart_streets_hausen.html')


@pytest.fixture
def mocked_district(stuttgart_districts):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, 'http://onlinestreet.de/strassen/in-Stuttgart.html',
                 status=200, body=open(stuttgart_districts).read(), content_type='text/html')
        return list(get_districts_stuttgart())


@pytest.fixture
def stuttgart_districts_process(mocked_district):
    for index, tr in enumerate(mocked_district):
        if index == 0:
            # ignore head
            continue
        x = extract_district_from_tr(tr)
        add_district_to_database(x)


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
        assert len(mocked_district) == 57

    def test_extract_district_from_tr(self, mocked_district):
        for index, tr in enumerate(mocked_district):
            if index == 0:
                # ignore head
                continue
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
            if index == 0:
                # ignore head
                continue
            x = extract_street_from_tr(tr)
            break  # one is enough
