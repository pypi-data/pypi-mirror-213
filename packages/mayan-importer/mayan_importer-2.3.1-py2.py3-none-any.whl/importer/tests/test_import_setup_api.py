from rest_framework import status

from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import event_import_setup_created, event_import_setup_edited
from ..models import ImportSetup
from ..permissions import (
    permission_import_setup_create, permission_import_setup_delete,
    permission_import_setup_edit, permission_import_setup_view
)
from .mixins import ImportSetupAPIViewTestMixin, ImportSetupTestMixin


class ImportSetupAPIViewTestCase(
    DocumentTestMixin, ImportSetupAPIViewTestMixin, ImportSetupTestMixin,
    BaseAPITestCase
):
    auto_upload_test_document = False

    def test_import_setup_create_api_view_no_permission(self):
        import_setup_count = ImportSetup.objects.count()

        self._clear_events()

        response = self._request_test_import_setup_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(ImportSetup.objects.count(), import_setup_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_create_api_view_with_access(self):
        import_setup_count = ImportSetup.objects.count()

        self.grant_permission(permission=permission_import_setup_create)

        self._clear_events()

        response = self._request_test_import_setup_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            ImportSetup.objects.count(), import_setup_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self.test_import_setup)
        self.assertEqual(events[0].target, self.test_import_setup)
        self.assertEqual(events[0].verb, event_import_setup_created.id)

    def test_import_setup_delete_api_view_no_permission(self):
        self._create_test_import_setup()

        import_setup_count = ImportSetup.objects.count()

        self._clear_events()

        response = self._request_test_import_setup_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            ImportSetup.objects.count(), import_setup_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_delete_api_view_with_access(self):
        self._create_test_import_setup()

        import_setup_count = ImportSetup.objects.count()

        self.grant_access(
            obj=self.test_import_setup,
            permission=permission_import_setup_delete
        )

        self._clear_events()

        response = self._request_test_import_setup_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(
            ImportSetup.objects.count(), import_setup_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_detail_api_view_no_permission(self):
        self._create_test_import_setup()

        self._clear_events()

        response = self._request_test_import_setup_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('id' not in response.data)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_detail_api_view_with_access(self):
        self._create_test_import_setup()

        self.grant_access(
            obj=self.test_import_setup,
            permission=permission_import_setup_view
        )

        self._clear_events()

        response = self._request_test_import_setup_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['id'], self.test_import_setup.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_edit_via_patch_api_view_no_permssion(self):
        self._create_test_import_setup()

        import_setup_label = self.test_import_setup.label

        self._clear_events()

        response = self._request_test_import_setup_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_import_setup.refresh_from_db()
        self.assertEqual(
            self.test_import_setup.label, import_setup_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_edit_via_patch_api_view_with_access(self):
        self._create_test_import_setup()

        import_setup_label = self.test_import_setup.label

        self.grant_access(
            obj=self.test_import_setup,
            permission=permission_import_setup_edit
        )

        self._clear_events()

        response = self._request_test_import_setup_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_import_setup.refresh_from_db()
        self.assertNotEqual(
            self.test_import_setup.label, import_setup_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self.test_import_setup)
        self.assertEqual(events[0].target, self.test_import_setup)
        self.assertEqual(events[0].verb, event_import_setup_edited.id)

    def test_import_setup_edit_via_put_api_view_no_permission(self):
        self._create_test_import_setup()

        import_setup_label = self.test_import_setup.label

        self._clear_events()

        response = self._request_test_import_setup_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_import_setup.refresh_from_db()
        self.assertEqual(
            self.test_import_setup.label, import_setup_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_edit_via_put_api_view_with_access(self):
        self._create_test_import_setup()

        import_setup_label = self.test_import_setup.label

        self.grant_access(
            obj=self.test_import_setup,
            permission=permission_import_setup_edit
        )

        self._clear_events()

        response = self._request_test_import_setup_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_import_setup.refresh_from_db()
        self.assertNotEqual(
            self.test_import_setup.label, import_setup_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self.test_import_setup)
        self.assertEqual(events[0].target, self.test_import_setup)
        self.assertEqual(events[0].verb, event_import_setup_edited.id)

    def test_import_setup_list_api_view_no_permission(self):
        self._create_test_import_setup()

        self._clear_events()

        response = self._request_test_import_setup_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_list_api_view_with_access(self):
        self._create_test_import_setup()

        self.grant_access(
            obj=self.test_import_setup,
            permission=permission_import_setup_view
        )

        self._clear_events()

        response = self._request_test_import_setup_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['id'], self.test_import_setup.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
