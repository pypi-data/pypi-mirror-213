from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from credentials.tests.mixins import StoredCredentialTestMixin

from ..events import event_import_setup_edited
from ..models import ImportSetupAction
from ..permissions import (
    permission_import_setup_edit, permission_import_setup_view
)

from .mixins import (
    ImportSetupActionTestMixin, ImportSetupActionViewTestMixin,
    ImportSetupTestMixin
)


class ImportSetupActionViewTestCase(
    StoredCredentialTestMixin, ImportSetupActionTestMixin,
    ImportSetupActionViewTestMixin, ImportSetupTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_stored_credential()
        self._create_test_import_setup()

    def test_import_setup_action_backend_selection_view_no_permissions(self):
        import_setup_action_count = ImportSetupAction.objects.count()

        self._clear_events()

        response = self._request_test_import_setup_action_backend_selection_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            ImportSetupAction.objects.count(), import_setup_action_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_action_backend_selection_view_with_permissions(self):
        self.grant_access(
            obj=self.test_import_setup,
            permission=permission_import_setup_edit
        )
        import_setup_action_count = ImportSetupAction.objects.count()

        self._clear_events()

        response = self._request_test_import_setup_action_backend_selection_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            ImportSetupAction.objects.count(), import_setup_action_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_action_create_view_no_permissions(self):
        import_setup_action_count = ImportSetupAction.objects.count()

        self._clear_events()

        response = self._request_test_import_setup_action_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            ImportSetupAction.objects.count(), import_setup_action_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_action_create_view_with_permissions(self):
        self.grant_access(
            obj=self.test_import_setup, permission=permission_import_setup_edit
        )
        import_setup_action_count = ImportSetupAction.objects.count()

        self._clear_events()

        response = self._request_test_import_setup_action_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            ImportSetupAction.objects.count(), import_setup_action_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object, self.test_import_setup_action
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_import_setup)
        self.assertEqual(events[0].verb, event_import_setup_edited.id)

    def test_import_setup_action_delete_view_no_permissions(self):
        self._create_test_import_setup_action()

        import_setup_action_count = ImportSetupAction.objects.count()

        self._clear_events()

        response = self._request_test_import_setup_action_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            ImportSetupAction.objects.count(), import_setup_action_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_action_delete_view_with_access(self):
        self._create_test_import_setup_action()

        self.grant_access(
            obj=self.test_import_setup,
            permission=permission_import_setup_edit
        )

        import_setup_action_count = ImportSetupAction.objects.count()

        self._clear_events()

        response = self._request_test_import_setup_action_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            ImportSetupAction.objects.count(), import_setup_action_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_action_edit_view_no_permissions(self):
        self._create_test_import_setup_action()

        import_setup_action_label = self.test_import_setup_action.label

        self._clear_events()

        response = self._request_test_import_setup_action_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_import_setup_action.refresh_from_db()
        self.assertEqual(
            self.test_import_setup_action.label, import_setup_action_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_action_edit_view_with_access(self):
        self._create_test_import_setup_action()

        self.grant_access(
            obj=self.test_import_setup,
            permission=permission_import_setup_edit
        )

        self._clear_events()

        import_setup_action_label = self.test_import_setup_action.label

        response = self._request_test_import_setup_action_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_import_setup_action.refresh_from_db()
        self.assertNotEqual(
            self.test_import_setup_action.label, import_setup_action_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object, self.test_import_setup_action
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_import_setup)
        self.assertEqual(events[0].verb, event_import_setup_edited.id)

    def test_import_setup_action_list_view_with_no_permission(self):
        self._create_test_import_setup_action()

        self._clear_events()

        response = self._request_test_import_setup_action_list_view()
        self.assertNotContains(
            response=response, text=self.test_import_setup_action.label,
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_import_setup_action_list_view_with_access(self):
        self._create_test_import_setup_action()

        self.grant_access(
            obj=self.test_import_setup,
            permission=permission_import_setup_view
        )

        self._clear_events()

        response = self._request_test_import_setup_action_list_view()
        self.assertContains(
            response=response, text=self.test_import_setup_action.label,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
