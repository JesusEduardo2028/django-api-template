import factory

from django.conf import settings


class UserFactory(factory.DjangoModelFactory):

    class Meta:
        model = settings.AUTH_USER_MODEL

    email = factory.Sequence(lambda n: f'person{n}')
    password = '12345678'
    name = 'Sample User'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class SuperUserFactory(UserFactory):

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)

        return manager.create_superuser(
            kwargs['email'],
            kwargs['password']
        )
