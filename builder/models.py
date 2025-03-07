from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    summary = models.TextField()
    experience = models.TextField()
    skills = models.TextField()
    education = models.TextField()
    
    def __str__(self):
        return self.name
