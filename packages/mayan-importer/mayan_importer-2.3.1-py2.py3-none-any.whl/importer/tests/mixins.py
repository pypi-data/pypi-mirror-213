from django.db.models import Q

from ..models import ImportSetup, ImportSetupAction

from .literals import (
    TEST_IMPORT_SETUP_ACTION_BACKEND_PATH, TEST_IMPORT_SETUP_ACTION_LABEL,
    TEST_IMPORT_SETUP_ACTION_LABEL_EDITED,
    TEST_IMPORT_SETUP_ITEM_IDENTIFIER_EDITED,
    TEST_IMPORT_SETUP_ITEM_TIME_BUFFER, TEST_IMPORT_SETUP_LABEL,
    TEST_IMPORT_SETUP_LABEL_EDITED, TEST_IMPORT_SETUP_PROCESS_SIZE,
    TEST_IMPORTER_BACKEND_PATH
)
from .importers import TestImporter


class ImportSetupAPIViewTestMixin:
    def _request_test_import_setup_create_api_view(self):
        pk_list = list(ImportSetup.objects.values_list('pk', flat=True))

        response = self.post(
            viewname='rest_api:importsetup-list', data={
                'label': TEST_IMPORT_SETUP_LABEL,
                'backend_path': TEST_IMPORTER_BACKEND_PATH,
                'document_type_id': self.test_document_type.pk
            }
        )

        try:
            self.test_import_setup = ImportSetup.objects.get(
                ~Q(pk__in=pk_list)
            )
        except ImportSetup.DoesNotExist:
            self.test_import_setup = None

        return response

    def _request_test_import_setup_delete_api_view(self):
        return self.delete(
            viewname='rest_api:importsetup-detail', kwargs={
                'import_setup_id': self.test_import_setup.pk
            }
        )

    def _request_test_import_setup_detail_api_view(self):
        return self.get(
            viewname='rest_api:importsetup-detail', kwargs={
                'import_setup_id': self.test_import_setup.pk
            }
        )

    def _request_test_import_setup_edit_via_patch_api_view(self):
        return self.patch(
            viewname='rest_api:importsetup-detail', kwargs={
                'import_setup_id': self.test_import_setup.pk
            }, data={
                'label': '{} edited'.format(self.test_import_setup.label)
            }
        )

    def _request_test_import_setup_edit_via_put_api_view(self):
        return self.put(
            viewname='rest_api:importsetup-detail', kwargs={
                'import_setup_id': self.test_import_setup.pk
            }, data={
                'label': '{} edited'.format(self.test_import_setup.label),
                'document_type_id': self.test_import_setup.document_type.pk,
            }
        )

    def _request_test_import_setup_list_api_view(self):
        return self.get(viewname='rest_api:importsetup-list')


class ImportSetupActionTestMixin:
    def _create_test_import_setup_action(self):
        self.test_import_setup_action = self.test_import_setup.actions.create(
            backend_path=TEST_IMPORT_SETUP_ACTION_BACKEND_PATH,
            label=TEST_IMPORT_SETUP_ACTION_LABEL,
        )


class ImportSetupActionViewTestMixin:
    def _request_test_import_setup_action_backend_selection_view(self):
        return self.post(
            viewname='importer:import_setup_action_backend_selection', kwargs={
                'import_setup_id': self.test_import_setup.pk
            }, data={
                'class_path': TEST_IMPORT_SETUP_ACTION_BACKEND_PATH,
            }
        )

    def _request_test_import_setup_action_create_view(self):
        pk_list = list(ImportSetupAction.objects.values_list('pk', flat=True))

        response = self.post(
            viewname='importer:import_setup_action_create', kwargs={
                'import_setup_id': self.test_import_setup.pk,
                'class_path': TEST_IMPORT_SETUP_ACTION_BACKEND_PATH
            }, data={
                'label': TEST_IMPORT_SETUP_ACTION_LABEL,
            }
        )

        try:
            self.test_import_setup_action = ImportSetupAction.objects.get(
                ~Q(pk__in=pk_list)
            )
        except ImportSetupAction.DoesNotExist:
            self.test_import_setup_action = None

        return response

    def _request_test_import_setup_action_delete_view(self):
        return self.post(
            viewname='importer:import_setup_action_delete', kwargs={
                'import_setup_action_id': self.test_import_setup_action.pk
            }
        )

    def _request_test_import_setup_action_edit_view(self):
        return self.post(
            viewname='importer:import_setup_action_edit', kwargs={
                'import_setup_action_id': self.test_import_setup_action.pk
            }, data={
                'label': TEST_IMPORT_SETUP_ACTION_LABEL_EDITED,
            }
        )

    def _request_test_import_setup_action_list_view(self):
        return self.get(
            viewname='importer:import_setup_action_list', kwargs={
                'import_setup_id': self.test_import_setup.pk
            }
        )


