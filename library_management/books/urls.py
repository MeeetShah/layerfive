from django.urls import path
from .views import BookListCreateView
from django.urls import path
from .views import (
    BookListCreateView,
    BorrowBookView,
    ReturnBookView,
    ActiveBorrowedBooksView,
    BorrowerHistoryView,
)


urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('borrow/', BorrowBookView.as_view(), name='borrow-book'),
    path('return/', ReturnBookView.as_view(), name='return-book'),
    path('borrowed/<int:borrower_id>/', ActiveBorrowedBooksView.as_view(), name='active-borrowed-books'),
    path('history/<int:borrower_id>/', BorrowerHistoryView.as_view(), name='borrower-history'),
]

