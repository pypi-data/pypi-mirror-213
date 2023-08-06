from rest_framework import status

from credentials.tests.mixins import StoredCredentialTestMixin
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import (
    event_import_setup_item_edited, event_import_setup_item_deleted
)
from ..permissions import (
    permission_import_setup_edit, permission_import_setup_view
)
from .mixins import (
    ImportSetupItemAPIViewTestMixin, ImportSetupItemTestMixin,
    ImportSetupTestMixin
)


class ImportSetupItemAPIViewTestCase(
    DocumentTestMixin, ImportSetupItemTestMixin,
    ImportSetupItemAPIViewTestMixin,
    ImportSetupTestMixin, StoredCredentialTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_stored_credential()
        self._create_test_import_setup()

    def test_import_setup_item_delete_api_view_no_permission(self):
        self._create_test_import_setup_item()

        import_setup_item_count = self.test_import_setup.items.count()

        self._clear_events()

        response = self._request_test_import_setup_item_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_import_setup.items.count(), import_setup_item_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_item_delete_api_view_with_access(self):
        self._create_test_import_setup_item()

        import_setup_item_count = self.test_import_setup.items.count()

        self.grant_access(
            obj=self.test_import_setup,
            permission=permission_import_setup_edit
        )

        self._clear_events()

        response = self._request_test_import_setup_item_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(
            self.test_import_setup.items.count(), import_setup_item_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self.test_import_setup)
        self.assertEqual(events[0].target, self.test_import_setup)
        self.assertEqual(events[0].verb, event_import_setup_item_deleted.id)

    def test_import_setup_item_detail_api_view_no_permission(self):
        self._create_test_import_setup_item()

        self._clear_events()

        response = self._request_test_import_setup_item_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('id' not in response.data)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_item_detail_api_view_with_access(self):
        self._create_test_import_setup_item()

        self.grant_access(
            obj=self.test_import_setup,
            permission=permission_import_setup_view
        )

        self._clear_events()

        response = self._request_test_import_setup_item_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['id'], self.test_import_setup_item.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_item_edit_via_patch_api_view_no_permssion(self):
        self._create_test_import_setup_item()

        import_setup_item_label = self.test_import_setup_item.identifier

        self._clear_events()

        response = self._request_test_import_setup_item_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_import_setup_item.refresh_from_db()
        self.assertEqual(
            self.test_import_setup_item.identifier, import_setup_item_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_item_edit_via_patch_api_view_with_access(self):
        self._create_test_import_setup_item()

        import_setup_item_label = self.test_import_setup_item.identifier

        self.grant_access(
            obj=self.test_import_setup,
            permission=permission_import_setup_edit
        )

        self._clear_events()

        response = self._request_test_import_setup_item_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_import_setup_item.refresh_from_db()
        self.assertNotEqual(
            self.test_import_setup_item.identifier, import_setup_item_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_import_setup)
        self.assertEqual(events[0].actor, self.test_import_setup_item)
        self.assertEqual(events[0].target, self.test_import_setup_item)
        self.assertEqual(events[0].verb, event_import_setup_item_edited.id)

    def test_import_setup_item_edit_via_put_api_view_no_permission(self):
        self._create_test_import_setup_item()

        import_setup_item_label = self.test_import_setup_item.identifier

        self._clear_events()

        response = self._request_test_import_setup_item_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_import_setup_item.refresh_from_db()
        self.assertEqual(
            self.test_import_setup_item.identifier, import_setup_item_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_item_edit_via_put_api_view_with_access(self):
        self._create_test_import_setup_item()

        import_setup_item_label = self.test_import_setup_item.identifier

        self.grant_access(
            obj=self.test_import_setup,
            permission=permission_import_setup_edit
        )

        self._clear_events()

        response = self._request_test_import_setup_item_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_import_setup_item.refresh_from_db()
        self.assertNotEqual(
            self.test_import_setup_item.identifier, import_setup_item_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_import_setup)
        self.assertEqual(events[0].actor, self.test_import_setup_item)
        self.assertEqual(events[0].target, self.test_import_setup_item)
        self.assertEqual(events[0].verb, event_import_setup_item_edited.id)

    def test_import_setup_item_list_api_view_no_permission(self):
        self._create_test_import_setup_item()

        self._clear_events()

        response = self._request_test_import_setup_item_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_item_list_api_view_with_access(self):
        self._create_test_import_setup_item()

        self.grant_access(
            obj=self.test_import_setup,
            permission=permission_import_setup_view
        )

        self._clear_events()

        response = self._request_test_import_setup_item_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['id'], self.test_import_setup_item.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
