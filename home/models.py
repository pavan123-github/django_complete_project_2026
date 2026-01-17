from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=30)
    country = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    

class Book(models.Model):
    title = models.CharField(max_length=50)
    publication_date = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE,related_name='books')
    def __str__(self):
        return self.title 
