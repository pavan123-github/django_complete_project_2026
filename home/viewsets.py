from rest_framework import viewsets
from .models import Profile 
from .serializer import ProfileSerializer

#viewset provides all crud apis automatic 
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer 
    