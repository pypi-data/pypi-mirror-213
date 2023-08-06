import json

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.tasks import task_document_file_upload
try:
    from mayan.apps.events.classes import (
        EventManagerMethodAfter, EventManagerSave
    )
except ImportError:
    from mayan.apps.events.event_managers import (
        EventManagerMethodAfter, EventManagerSave
    )

from mayan.apps.events.decorators import method_event

from ..events import (
    event_import_setup_item_completed, event_import_setup_item_created,
    event_import_setup_item_deleted, event_import_setup_item_edited
)
from ..literals import (
    ITEM_STATE_CHOICES, ITEM_STATE_COMPLETE, ITEM_STATE_DOWNLOADED,
    ITEM_STATE_ERROR, ITEM_STATE_NONE
)

from .import_setup_models import ImportSetup


class ImportSetupItem(models.Model):
    import_setup = models.ForeignKey(
        on_delete=models.CASCADE, related_name='items',
        to=ImportSetup, verbose_name=_('Import setup')
    )
    identifier = models.CharField(
        db_index=True, max_length=64, verbose_name=_('Identifier')
    )
    serialized_data = models.TextField(
        blank=True, default='{}', verbose_name=_('Serialized data')
    )
    state = models.IntegerField(
        db_index=True, choices=ITEM_STATE_CHOICES, default=ITEM_STATE_NONE,
        verbose_name=_('State')
    )
    state_data = models.TextField(blank=True, verbose_name=_('State data'))
    documents = models.ManyToManyField(
        blank=True, related_name='import_items',
        to=Document, verbose_name=_('Document')
    )

    class Meta:
        ordering = ('import_setup', 'identifier')
        verbose_name = _('Import setup item')
        verbose_name_plural = _('Import setup items')

    def __str__(self):
        return self.identifier

    def get_absolute_url(self):
        return reverse(
            viewname='importer:import_setup_items_list', kwargs={
                'import_setup_id': self.import_setup.pk
            }
        )

    def check_valid(self):
        backend_instance = self.import_setup.get_backend_instance()
        return backend_instance.check_valid(
            identifier=self.identifier, data=self.data
        )

    @method_event(
        event_manager_class=EventManagerMethodAfter,
        event=event_import_setup_item_completed,
        action_object='import_setup',
        target='self',
    )
    def create_document(self, shared_uploaded_file):
        """
        Create a document from a downloaded ImportSetupItem instance.
        """
        backend_class = self.import_setup.get_backend()
        document_type = self.import_setup.document_type
        label = self.data.get(backend_class.item_label, self.id)

        try:
            document = Document.objects.create(
                document_type=document_type, label=label
            )
        except Exception as exception:
            self.state = ITEM_STATE_ERROR
            self.state_data = str(exception)
            self.save()
            if settings.DEBUG:
                raise
        else:
            self.state = ITEM_STATE_COMPLETE
            self.state_data = ''
            self.save()

            task_document_file_upload.apply_async(
                kwargs={
                    'document_id': document.pk,
                    'filename': document.label,
                    'shared_uploaded_file_id': shared_uploaded_file.pk,
                }
            )

            return document

    @cached_property
    def data(self):
        return self.load_data()

    @method_event(
        event_manager_class=EventManagerMethodAfter,
        event=event_import_setup_item_deleted,
        action_object='self',
        target='import_setup',
    )
    def delete(self):
        return super().delete()

    def load_data(self):
        return json.loads(s=self.serialized_data or '{}')

    def get_data_display(self):
        return ', '.join(
            [
                '"{}": "{}"'.format(key, value) for key, value in self.data.items()
            ]
        )
    get_data_display.short_description = _('Data')

    def dump_data(self, obj):
        self.serialized_data = json.dumps(obj=obj)

    def get_state_label(self):
        return self.get_state_display()
    get_state_label.help_text = _(
        'The last recorded state of the item. The field will be sorted by '
        'the numeric value of the state and not the actual text.'
    )
    get_state_label.short_description = _('State')

    def process(self):
        shared_uploaded_file = None

        if self.state == ITEM_STATE_NONE:
            try:
                backend_instance = self.import_setup.get_backend_instance()
                shared_uploaded_file = backend_instance.item_process(
                    identifier=self.identifier, data=self.data
                )
            except Exception as exception:
                self.state = ITEM_STATE_ERROR
                self.state_data = str(exception)
                self.save()
                if settings.DEBUG:
                    raise
            else:
                self.state = ITEM_STATE_DOWNLOADED
                self.state_data = ''
                self.save()

            if shared_uploaded_file:
                document = self.create_document(
                    shared_uploaded_file=shared_uploaded_file
                )
                if document:
                    self.documents.add(document)

                    context = {'document': document, 'self': self}
                    for action in self.import_setup.actions.filter(enabled=True):
                        action.execute(context=context)

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'action_object': 'import_setup',
            'event': event_import_setup_item_created,
            'target': 'self'
        },
        edited={
            'action_object': 'import_setup',
            'event': event_import_setup_item_edited,
            'target': 'self'
        }
    )
    def save(self, *args, **kwargs):
        if not self.state:
            self.state = ITEM_STATE_NONE

        if not self.state_data:
            self.state_data = ''

        super().save(*args, **kwargs)
