from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.models.document_type_models import DocumentType
try:
    from mayan.apps.events.classes import EventManagerSave
except ImportError:
    from mayan.apps.events.event_managers import EventManagerSave

from mayan.apps.events.decorators import method_event

from credentials.models import StoredCredential

from ..events import (
    event_import_setup_created, event_import_setup_edited,
    event_import_setup_populate_ended, event_import_setup_populate_started,
    event_import_setup_process_ended, event_import_setup_process_started
)
from ..literals import (
    DEFAULT_ITEM_TIME_BUFFER, DEFAULT_PROCESS_SIZE, ITEM_STATE_COMPLETE,
    ITEM_STATE_DOWNLOADED, SETUP_STATE_CHOICES, SETUP_STATE_ERROR,
    SETUP_STATE_EXECUTING, SETUP_STATE_NONE, SETUP_STATE_POPULATING
)
from ..tasks import task_import_setup_item_process

from .mixins import BackendModelMixin

ENABLE_STATE_CHANGE = False


class ImportSetup(BackendModelMixin, models.Model):
    label = models.CharField(
        help_text=_('Short description of this import setup.'),
        max_length=128, unique=True, verbose_name=_('Label')
    )
    credential = models.ForeignKey(
        blank=True, null=True, on_delete=models.CASCADE,
        related_name='import_setups', to=StoredCredential,
        verbose_name=_('Credential')
    )
    document_type = models.ForeignKey(
        on_delete=models.CASCADE, related_name='import_setups',
        to=DocumentType, verbose_name=_('Document type')
    )
    process_size = models.PositiveIntegerField(
        default=DEFAULT_PROCESS_SIZE, help_text=_(
            'Number of items to process per execution.'
        ), verbose_name=_('Process size')
    )
    state = models.PositiveIntegerField(
        choices=SETUP_STATE_CHOICES, default=SETUP_STATE_NONE, help_text=_(
            'The last recorded state of the import setup.'
        ), verbose_name=_('State')
    )
    item_time_buffer = models.PositiveIntegerField(
        default=DEFAULT_ITEM_TIME_BUFFER, help_text=_(
            'Delay in milliseconds between item import tasks execution.'
        ), verbose_name=_('Item time buffer')
    )

    class Meta:
        ordering = ('label',)
        verbose_name = _('Import setup')
        verbose_name_plural = _('Import setups')

    def __str__(self):
        return self.label

    def clear(self):
        self.items.all().delete()

    def get_absolute_url(self):
        return reverse(
            viewname='importer:import_setup_list'
        )

    def get_backend_instance(self):
        kwargs = self.get_backend_data()

        if self.credential:
            kwargs.update(
                {
                    'credential_class': self.credential.get_backend(),
                    'credential_data': self.credential.get_backend_data()
                }
            )

        return self.get_backend()(**kwargs)

    def get_state_label(self):
        return self.get_state_display()
    get_state_label.short_description = _('State')
    get_state_label.help_text = _(
        'The last recorded state of the setup item. The field will be '
        'sorted by the numeric value of the state and not the actual text.'
    )

    def item_count_all(self):
        return self.items.count()

    item_count_all.short_description = _('Items')

    def item_count_complete(self):
        return self.items.filter(state=ITEM_STATE_COMPLETE).count()

    item_count_complete.short_description = _('Items complete')

    def item_count_percent(self):
        items_complete = self.item_count_complete()
        items_all = self.item_count_all()

        if items_all == 0:
            percent = 0
        else:
            percent = items_complete / items_all * 100.0

        return '{} of {} ({:.0f}%)'.format(
            intcomma(value=items_complete), intcomma(value=items_all),
            percent
        )

    item_count_percent.short_description = _('Progress')

    def populate(self, user=None):
        event_import_setup_populate_started.commit(
            actor=user, target=self
        )

        if ENABLE_STATE_CHANGE:
            self.state = SETUP_STATE_POPULATING
            self.save()

        try:
            backend = self.get_backend_instance()

            for item in backend.get_item_list():

                identifer_field = backend.item_identifier
                try:
                    # Try as an attribute
                    identifier = getattr(item, identifer_field)
                except (AttributeError, TypeError):
                    # Try as dictionary
                    identifier = item[identifer_field]

                setup_item, created = self.items.get_or_create(
                    identifier=identifier
                )
                if created:
                    setup_item.dump_data(
                        obj=item
                    )
                    setup_item.save()
        except Exception as exception:
            if ENABLE_STATE_CHANGE:
                self.state = SETUP_STATE_ERROR
                self.save()

            self.logs.create(
                text=str(exception)
            )

            if settings.DEBUG:
                raise
        else:
            if ENABLE_STATE_CHANGE:
                self.state = SETUP_STATE_NONE
                self.save()

            event_import_setup_populate_ended.commit(
                actor=user, target=self
            )

            self.logs.all().delete()

    def process(self, user=None):
        """
        Iterate of the ImportSetupItem instances downloading and creating
        documents from them.
        """
        if ENABLE_STATE_CHANGE:
            self.state = SETUP_STATE_EXECUTING
            self.save()

        event_import_setup_process_started.commit(
            actor=user, target=self
        )

        try:
            count = 0
            eta = datetime.utcnow()
            # Only schedule items that have not succeeded in being imported.
            queryset = self.items.exclude(state=ITEM_STATE_DOWNLOADED)
            iterator = queryset.iterator()

            while True:
                item = next(iterator)
                if item.check_valid():
                    count = count + 1
                    eta += timedelta(milliseconds=self.item_time_buffer)
                    task_import_setup_item_process.apply_async(
                        eta=eta, kwargs={
                            'import_setup_item_id': item.pk
                        }
                    )
                    if count >= self.process_size:
                        break
        except StopIteration:
            """
            Expected exception when iterator is exhausted before the process
            size is reached.
            """
        except Exception as exception:
            if ENABLE_STATE_CHANGE:
                self.state = SETUP_STATE_ERROR
                self.save()

            self.logs.create(
                text=str(exception)
            )

            if settings.DEBUG:
                raise

            # Exit the method to avoid committing the ended event.
            return

        # This line is reached on StopIteration or from the break in the loop.
        if ENABLE_STATE_CHANGE:
            self.state = SETUP_STATE_NONE
            self.save()

        self.logs.all().delete()

        event_import_setup_process_ended.commit(
            actor=user, target=self
        )

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_import_setup_created,
            'target': 'self',
        },
        edited={
            'event': event_import_setup_edited,
            'target': 'self',
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class ImportSetupLog(models.Model):
    import_setup = models.ForeignKey(
        on_delete=models.CASCADE, related_name='logs',
        to=ImportSetup, verbose_name=_('Import setup log')
    )
    datetime = models.DateTimeField(
        auto_now_add=True, db_index=True, editable=False,
        verbose_name=_('Date time')
    )
    text = models.TextField(
        blank=True, editable=False, verbose_name=_('Text')
    )

    class Meta:
        get_latest_by = 'datetime'
        ordering = ('-datetime',)
        verbose_name = _('Log entry')
        verbose_name_plural = _('Log entries')
