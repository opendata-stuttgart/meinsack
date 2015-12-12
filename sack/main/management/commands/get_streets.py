# coding=utf-8
from django.core.management import BaseCommand


class Command(BaseCommand):

    help = "Import streets and districts"

    def handle(self, *args, **options):
        from main.utils import (
            add_district_to_database,
            add_street_to_database,
            extract_district_from_tr,
            extract_street_from_tr,
            get_districts_stuttgart,
            get_streets_from_district,
        )

        for tr in get_districts_stuttgart():
            d = extract_district_from_tr(tr)
            district = add_district_to_database(d)
            for street in get_streets_from_district(district):
                data = extract_street_from_tr(street)
                street = add_street_to_database(data, district)
