from django.shortcuts import render
from .serializers import UserSerializer, TransactionSerializer, CategorySerializer
from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Transaction, Category
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum


# Create your views here.

# View to register users.
class CreateUserView(generics.CreateAPIView): # create a new user
    queryset = User.objects.all() # list of all the user objects available 
    serializer_class = UserSerializer # Tells what kind of data to create a new user 
    permission_classes = [AllowAny] # Allow anyone to create a new user


# View for creating transactions, edit, filter,  delete (CRUD) 
class TransactionViewSet(viewsets.ModelViewSet):

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = [
        "category",
        "transaction_type",
        "date",
    ]

    ordering_fields = ["date", "amount"]

    def get_queryset(self):

        department = self.request.user.userdetail.department

        return Transaction.objects.filter(
            department=department,
            is_deleted=False
        )
    def perform_create(self, serializer):

        department = self.request.user.userdetail.department

        serializer.save(
            author=self.request.user,
            department=department
        )
        
    def delete(self, request, *args, **kwargs):

        instance = self.get_object()
        instance.is_deleted = True
        instance.save()

        return Response({"message": "Transaction deleted successfully"})

#Views for the category 
class CategoryViewSet(viewsets.ModelViewSet):

    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    
    
# Views for Category expense
class CategoryExpenseView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        department = self.request.user.userdetail.department

        data = (
            Transaction.objects
            .filter(
                department=department,
                transaction_type="Expense",
                is_deleted=False
            )
            .values("category__category_name")
            .annotate(total=Sum("amount"))
        )

        return Response(data)


# views for the dashboard
class DashboardView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        department = self.request.user.userdetail.department

        transactions = Transaction.objects.filter(
            department=department,
            is_deleted=False
        )

        total_income = transactions.filter(transaction_type="Income").aggregate(
            total=Sum("amount")
        )["total"] or 0

        total_expense = transactions.filter(transaction_type="Expense").aggregate(
            total=Sum("amount")
        )["total"] or 0

        balance = total_income - total_expense

        return Response({
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance
        })
        
        
        


# class TransactionListCreate(generics.ListCreateAPIView): # list new transaction user has created or create a new note
#     serializer_class = TransactionSerializer
#     permission_classes= [IsAuthenticated] # Only authenticated users can create new notes
    
#     # allows request for the user in department to be the authors
#     def get_queryset(self):
#         department= self.request.user.userdetail.department
#         return Transaction.objects.filter(department=department, is_deleted=False) # allows to filter transactions only written by the users in the department
    
#     # Allows serializer object to validate the new transactions and save users in department.
#     def perform_create(self, serializer):
#         department = self.request.user.userdetail.department
#         serializer.save(
#             author=self.request.user,
#             department=department
#         )
    
# # Views for transaction details to edit and delete
# class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = TransactionSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         department = self.request.user.userdetail.department
#         return Transaction.objects.filter(
#             department=department,
#             is_deleted=False
#         )

#     def perform_destroy(self, instance):
#         instance.is_deleted = True   
#         instance.save()
