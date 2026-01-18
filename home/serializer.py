from rest_framework import serializers
from .models import Profile


#is serializer class convert python object data into json format and validating data 
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        
        
