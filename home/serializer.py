from rest_framework import serializers
from .models import Profile,Book,SparePart,Vehical,Garment,Devise


#is serializer class convert python object data into json format and validating data 
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        
        
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class SparePartSerializer(serializers.ModelSerializer):
    class Meta:
        model = SparePart
        fields = '__all__'

class VehicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehical 
        fields = '__all__'

class GarmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garment
        fields = '__all__'

class DeviseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devise
        fields = '__all__'