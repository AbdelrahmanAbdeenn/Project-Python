from unittest.mock import Mock

import pytest

from src.domain.member_entity import Member
from src.application.member_services import MemberServices


@pytest.fixture
def member_services():
    service = MemberServices()
    service.repo = Mock()
    service.repo.primary_key_column = "member_id"
    return service

# ========== MEMBER CRUD TESTING ==========

def test_create_member_success(member_services):
    mock_member = Mock(spec=Member)
    mock_member.member_id = 1
    mock_member.name = "John Doe"
    mock_member.email = "john@example.com"

    member_services.repo.entity_type.return_value = mock_member
    member_services.repo.get_by_id.return_value = None
    member_services.repo.add.return_value = mock_member 

    response = member_services.create({"name": "John Doe", "email": "john@example.com"})

    assert response.name == "John Doe"
    assert response.email  == "john@example.com"

def test_get_member_success(member_services):
    mock_member = Mock(spec=Member)
    mock_member.member_id = 1
    mock_member.name = "John Doe"
    mock_member.email = "john@example.com"

    member_services.repo.get_by_id.return_value = mock_member

    response = member_services.get(1)
    assert response.name == "John Doe"
    assert response.email == "john@example.com"

def test_update_member_success(member_services):
    existing_member = Mock(spec=Member)
    existing_member.member_id = 1
    existing_member.name = "Old Name"
    existing_member.email = "old@example.com"

    updated_member = Mock(spec=Member)
    updated_member.member_id = 1
    updated_member.name = "Jane Doe"
    updated_member.email = "jane@example.com"

    member_services.repo.get_by_id.return_value = existing_member
    member_services.repo.update.return_value = True
    member_services.repo.get_by_id.return_value = updated_member  # ✅ Ensure updated member is returned

    response = member_services.update(1, {"name": "Jane Doe", "email": "jane@example.com"})

    assert response.name == "Jane Doe"
    assert response.email == "jane@example.com"

def test_delete_member_success(member_services):
    mock_member = Mock(spec=Member)
    mock_member.member_id = 1

    member_services.repo.get_by_id.return_value = mock_member
    member_services.repo.delete.return_value = True

    response = member_services.delete(1)

    assert response["message"] == "Entity deleted successfully"

# ========== MEMBER ERROR HANDLING ==========

def test_get_member_not_found(member_services):
    member_services.repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Entity not found"):
        member_services.get(99)


def test_create_member_duplicate(member_services):
    existing_member = Mock(spec=Member, member_id=1, name="John Doe", email="john@example.com")

    member_services.repo.entity_type.return_value = existing_member
    member_services.repo.get_by_id.return_value = existing_member

    with pytest.raises(ValueError, match="Entity with this member_id already exists"):
        member_services.create({"name": "John Doe", "email": "john@example.com"})