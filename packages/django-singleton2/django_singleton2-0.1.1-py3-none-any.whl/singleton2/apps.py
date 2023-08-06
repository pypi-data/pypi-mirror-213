from django.apps import AppConfig


class Singleton2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'singleton2'

    def ready(self) -> None:

        try:
            # register any checks...
            import singleton2.checks  # noqa
        except ImportError:
            pass

        try:
            # register any signals...
            import singleton2.signals  # noqa
        except ImportError:
            pass
