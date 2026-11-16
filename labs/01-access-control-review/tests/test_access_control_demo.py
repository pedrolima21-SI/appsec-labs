from access_control_demo import allow_access, Resource, User


def test_reader_can_view_published_report():
    user = User("alice", "reader")
    resource = Resource("report", "Quarterly Summary", published=True)
    assert allow_access(user, "view_report", resource) is True


def test_reader_cannot_create_draft():
    user = User("alice", "reader")
    resource = Resource("report", "Quarterly Summary", published=True)
    assert allow_access(user, "create_draft", resource) is False


def test_editor_can_edit_own_draft():
    user = User("bob", "editor")
    resource = Resource("draft", "Draft 01", owner="bob")
    assert allow_access(user, "edit_draft", resource) is True


def test_editor_cannot_edit_another_draft():
    user = User("bob", "editor")
    resource = Resource("draft", "Draft 02", owner="carol")
    assert allow_access(user, "edit_draft", resource) is False


def test_administrator_has_admin_privileges():
    user = User("admin", "administrator")
    resource = Resource("config", "Application configuration")
    assert allow_access(user, "manage_roles", resource) is True
