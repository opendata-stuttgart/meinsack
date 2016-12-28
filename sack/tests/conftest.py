import os
import pytest


@pytest.fixture
def stuttgart_districts():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'fixtures/',
                        'stuttgart_districts.html')

@pytest.fixture
def mocked_district(stuttgart_districts):
    import responses
    from main.utils import get_districts_stuttgart
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, 'http://onlinestreet.de/strassen/in-Stuttgart.html',
                 status=200, body=open(stuttgart_districts).read(), content_type='text/html')
        return list(get_districts_stuttgart())


@pytest.fixture
def stuttgart_districts_process(mocked_district):
    from main.utils import add_district_to_database, extract_district_from_tr
    for index, tr in enumerate(mocked_district):
        x = extract_district_from_tr(tr)
        add_district_to_database(x)
