from django.db import models
from django.contrib.auth.models import User 

class Author(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)
    country = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
#Related to onetomany relationship with using Foreign key Authors + Books
class Book(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    publication_date = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE,related_name='books')
    def __str__(self):
        return self.title 

# only for pagination
class State(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    state_code = models.IntegerField()
    def __str__(self):
        return self.name

#Using RestApi + OneToOne Relationalship + Pagination    
class Profile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=50, blank=True)
    birth_data = models.DateField(null=True, blank=True)
    def __str__(self):
        return f'{self.user.username} profile'


class SparePart(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    price = models.IntegerField()
    vahical_type = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Vehical(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    year = models.DateField()
    price = models.FloatField()
    def __str__(self):
        return self.name

# only for class based views
class Garment(models.Model):
    name = models.CharField(max_length=100)
    manufacture_city = models.CharField(max_length=100)
    fabric = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
#for mixins in django
class Devise(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    def __str__(self):
        return self.name

    