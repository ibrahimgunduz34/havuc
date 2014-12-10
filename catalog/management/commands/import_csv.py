import csv
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from catalog.models import Resource, ProviderProduct


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--filename', '-f'),
        make_option('--resource_slug'),
    )

    def validate_options(self, **options):
        filename = options.get('filename')
        resource_slug = options.get('resource_slug')

        if not filename:
            raise CommandError('filename is required!')

        if not resource_slug:
            raise CommandError('resource_slug is required!')

    def get_resource(self, resource_slug):
        try:
            return Resource.objects.get(slug=resource_slug)
        except Resource.DoesNotExist:
            raise CommandError('The specified resource is not found.')

    def encode_utf8(self, data):
        for line in data:
            yield line.decode('utf-8').encode('utf8')

    def handle(self, *args, **options):
        self.validate_options(**options)
        resource = self.get_resource(options.get('resource_slug'))
        with open(options.get('filename'), 'r') as fh:
            reader = csv.reader(self.encode_utf8(fh), delimiter=",")
            for row in reader:
                try:
                    ProviderProduct.objects.create(
                        name=unicode(row[0], 'utf8'),
                        url=row[1], resource=resource)
                except IntegrityError:
                    self.stdout.write('%s is already exist.' % row[1])
