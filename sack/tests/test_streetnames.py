import pytest

from main.utils import get_possible_street_variants


class TestStreetNameVariants:

    @pytest.mark.parametrize(('street_name', 'results'), (
        ('Ulmer Straße', (
            'Ulmer Straße', 'Ulmer Strasse', 'Ulmer Str.', 'Ulmerstraße',
            'Ulmerstrasse', 'Ulmerstr.')),
        ('Daimlerstraße', (
            'Daimlerstraße', 'Daimlerstrasse', 'Daimlerstr.', 'Daimler Straße',
            'Daimler Strasse', 'Daimler Str.')),
        ('Neue Brücke', (
            'Neue Brücke', 'Neue Bruecke')),
        ('Großglocknerstraße', (
            'Großglocknerstraße', 'Grossglocknerstrasse', 'Großglocknerstr.',
            'Grossglocknerstr.', 'Großglockner Straße', 'Grossglockner Strasse',
            'Großglockner Str.', 'Grossglockner Str.')),
    ))
    def test_variants(self, street_name, results):
        assert get_possible_street_variants(street_name) == set(results)
