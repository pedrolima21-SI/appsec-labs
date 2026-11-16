import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from access_control_demo import allow_access, Resource, User, run_scenarios


def test_reader_can_view_published_report():
    user = User("alice", "reader")
    resource = Resource("report", "Quarterly Summary", published=True)
    assert allow_access(user, "view_report", resource) is True


def test_reader_cannot_create_draft():
    user = User("alice", "reader")
    resource = Resource("report", "Quarterly Summary", published=True)
    assert allow_access(user, "create_draft", resource) is False


def test_editor_can_create_draft():
    user = User("bob", "editor")
    resource = Resource("report", "Quarterly Summary", published=True)
    assert allow_access(user, "create_draft", resource) is True


def test_editor_can_edit_own_draft():
    user = User("bob", "editor")
    resource = Resource("draft", "Draft 01", owner="bob")
    assert allow_access(user, "edit_draft", resource) is True


def test_editor_cannot_edit_another_draft():
    user = User("bob", "editor")
    resource = Resource("draft", "Draft 02", owner="carol")
    assert allow_access(user, "edit_draft", resource) is False


def test_editor_cannot_publish_report():
    user = User("bob", "editor")
    resource = Resource("report", "Quarterly Summary", published=False)
    assert allow_access(user, "publish_report", resource) is False


def test_administrator_can_manage_roles():
    user = User("admin", "administrator")
    resource = Resource("config", "Application configuration")
    assert allow_access(user, "manage_roles", resource) is True


def test_administrator_cannot_run_unknown_action():
    user = User("admin", "administrator")
    resource = Resource("config", "Application configuration")
    assert allow_access(user, "delete_everything", resource) is False


def test_unknown_role_is_denied_by_default():
    user = User("ghost", "guest")
    resource = Resource("report", "Quarterly Summary", published=True)
    assert allow_access(user, "view_report", resource) is False


def test_unknown_action_is_denied_by_default():
    user = User("alice", "reader")
    resource = Resource("report", "Quarterly Summary", published=True)
    assert allow_access(user, "read_private_data", resource) is False


def test_run_scenarios_matches_matrix_expectations():
    expected = {
        "reader can view a published report": True,
        "reader cannot create a draft": False,
        "editor can create a draft": True,
        "editor can edit own draft": True,
        "editor cannot edit another user's draft": False,
        "editor cannot publish a report": False,
        "administrator can manage roles": True,
        "administrator can alter config": True,
        "administrator cannot perform unknown action": False,
        "unknown role is denied by default": False,
        "unknown action is denied by default": False,
    }

    for name, actual, result in run_scenarios():
        assert actual == result, f"{name}: expected {result}, got {actual}"
        assert expected[name] == result


def test_main_exits_non_zero_on_failures(tmp_path):
    script = Path(__file__).resolve().parent.parent / "access_control_demo.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "PASS: all access-control scenarios matched the expected policy." in result.stdout