class ImportSetupItemAPIViewTestMixin:
    def _request_test_import_setup_clear_api_view(self):
        return self.post(
            viewname='rest_api:importsetup-clear', kwargs={
                'import_setup_id': self.test_import_setup.pk
            }
        )

    def _request_test_import_setup_item_delete_api_view(self):
        return self.delete(
            viewname='rest_api:importsetupitem-detail', kwargs={
                'import_setup_id': self.test_import_setup.pk,
                'import_setup_item_id': self.test_import_setup_item.pk
            }
        )

    def _request_test_import_setup_item_detail_api_view(self):
        return self.get(
            viewname='rest_api:importsetupitem-detail', kwargs={
                'import_setup_id': self.test_import_setup.pk,
                'import_setup_item_id': self.test_import_setup_item.pk
            }
        )

    def _request_test_import_setup_item_edit_via_patch_api_view(self):
        return self.patch(
            viewname='rest_api:importsetupitem-detail', kwargs={
                'import_setup_id': self.test_import_setup.pk,
                'import_setup_item_id': self.test_import_setup_item.pk
            }, data={
                'identifier': TEST_IMPORT_SETUP_ITEM_IDENTIFIER_EDITED
            }
        )

    def _request_test_import_setup_item_edit_via_put_api_view(self):
        return self.put(
            viewname='rest_api:importsetupitem-detail', kwargs={
                'import_setup_id': self.test_import_setup.pk,
                'import_setup_item_id': self.test_import_setup_item.pk
            }, data={
                'identifier': TEST_IMPORT_SETUP_ITEM_IDENTIFIER_EDITED
            }
        )

    def _request_test_import_setup_item_list_api_view(self):
        return self.get(
            viewname='rest_api:importsetupitem-list', kwargs={
                'import_setup_id': self.test_import_setup.pk
            }
        )

    def _request_test_import_setup_populate_api_view(self):
        return self.post(
            viewname='rest_api:importsetup-populate', kwargs={
                'import_setup_id': self.test_import_setup.pk
            }
        )

    def _request_test_import_setup_process_api_view(self):
        return self.post(
            viewname='rest_api:importsetup-process', kwargs={
                'import_setup_id': self.test_import_setup.pk
            }
        )


class ImportSetupTestMixin:
    def _create_test_import_setup(self):
        self.test_import_setup = ImportSetup.objects.create(
            backend_path=TEST_IMPORTER_BACKEND_PATH,
            label=TEST_IMPORT_SETUP_LABEL,
            document_type=self.test_document_type
        )


class ImportSetupItemTestMixin:
    def _create_test_import_setup_item(self):
        test_item_list = TestImporter().get_item_list()
        self.test_import_setup_item = self.test_import_setup.items.create(
            identifier=test_item_list[0].id
        )


class ImportSetupViewTestMixin:
    def _request_test_import_setup_backend_selection_view(self):
        return self.post(
            viewname='importer:import_setup_backend_selection', data={
                'backend': TEST_IMPORTER_BACKEND_PATH,
            }
        )

    def _request_test_import_setup_create_view(self):
        pk_list = list(ImportSetup.objects.values_list('pk', flat=True))

        repsonse = self.post(
            viewname='importer:import_setup_create', kwargs={
                'class_path': TEST_IMPORTER_BACKEND_PATH
            }, data={
                'document_type': self.test_document_type.pk,
                'label': TEST_IMPORT_SETUP_LABEL,
                'item_time_buffer': TEST_IMPORT_SETUP_ITEM_TIME_BUFFER,
                'process_size': TEST_IMPORT_SETUP_PROCESS_SIZE
            }
        )

        try:
            self.test_import_setup = ImportSetup.objects.get(
                ~Q(pk__in=pk_list)
            )
        except ImportSetup.DoesNotExist:
            self.test_import_setup = None

        return repsonse

    def _request_test_import_setup_delete_view(self):
        return self.post(
            viewname='importer:import_setup_delete', kwargs={
                'import_setup_id': self.test_import_setup.pk
            }
        )

    def _request_test_import_setup_edit_view(self):
        return self.post(
            viewname='importer:import_setup_edit', kwargs={
                'import_setup_id': self.test_import_setup.pk
            }, data={
                'credential': self.test_stored_credential.pk,
                'document_type': self.test_document_type.pk,
                'item_time_buffer': TEST_IMPORT_SETUP_ITEM_TIME_BUFFER,
                'label': TEST_IMPORT_SETUP_LABEL_EDITED,
                'process_size': TEST_IMPORT_SETUP_PROCESS_SIZE
            }
        )

    def _request_test_import_setup_list_view(self):
        return self.get(viewname='importer:import_setup_list')


class ImportSetupItemViewTestMixin:
    def _request_test_import_setup_clear_view(self):
        return self.post(
            viewname='importer:import_setup_clear', kwargs={
                'import_setup_id': self.test_import_setup.pk
            }
        )

    def _request_test_import_setup_item_delete_view(self):
        return self.post(
            viewname='importer:import_setup_item_delete', kwargs={
                'import_setup_item_id': self.test_import_setup_item.pk
            }
        )

    def _request_test_import_setup_item_edit_view(self):
        return self.post(
            viewname='importer:import_setup_item_edit', kwargs={
                'import_setup_item_id': self.test_import_setup_item.pk
            }, data={
                'identifier': TEST_IMPORT_SETUP_ITEM_IDENTIFIER_EDITED,
                'state': self.test_import_setup_item.state
            }
        )

    def _request_test_import_setup_process_view(self):
        return self.post(
            viewname='importer:import_setup_process', kwargs={
                'import_setup_id': self.test_import_setup.pk
            }
        )

    def _request_test_import_setup_populate_view(self):
        return self.post(
            viewname='importer:import_setup_populate', kwargs={
                'import_setup_id': self.test_import_setup.pk
            }
        )
