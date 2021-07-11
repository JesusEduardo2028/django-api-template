import factory

from django.conf import settings


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = settings.AUTH_USER_MODEL

    email = factory.Sequence(lambda n: f'person{n}')
    password = '12345678'
    name = 'Sample User'
