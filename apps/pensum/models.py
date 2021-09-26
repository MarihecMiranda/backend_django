from django.db import models

# Create your models here.
class Programa(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    num_semesters=models.PositiveIntegerField()    
    state = models.CharField(max_length=1,default="A")
    def __str__(self):
        return self.name
    class Meta:  
        db_table = 'programa'

class Pensum(models.Model):
    description = models.CharField(max_length=255)
    uploadedFile = models.FileField(upload_to = "Uploaded Files/") #require pillow
    date_issue = models.DateField(auto_now =False, auto_now_add=False)
    expiration_date = models.DateField(auto_now =False, auto_now_add=False)
    state = models.CharField(max_length=1,default="A")
    programa_id = models.ForeignKey(Programa, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:  
        db_table = 'pensum'