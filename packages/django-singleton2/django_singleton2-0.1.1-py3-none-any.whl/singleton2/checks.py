from django.conf import settings
from django.core.checks import Error, Tags, register

from singleton2 import __title__ as APP_TITLE

APP_DEPENDENCIES = [
    # list of django-apps required by this app
]
APP_SETTINGS = {
    # map of config settings required by this app
}
THIRD_PARTY_SETTINGS = {
    # map of config settings required by dependencies of this app
}


@register(Tags.compatibility)
def check_app_dependencies(app_configs, **kwargs):

    errors = []

    for i, dependency in enumerate(APP_DEPENDENCIES):
        if dependency not in settings.INSTALLED_APPS:
            errors.append(
                Error(
                    f"You are using {APP_TITLE} which requires the {dependency} module.  Please install it and add it to INSTALLED_APPS.",
                    id=f"{APP_TITLE}:E{i:03}",
                )
            )

    return errors


@register(Tags.compatibility)
def check_app_settings(app_configs, **kwargs):

    errors = []

    return errors


@register(Tags.compatibility)
def check_third_party_settings(app_configs, **kwargs):

    errors = []

    return errors
