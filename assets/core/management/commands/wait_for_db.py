"""
Django command to wait for the database to be available.
"""

import time

from MySQLdb import OperationalError as MySQLOperationalError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write("Waiting for database...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except MySQLOperationalError as error:
                self.stdout.write('Database unavailable, waiting 2 second...')
                self.stdout.write(f'MySQLOperationalError: {error}')
                time.sleep(2)
            except OperationalError as error:
                self.stdout.write('Database unavailable, waiting 2 second...')
                self.stdout.write(f'DjangoOperatinalError: {error}')
                time.sleep(2)

        self.stdout.write(self.style.SUCCESS('Database available!'))
