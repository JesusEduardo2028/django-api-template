from django.core.management.base import BaseCommand

from mock import factories


class Command(BaseCommand):
    """
    Command to populate data for testing purposes
    """

    def handle(self, *args, **options):

        self.stdout.write('Creating SuperUser admin@test.com')
        factories.SuperUserFactory(email='admin@test.com')

        self.stdout.write('Creating User user@test.com')
        factories.UserFactory(email='user@test.com')
