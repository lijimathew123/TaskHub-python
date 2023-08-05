from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import now

class Employee(models.Model):
    
    
    ROLE_CHOICES = (
        ('Project Manager', 'Project Manager'),
        ('Project Developer', 'Project Developer')
    )

    DOMAIN_CHOICES = [
        ('Designer', 'Designer'),
        ('Developer', 'Developer'),
        ('Tester', 'Tester'),
        ('Client Communication', 'Client Communication'),
    ]
     
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    domain = models.CharField(max_length=20,choices = DOMAIN_CHOICES,blank=True,null=True)
    technologies_used = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
    

    

class Group(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True, default=None)
    developers = models.ManyToManyField(Employee, related_name='groups')
    creator = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='created_groups',null=True, blank=True, default=None)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    
    

class Task(models.Model):
    PRIORITY_CHOICES = (
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low')
    )

    STATUS_CHOICES = (
        ('Not Started','Not Started'),
        ('Start','Start'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    )
    
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=100, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=150, choices=STATUS_CHOICES)
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE)
   

    def __str__(self):
        return self.title


class Activity(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return self.title
    
    
class TaskNote(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    note = models.TextField()
    created_on = models.DateTimeField(default=now) 

    def __str__(self):
        return self.note