import pytest
from unittest.mock import Mock
from datetime import datetime
from src.application.book_services import BookServices

@pytest.fixture
def book_services(mocker):
    """Fixture to initialize BookServices with mock repositories."""
    service = BookServices()
    service.repo = Mock()
    service.member_repo = Mock()
    return service

def test_borrow_book_success(book_services):
    """Test successful book borrowing."""
    book = Mock(book_id=1, is_borrowed=False)
    member = Mock(member_id=1)

    book_services.repo.get_by_id.return_value = book
    book_services.member_repo.get_by_id.return_value = member
    book_services.repo.update.return_value = True

    response, status = book_services.borrow_book(1, 1)

    assert status == 200
    assert response["message"] == "Book borrowed successfully"

def test_borrow_book_already_borrowed(book_services):
    """Test attempting to borrow an already borrowed book."""
    book = Mock(book_id=1, is_borrowed=True)
    book_services.repo.get_by_id.return_value = book

    with pytest.raises(ValueError, match="Book is already borrowed"):
        book_services.borrow_book(1, 1)

def test_borrow_book_not_found(book_services):
    """Test attempting to borrow a non-existent book."""
    book_services.repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Book not found"):
        book_services.borrow_book(99, 1)

def test_borrow_book_member_not_found(book_services):
    """Test attempting to borrow a book with a non-existent member."""
    book = Mock(book_id=1, is_borrowed=False)
    book_services.repo.get_by_id.return_value = book
    book_services.member_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Member not found"):
        book_services.borrow_book(1, 99)

def test_return_book_success(book_services):
    """Test successful book return."""
    book = Mock(book_id=1, is_borrowed=True)
    book_services.repo.get_by_id.return_value = book
    book_services.repo.update.return_value = True

    response, status = book_services.return_book(1)

    assert status == 200
    assert response["message"] == "Book returned successfully"

def test_return_book_not_found(book_services):
    """Test attempting to return a non-existent book."""
    book_services.repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Book not found"):
        book_services.return_book(99)

def test_return_book_not_borrowed(book_services):
    """Test attempting to return a book that was never borrowed."""
    book = Mock(book_id=1, is_borrowed=False)
    book_services.repo.get_by_id.return_value = book

    with pytest.raises(ValueError, match="Book is not currently borrowed"):
        book_services.return_book(1)
