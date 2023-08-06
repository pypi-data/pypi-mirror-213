import logging

from django.contrib import messages
from django.core.files import File
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.translation import ungettext, ugettext_lazy as _

from mayan.apps.documents.views.document_views import DocumentListView
from mayan.apps.organizations.utils import get_organization_installation_url
from mayan.apps.storage.models import SharedUploadedFile
from mayan.apps.views.generics import (
    ConfirmView, FormView, MultipleObjectConfirmActionView,
    SingleObjectEditView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectViewMixin

from ..classes import ModelFiler
from ..forms import ModelFilerUpload
from ..icons import icon_import_setup_items_list
from ..links import link_import_setup_populate, link_model_filer_load
from ..models import ImportSetup, ImportSetupItem
from ..permissions import (
    permission_import_setup_edit, permission_import_setup_process,
    permission_import_setup_view, permission_model_filer_load,
    permission_model_filer_save
)
from ..tasks import (
    task_import_setup_item_process, task_import_setup_populate,
    task_import_setup_process, task_model_filer_load, task_model_filer_save
)

logger = logging.getLogger(name=__name__)


class ImportSetupClearView(MultipleObjectConfirmActionView):
    model = ImportSetup
    object_permission = permission_import_setup_process
    pk_url_kwarg = 'import_setup_id'
    success_message = _('%(count)d import setup cleared.')
    success_message_plural = _('%(count)d import setups cleared.')

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'title': ungettext(
                singular='Clear the selected import setup?',
                plural='Clear the selected import setups?',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _('Clear import setup: %s') % queryset.first()
                }
            )

        return result

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def object_action(self, instance, form=None):
        instance.clear()


class ImportSetupItemDeleteView(MultipleObjectConfirmActionView):
    model = ImportSetupItem
    object_permission = permission_import_setup_edit
    pk_url_kwarg = 'import_setup_item_id'
    success_message = _('%(count)d import setup item deleted.')
    success_message_plural = _('%(count)d import setup items deleted.')

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'delete_view': True,
            'import_setup': self.object_list.first().import_setup,
            'message': _(
                'You can add this item again by executing the prepare '
                'action.'
            ),
            'navigation_object_list': ('import_setup', 'object'),
            'title': ungettext(
                singular='Delete the selected import setup item?',
                plural='Delete the selected import setup items?',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _('Delete import setup item: %s') % queryset.first()
                }
            )

        return result

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def get_post_action_redirect(self):
        # Use [0] instead of first(). First returns None and it is not usable.
        return reverse(
            viewname='importer:import_setup_items_list', kwargs={
                'import_setup_id': self.object_list[0].import_setup.pk
            }
        )

    def object_action(self, instance, form=None):
        instance.delete()


class ImportSetupItemEditView(SingleObjectEditView):
    fields = (
        'identifier', 'serialized_data', 'serialized_data', 'state',
        'state_data'
    )
    model = ImportSetupItem
    object_permission = permission_import_setup_edit
    pk_url_kwarg = 'import_setup_item_id'

    def get_extra_context(self):
        return {
            'import_setup': self.object.import_setup,
            'navigation_object_list': ('import_setup', 'object'),
            'title': _(
                'Edit import setup item: %s'
            ) % self.object
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class ImportSetupItemDocumentListView(
    ExternalObjectViewMixin, DocumentListView
):
    external_object_class = ImportSetupItem
    external_object_permission = permission_import_setup_view
    external_object_pk_url_kwarg = 'import_setup_item_id'

    def get_document_queryset(self):
        return self.external_object.documents.all()

    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'import_setup': self.external_object.import_setup,
                'import_setup_item': self.external_object,
                'navigation_object_list': (
                    'import_setup', 'import_setup_item'
                ),
                'no_results_text': _(
                    'This view will list the documents that were created '
                    'by an import setup item.'
                ),
                'no_results_title': _(
                    'There are no documents for this import setup item.'
                ),
                'title': _(
                    'Document created from import setup item: %s'
                ) % self.external_object
            }
        )
        return context


class ImportSetupItemListView(ExternalObjectViewMixin, SingleObjectListView):
    external_object_class = ImportSetup
    external_object_permission = permission_import_setup_view
    external_object_pk_url_kwarg = 'import_setup_id'

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_import_setup_items_list,
            'no_results_secondary_links': (
                link_import_setup_populate.resolve(
                    context=RequestContext(
                        dict_={'object': self.external_object},
                        request=self.request
                    )
                ),
                link_model_filer_load.resolve(
                    context=RequestContext(
                        dict_={'object': self.external_object},
                        request=self.request
                    )
                ),
            ),
            'no_results_text': _(
                'Import setups items are the entries for the actual '
                'files that will be imported and converted into documents.'
            ),
            'no_results_title': _('No import setups items available'),
            'object': self.external_object,
            'title': _('Items of import setup: %s') % self.external_object
        }

    def get_source_queryset(self):
        return self.external_object.items.all()


