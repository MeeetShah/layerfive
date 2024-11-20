from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

class BookListCreateView(APIView):
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from .models import Book, Borrower, Loan

class BorrowBookView(APIView):
    def post(self, request):
        book_id = request.data.get('book_id')
        borrower_id = request.data.get('borrower_id')

        # Validate borrower
        borrower = get_object_or_404(Borrower, id=borrower_id)
        if not borrower.is_active:
            raise ValidationError("Borrower is not active.")

        # Check borrowing limit
        active_loans = Loan.objects.filter(borrower=borrower, is_returned=False).count()
        if active_loans >= 3:
            raise ValidationError("Borrowing limit reached. Maximum 3 books allowed.")

        # Validate book
        book = get_object_or_404(Book, id=book_id)
        if not book.available:
            raise ValidationError("Book is not available for borrowing.")

        # Create a loan
        loan = Loan.objects.create(book=book, borrower=borrower)
        book.available = False
        book.borrow_count += 1
        book.save()

        return Response({"message": f"{book.title} borrowed successfully."}, status=status.HTTP_201_CREATED)


class ReturnBookView(APIView):
    def post(self, request):
        book_id = request.data.get('book_id')

        # Validate loan
        loan = get_object_or_404(Loan, book_id=book_id, is_returned=False)
        loan.is_returned = True
        loan.returned_at = timezone.now()
        loan.save()

        # Update book availability
        book = loan.book
        book.available = True
        book.save()

        return Response({"message": f"{book.title} returned successfully."}, status=status.HTTP_200_OK)

class ActiveBorrowedBooksView(APIView):
    def get(self, request, borrower_id):
        borrower = get_object_or_404(Borrower, id=borrower_id)
        loans = Loan.objects.filter(borrower=borrower, is_returned=False)
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)

class BorrowerHistoryView(APIView):
    def get(self, request, borrower_id):
        borrower = get_object_or_404(Borrower, id=borrower_id)
        loans = Loan.objects.filter(borrower=borrower)
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)
