from django.shortcuts import render
from .serializers import UserSerializer, TransactionSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Transaction
# Create your views here.

class CreateUserView(generics.CreateAPIView): # create a new user
    queryset = User.objects.all() # list of all the user objects available 
    serializer_class = UserSerializer # Tells what kind of data to create a new user 
    permission_classes = [AllowAny] # Allow anyone to create a new user


# View for creating transactions 
class TransactionListCreate (generics.ListCreateAPIView): # list new transaction user has created or create a new note
    serializer_class = TransactionSerializer
    permission_classes= [IsAuthenticated] # Only authenticated users can create new notes
    
    # allows request for the user to enable the author
    def get_queryset(self):
        user= self.request.user
        return Transaction.objects.filter(author=user) # allows to filter transactions only written by the user
    
    # Allows serializer object to validate the new transactions and save users.
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)