class ImportSetupItemProcessView(MultipleObjectConfirmActionView):
    model = ImportSetupItem
    object_permission = permission_import_setup_process
    pk_url_kwarg = 'import_setup_item_id'
    success_message = _('%(count)d import setup item processed.')
    success_message_plural = _('%(count)d import setup items processed.')

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'import_setup': self.object_list.first().import_setup,
            'navigation_object_list': ('import_setup', 'object'),
            'title': ungettext(
                singular='Process the selected import setup item?',
                plural='Process the selected import setup items?',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _('Process import setup item: %s') % queryset.first()
                }
            )

        return result

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def get_post_action_redirect(self):
        # Use [0] instead of first(). First returns None and it is not usable.
        return reverse(
            viewname='importer:import_setup_items_list', kwargs={
                'import_setup_id': self.object_list[0].import_setup.pk
            }
        )

    def object_action(self, instance, form=None):
        task_import_setup_item_process.apply_async(
            kwargs={
                'import_setup_item_id': instance.pk
            }
        )


class ImportSetupItemLoadView(ExternalObjectViewMixin, FormView):
    external_object_class = ImportSetup
    external_object_object_permission = permission_model_filer_load
    external_object_pk_url_kwarg = 'import_setup_id'
    form_class = ModelFilerUpload

    def form_valid(self, form):
        with self.request.FILES['uploaded_file'].open(mode='r') as file_object:
            shared_upload_file = SharedUploadedFile.objects.create(
                file=File(file_object),
            )

        full_model_name = ModelFiler.get_full_model_name(
            model=self.external_object.items.model
        )
        task_model_filer_load.apply_async(
            kwargs={
                'field_defaults': {'import_setup_id': self.external_object.pk},
                'full_model_name': full_model_name,
                'shared_upload_file_id': shared_upload_file.pk
            }
        )

        messages.success(
            message=_('File uploaded and queued for loading as models.'),
            request=self.request
        )
        return HttpResponseRedirect(
            redirect_to=reverse(viewname='importer:import_setup_list')
        )

    def get_extra_context(self):
        return {
            'object': self.external_object,
            'title': _(
                'Load the items of import setup: %s'
            ) % self.external_object
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }


class ImportSetupItemSaveConfirmView(ExternalObjectViewMixin, ConfirmView):
    external_object_class = ImportSetup
    external_object_object_permission = permission_model_filer_save
    external_object_pk_url_kwarg = 'import_setup_id'

    def get_extra_context(self):
        return {
            'object': self.external_object,
            'title': _(
                'Save the items of import setup: %s'
            ) % self.external_object
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def view_action(self):
        full_model_name = ModelFiler.get_full_model_name(
            model=self.external_object.items.model
        )

        task_model_filer_save.apply_async(
            kwargs={
                'filter_kwargs': {'import_setup': self.external_object.pk},
                'full_model_name': full_model_name,
                'save_file_title': str(
                    _('Import setup "%s"') % self.external_object
                ),
                'organization_installation_url': get_organization_installation_url(
                    request=self.request
                ),
                'user_id': self.request.user.pk
            }
        )


class ImportSetupPopulateView(MultipleObjectConfirmActionView):
    model = ImportSetup
    object_permission = permission_import_setup_process
    pk_url_kwarg = 'import_setup_id'
    post_action_redirect = reverse_lazy(
        viewname='importer:import_setup_list'
    )
    success_message = _('%(count)d import setup item population queued.')
    success_message_plural = _('%(count)d import setups item population queued.')

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'message': _(
                'This process will populate the items to import by querying '
                'the source repository. The process will run in the '
                'background and once starter, cannot be stopped from the '
                'user interface. The time to completion will depend on the '
                'number of files that match the import setup criteria, the '
                'import backend, the size of the source repository, and '
                'the bandwidth between Mayan EDMS and the source '
                'repository. The completion may take between a few minutes '
                'to a few days to complete.'
            ),
            'title': ungettext(
                singular='Population the selected import setup?',
                plural='Population the selected import setups?',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _('Prepare import setup: %s') % queryset.first()
                }
            )

        return result

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def object_action(self, instance, form=None):
        task_import_setup_populate.apply_async(
            kwargs={'import_setup_id': instance.pk}
        )


class ImportSetupProcessView(MultipleObjectConfirmActionView):
    model = ImportSetup
    object_permission = permission_import_setup_process
    pk_url_kwarg = 'import_setup_id'
    post_action_redirect = reverse_lazy(
        viewname='importer:import_setup_list'
    )
    success_message = _('%(count)d import setup processing queued.')
    success_message_plural = _('%(count)d import setups processing queued.')

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'title': ungettext(
                singular='Process the selected import setup?',
                plural='Process the selected import setups?',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _('Process import setup: %s') % queryset.first()
                }
            )

        return result

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def object_action(self, instance, form=None):
        if instance.items.count() == 0:
            messages.warning(
                message=_(
                    'Import setup "%s" does not have any item to process. '
                    'Use the prepare action first.'
                ) % instance, request=self.request
            )
        else:
            task_import_setup_process.apply_async(
                kwargs={
                    'import_setup_id': instance.pk
                }
            )
