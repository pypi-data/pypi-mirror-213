from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from singleton2.conf import settings as app_settings


class SingletonMixin(models.Model):
    """
    Mixin to turn a model into a singleton
    """

    class Meta:
        abstract = True

    DEFAULT_SINGLETON_ID = 1

    ERROR_MESSAGE = _("Only one instance of a Singleton is allowed.")

    _singleton_id = models.IntegerField(
        default=DEFAULT_SINGLETON_ID,
        editable=False,
        help_text=_(
            "An ID to use for this mixin, "
            "in case the model uses some non-standard PK."
        ),
    )

    def clean(self, *args, **kwargs):
        if not self.pk and self.__class__.objects.count() > 0:
            raise ValidationError(self.ERROR_MESSAGE)

    def save(self, *args, **kwargs):
        if self.pk or not self.__class__.objects.count():
            return super().save(*args, **kwargs)
        if app_settings.SINGLETON_RAISE_ERROR_ON_SAVE:
            raise ValidationError(self.ERROR_MESSAGE)

    @classmethod
    def load(cls):
        """
        Returns the one-and-only singleton instance
        """
        obj, _ = cls.objects.get_or_create(_singleton_id=cls.DEFAULT_SINGLETON_ID)
        return obj
