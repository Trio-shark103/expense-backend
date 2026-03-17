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
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth


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
        
    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        instance.is_deleted = True
        instance.save()

        return Response({"message": "Transaction deleted successfully"})

#Views for the category 
class CategoryViewSet(viewsets.ModelViewSet):

    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        # department = self.request.user.userdetail.department

        return Category.objects.filter(
            # department=department,
            is_deleted=False
        )

    def perform_create(self, serializer):

        # department = self.request.user.userdetail.department

        serializer.save()
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()

        return Response({"message": "Category has deleted successfully"})
    
    
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
            .values(category_name=F("category__category_name"))
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
            "balance": balance,
            "currency": "GH₵"
        })
        
# view for monthly expense       
class MonthlyExpenseView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        department = request.user.userdetail.department

        data = (
            Transaction.objects
            .filter(
                department=department,
                transaction_type="Expense",
                is_deleted=False
            )
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(total=Sum("amount"))
            .order_by("month")
        )

        return Response(data)       

# views for the top 5 categories expense
class TopCategoryExpenseView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        department = request.user.userdetail.department

        data = (
            Transaction.objects
            .filter(
                department=department,
                transaction_type="Expense",
                is_deleted=False
            )
            .values(category_name=F("category__category_name"))
            .annotate(total=Sum("amount"))
            .order_by("-total")[:5]   
        )

        return Response(data)

#       
