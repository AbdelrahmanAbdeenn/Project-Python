from datetime import datetime
from unittest.mock import Mock

import pytest

from src.domain.book_entity import Book
from src.application.book_services import BookServices


@pytest.fixture
def book_services():
    service = BookServices()
    service.repo = Mock()
    service.repo.primary_key_column = "book_id"
    service.member_repo = Mock()
    return service

# ========== BOOK CRUD TESTING ==========

def test_create_book_success(book_services):
    mock_book = Mock(spec=Book, book_id=1, title="1984", author="George Orwell")

    book_services.repo.entity_type.return_value = mock_book
    book_services.repo.get_by_id.return_value = None 
    book_services.repo.add.return_value = True

    response = book_services.create({"title": "1984", "author": "George Orwell"})

    assert response.title == "1984"
    assert response.author == "George Orwell"

def test_get_book_success(book_services):
    mock_book = Mock(spec=Book, book_id=1, title="1984", author="George Orwell")
    book_services.repo.get_by_id.return_value = mock_book
    response = book_services.get(1)
    assert response.title == "1984"
    assert response.author == "George Orwell"

def test_update_book_success(book_services):
    """Test updating a book."""
    existing_book = Mock(spec=Book, book_id=1, title="Old Title", author="Old Author")
    updated_book = Mock(spec=Book, book_id=1, title="Animal Farm", author="George Orwell")

    book_services.repo.get_by_id.return_value = existing_book
    book_services.repo.update.return_value = True
    book_services.repo.get_by_id.return_value = updated_book

    response = book_services.update(1, {"title": "Animal Farm", "author": "George Orwell"})

    assert response.title == "Animal Farm"
    assert response.author == "George Orwell"

def test_delete_book_success(book_services):
    mock_book = Mock(spec=Book, book_id=1)

    book_services.repo.get_by_id.return_value = mock_book
    book_services.repo.delete.return_value = True

    response = book_services.delete(1)

    assert response["message"] == "Entity deleted successfully"

# ========== BOOK ERROR HANDLING ==========

def test_get_book_not_found(book_services):
    book_services.repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Entity not found"):
        book_services.get(99)

def test_update_book_not_found(book_services):
    book_services.repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Entity not found"):
        book_services.update(99, {"title": "Animal Farm", "author": "George Orwell"})

def test_delete_book_not_found(book_services):
    book_services.repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Entity not found"):
        book_services.delete(99)

# ========== BOOK BORROWING & RETURNING ==========

def test_borrow_book_success(book_services):
    book = Mock(book_id=1, is_borrowed=False)
    member = Mock(member_id=1)

    book_services.repo.get_by_id.return_value = book
    book_services.member_repo.get_by_id.return_value = member
    book_services.repo.update.return_value = True

    response = book_services.borrow_book(1, 1)

    assert response["message"] == "Book borrowed successfully"

def test_borrow_book_already_borrowed(book_services):
    book = Mock(book_id=1, is_borrowed=True, borrowed_by=2, borrowed_date=datetime(2025, 3, 13, 14, 30, 0))
    book_services.repo.get_by_id.return_value = book

    expected_message = f"Book is already borrowed by member {book.borrowed_by} since {book.borrowed_date.strftime('%Y-%m-%d %H:%M:%S')}"

    with pytest.raises(ValueError, match=expected_message):
        book_services.borrow_book(1, 1)

def test_return_book_success(book_services):
    book = Mock(book_id=1, is_borrowed=True)
    book_services.repo.get_by_id.return_value = book
    book_services.repo.update.return_value = True

    response = book_services.return_book(1)

    assert response["message"] == "Book returned successfully"

def test_return_book_not_found(book_services):
    book_services.repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Book not found"):
        book_services.return_book(99)

def test_return_book_not_borrowed(book_services):
    book = Mock(book_id=1, is_borrowed=False)
    book_services.repo.get_by_id.return_value = book

    with pytest.raises(ValueError, match="Book is not currently borrowed"):
        book_services.return_book(1)
