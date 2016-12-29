# coding=utf-8
from django.core.management import BaseCommand
from main.models import Street, Area, PickUpDate
from main.utils import parse_schaal_und_mueller_csv_data



class Command(BaseCommand):

    help = "schaal+mueller datafile parsing"

    def add_arguments(self, parser):
        parser.add_argument('--filename', required=True)
        parser.add_argument('--year', type=int, required=True)

    def handle(self, *args, **options):
        parse_schaal_und_mueller_csv_data(options['filename'], options['year'])
