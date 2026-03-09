from django.contrib.auth.models import User
from .models import Transaction, UserDetail, Category
from rest_framework import serializers


#Creating a JSON serializer to convert python to JSON for Users
class UserSerializer(serializers.ModelSerializer):
    department_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", 'department_id' ]
        extra_kwargs = {"password":{"write_only":True}} # This allows users to change the password
        
    # create a new version of  validated users 
    def create(self,validated_data):
        department_id= validated_data.pop('department_id')
        user = User.objects.create_user(**validated_data)
        UserDetail.objects.create(
            user = user,
            department = department_id
        )
        return user
        
        
# Create  a  Json Serializer for the the transactions created
class TransactionSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    department = serializers.StringRelatedField()
    class Meta:
        model = Transaction
        fields = ["id", "transaction_type", "category","author","department", "narration", "amount","created_at", "updated_at", "date"]
        extra_kwargs = {"author":{"read_only": True},
                        "department": {"read_only": True}} # This restrict the name of the author to read only to prevent editing of author, department


# Create a JSON Serializer for categories created
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"