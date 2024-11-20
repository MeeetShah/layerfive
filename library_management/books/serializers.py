# from rest_framework import serializers
# from .models import Book, Borrower, Loan

# class BookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields = '__all__'

# class BorrowerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Borrower
#         fields = '__all__'

# class LoanSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Loan
#         fields = '__all__'


from rest_framework import serializers
from .models import Book, Borrower, Loan

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    borrower_name = serializers.CharField(source='borrower.name', read_only=True)

    class Meta:
        model = Loan
        fields = [
            'id', 'book', 'book_title', 'borrower', 'borrower_name',
            'borrowed_at', 'returned_at', 'is_returned'
        ]
