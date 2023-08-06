from django.db import models
from django.db.models import Max
from django.utils.translation import ugettext_lazy as _

try:
    from mayan.apps.events.classes import EventManagerSave
except ImportError:
    from mayan.apps.events.event_managers import EventManagerSave

from mayan.apps.events.decorators import method_event

from ..events import event_import_setup_edited

from .import_setup_models import ImportSetup
from .mixins import BackendModelMixin


class ImportSetupAction(BackendModelMixin, models.Model):
    import_setup = models.ForeignKey(
        on_delete=models.CASCADE, related_name='actions', to=ImportSetup,
        verbose_name=_('Import Setup')
    )
    label = models.CharField(
        max_length=255, help_text=_('A short text describing the action.'),
        verbose_name=_('Label')
    )
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))
    order = models.PositiveIntegerField(
        blank=True, db_index=True, default=0, help_text=_(
            'Order in which the action will be executed. If left '
            'unchanged, an automatic order value will be assigned.'
        ), verbose_name=_('Order')
    )

    class Meta:
        ordering = ('order', 'label')
        unique_together = (
            ('import_setup', 'order'), ('import_setup', 'label')
        )
        verbose_name = _('Import setup action')
        verbose_name_plural = _('Import setup actions')

    def __str__(self):
        return self.label

    def execute(self, context=None):
        if not context:
            context = {}

        return self.get_backend_instance().execute(context=context)

    def get_next_order(self):
        last_order = self.import_setup.actions.aggregate(
            Max('order')
        )['order__max']

        if last_order is not None:
            return last_order + 1
        else:
            return 0

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'action_object': 'self',
            'event': event_import_setup_edited,
            'target': 'import_setup'
        },
        edited={
            'action_object': 'self',
            'event': event_import_setup_edited,
            'target': 'import_setup'
        }
    )
    def save(self, *args, **kwargs):
        if not self.order:
            self.order = self.get_next_order()
        super().save(*args, **kwargs)
