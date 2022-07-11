from django.db import models
from django.contrib.auth.models import User

# Create your models here

class StudentClassModel(models.Model):
    class_id = models.CharField(max_length=2, primary_key=True)
    full_class_name = models.CharField(max_length=50)  


class UserClassExtension(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    class_id = models.ForeignKey(StudentClassModel, on_delete=models.CASCADE)


class StudentProfileModel(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, )
    profile_picture = models.ImageField(upload_to='students_pictures')
    class_id = models.ForeignKey(StudentClassModel, on_delete=models.CASCADE)
    parent = models.OneToOneField(User, 
                primary_key=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.first_name


class TaskModel(models.Model):
    task_id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=100)
    task_description = models.TextField()
    task_add_date = models.DateField()


class StudentMarksModel(models.Model):

    class Marks(models.TextChoices):
        A = 'A'
        B = 'B'
        C = 'C'
        D = 'D'
        E = 'E'

    mark = models.CharField(max_length=1, choices=Marks.choices)
    task = models.ForeignKey(TaskModel, on_delete=models.CASCADE)
    student_id = models.ForeignKey(StudentProfileModel, 
                                on_delete=models.CASCADE)

