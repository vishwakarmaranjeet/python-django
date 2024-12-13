from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from django.shortcuts import render
from .models import Book
from .serializers import BookSerializer
# Create your views here.

def home(request):
    return render(request, "home.html", {"name": "Ranjeet"})

def add(request):
    num1 = int(request.POST["num1"])
    num2 = int(request.POST["num2"])
    result = num1 + num2
    return render(request, "result.html", {"result": result})

def home_view(request):
    # Fetch all Book objects from the database
    books = Book.objects.all() # This returns a queryset of all books
    return render(request, "home.html", {"books": books })

class BookListView(APIView):
    def get(self, request):
        try:
            # Fetching all books from the database
            books = Book.objects.all()

            # If no books are found, raise a NotFound exception
            if not books:
                raise NotFound(detail="No books found", code=404)

            # Serializing the books data
            serializer = BookSerializer(books, many=True)

            # Return the serialized data with a 200 status code
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Book.DoesNotExist:
            # Handle case where Book model is not found in the database
            return Response({"error": "Books not found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Handle any unexpected error
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BookCreateView(APIView):
    def post(self, request):
        try:
            # Deserialize the incoming data
            serializer = BookSerializer(data=request.data)

            # Validate the data
            if serializer.is_valid():
                # Save the new book object to the database
                serializer.save()

                # Return a success response with the serialized book data
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            # If the data is not valid, return validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
