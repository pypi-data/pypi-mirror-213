from appconf import AppConf
from django.conf import settings


class SingletonConf(AppConf):
    class Meta:
        prefix = "singleton"

    RAISE_ERROR_ON_SAVE = False
    """
    Flag to raise an error if you attempt to save a new singleton.
    Default is to just do nothing.
    """

__all__ = ["settings", "SingletonConf"]
