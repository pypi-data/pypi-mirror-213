import logging

from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.generics import (
    FormView, SingleObjectDeleteView, SingleObjectDynamicFormCreateView,
    SingleObjectDynamicFormEditView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectViewMixin

from ..classes import ImportSetupActionBackend
from ..forms import (
    ImportSetupActionSelectionForm, ImportSetupActionDynamicForm
)
from ..icons import icon_import_setup_action
from ..links import link_import_setup_action_backend_selection
from ..models import ImportSetup, ImportSetupAction
from ..permissions import (
    permission_import_setup_edit, permission_import_setup_view
)

logger = logging.getLogger(name=__name__)


class ImportSetupActionCreateView(
    ExternalObjectViewMixin, SingleObjectDynamicFormCreateView
):
    external_object_class = ImportSetup
    external_object_permission = permission_import_setup_edit
    external_object_pk_url_kwarg = 'import_setup_id'
    form_class = ImportSetupActionDynamicForm

    def get_class(self):
        try:
            return ImportSetupActionBackend.get(
                name=self.kwargs['class_path']
            )
        except KeyError:
            raise Http404(
                '{} class not found'.format(self.kwargs['class_path'])
            )

    def get_extra_context(self):
        return {
            'object': self.external_object,
            'title': _(
                'Create "%(import_setup_action)s" action for import '
                'setup: %(import_setup)s'
            ) % {
                'import_setup_action': self.get_class().label,
                'import_setup': self.external_object
            }
        }

    def get_form_extra_kwargs(self):
        return {
            'request': self.request,
            'backend_path': self.kwargs['class_path']
        }

    def get_form_schema(self):
        return self.get_class()().get_form_schema(
            request=self.request, import_setup=self.external_object
        )

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'backend_path': self.kwargs['class_path'],
            'import_setup': self.external_object
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='importer:import_setup_action_list',
            kwargs={
                'import_setup_id': self.external_object.pk
            }
        )


class ImportSetupActionDeleteView(SingleObjectDeleteView):
    model = ImportSetupAction
    object_permission = permission_import_setup_edit
    pk_url_kwarg = 'import_setup_action_id'

    def get_extra_context(self):
        return {
            'navigation_object_list': (
                'import_setup', 'import_setup_action'
            ),
            'title': _('Delete import setup action: %s') % self.object,
            'import_setup': self.object.import_setup,
            'import_setup_action': self.object,
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='importer:import_setup_action_list',
            kwargs={
                'import_setup_id': self.object.import_setup.pk
            }
        )


class ImportSetupActionEditView(SingleObjectDynamicFormEditView):
    form_class = ImportSetupActionDynamicForm
    model = ImportSetupAction
    object_permission = permission_import_setup_edit
    pk_url_kwarg = 'import_setup_action_id'

    def get_extra_context(self):
        return {
            'navigation_object_list': (
                'object', 'import_setup', 'import_setup_action'
            ),
            'title': _('Edit import setup state action: %s') % self.object,
            'import_setup': self.object.import_setup,
            'import_setup_action': self.object,
        }

    def get_form_extra_kwargs(self):
        return {
            'request': self.request,
            'backend_path': self.object.backend_path,
        }

    def get_form_schema(self):
        return self.object.get_backend_instance().get_form_schema(
            request=self.request, import_setup=self.object.import_setup
        )

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class ImportSetupActionListView(ExternalObjectViewMixin, SingleObjectListView):
    external_object_class = ImportSetup
    external_object_permission = permission_import_setup_view
    external_object_pk_url_kwarg = 'import_setup_id'

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_import_setup_action,
            'no_results_main_link': link_import_setup_action_backend_selection.resolve(
                context=RequestContext(
                    request=self.request, dict_={
                        'object': self.external_object
                    }
                )
            ),
            'no_results_text': _(
                'Import setup actions are macros that get executed when '
                'documents are imported.'
            ),
            'no_results_title': _(
                'There are no actions for this import setup.'
            ),
            'object': self.external_object,
            'title': _(
                'Actions for import setup: %s'
            ) % self.external_object,
        }

    def get_source_queryset(self):
        return self.external_object.actions.all()


class ImportSetupActionBackendSelectionView(ExternalObjectViewMixin, FormView):
    external_object_class = ImportSetup
    external_object_permission = permission_import_setup_edit
    external_object_pk_url_kwarg = 'import_setup_id'
    form_class = ImportSetupActionSelectionForm

    def get_extra_context(self):
        return {
            'object': self.external_object,
            'title': _(
                'New import setup action selection for: %s'
            ) % self.external_object,
        }

    def form_valid(self, form):
        class_path = form.cleaned_data['class_path']
        return HttpResponseRedirect(
            redirect_to=reverse(
                viewname='importer:import_setup_action_create',
                kwargs={
                    'import_setup_id': self.external_object.pk,
                    'class_path': class_path
                }
            )
        )
