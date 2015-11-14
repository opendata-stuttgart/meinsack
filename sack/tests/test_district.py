import os.path
import pytest
from main.utils import get_districts_stuttgart, add_district_to_database, extract_district_from_tr, extract_street_from_tr, get_streets_from_district


@pytest.fixture
def stuttgart_districts():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'fixtures/',
                        'stuttgart_districts.html')


@pytest.fixture
def stuttgart_districts_process(stuttgart_districts):
    for index, tr in enumerate(get_districts_stuttgart(stuttgart_districts)):
        if index == 0:
            # ignore head
            continue
        x = extract_district_from_tr(tr)
        add_district_to_database(x)


@pytest.mark.django_db
class TestDistrict():

    def test_district_import(self, stuttgart_districts):
        x = get_districts_stuttgart(stuttgart_districts)
        assert len(list(x)) == 57

    def test_extract_district_from_tr(self, stuttgart_districts):
        for index, tr in enumerate(get_districts_stuttgart(stuttgart_districts)):
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

    def test_extract_street_from_tr(self, stuttgart_districts_process):
        from main.models import District
        for index, tr in enumerate(get_streets_from_district(District.objects.first())):
            if index == 0:
                # ignore head
                continue
            x = extract_street_from_tr(tr)
            break  # one is enough
