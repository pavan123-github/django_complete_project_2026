from rest_framework import serializers
from .models import Profile,Book


#is serializer class convert python object data into json format and validating data 
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        
        
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        