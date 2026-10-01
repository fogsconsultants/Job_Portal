from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Sectors(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Company(models.Model):
    name=models.CharField(max_length=50,unique=True)
    address=models.CharField(max_length=300)
    website=models.URLField()
    def __str__(self):
        return self.name

    
class Jobs(models.Model):
    title=models.CharField(max_length=100)
    sector=models.ForeignKey(Sectors,on_delete=models.CASCADE)
    location=models.CharField(max_length=50)
    description=models.TextField()
    salary=models.CharField(max_length=50)
    post_date=models.DateField(auto_now_add=True)
    slug=models.SlugField(blank=True)
    is_active=models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="posted_jobs")
    employment_type = models.CharField(max_length=30, default="Full-time")
    def __str__(self):
        return self.title

class Applications(models.Model):
    job=models.ForeignKey(Jobs,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Submitted")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["job", "user"], name="unique_job_application")
        ]

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"
