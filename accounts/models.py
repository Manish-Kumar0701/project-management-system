from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    DEVELOPER = "dev"
    BOD = "bod"
    PROJECT_MANAGER = "pm"
    COO = "coo"
    ROLE_CHOICES = [
        (DEVELOPER, "Developer"),
        (BOD, "Board of Directors"),
        (PROJECT_MANAGER, "Project Manager"),
        (COO, "Chief Operating Officer"),
    ]

    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default=DEVELOPER,
    )

    def __str__(self):
        return self.user.username
    


class Status(models.IntegerChoices):
    NOT_STARTED = 0, 'Not Started'
    IN_PROGRESS = 1, 'In Progress'
    COMPLETED = 2, 'Completed'
    CANCELLED = 3, 'Cancelled'

class Project(models.Model):
    project_name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=Status.choices, default=Status.NOT_STARTED)

    def __str__(self):
        return self.project_name

    
class Task(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title
    


class ProjectTasks(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(
        'Status',
        choices=Status.choices,
        default=Status.NOT_STARTED
    )
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    assigned_on = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.project_id.project_name} - {self.task_id.title}"



class ProjectMembers(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    member_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_project_lead = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.project_id.project_name} - {self.member_id.username}"


class Report(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Report - {self.title}"
