import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """ Django command to wait for database connection """

    def handle(self, *args, **options):
        """ Handles with the command """

        self.stdout.write('Connecting to the database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 sec...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
