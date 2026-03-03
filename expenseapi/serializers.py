from django.contrib.auth.models import User
from .models import Transaction
from rest_framework import serializers


#Creating a JSON serializer to convert python to JSON for Users
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password":{"write_only":True}} # This allows users to change the password
        
    # create a new version of  validated users 
    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        return user
        
        
# Create  a  Json Serializer for the the Notes created
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "title", "transaction_type", "category","author", "description", "amount","created_at", "updated_at", "date"]
        extra_kwargs = {"author":{"read_only": True}} # This restrict the name of the author to read only to prevent editing of author