from django.db import models
from django.contrib.auth.models import User
from embed_video.fields import EmbedVideoField

# Create your models here.


COMPONENT_TYPEs = (('file', 'file'), ('image', 'image'), ('text', 'text'), ('quiz', 'quiz'), ('video', 'video'))


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    title = models.TextField(max_length=127)
    description = models.TextField(max_length=2000)
    open = models.BooleanField(default=False)
    category = models.ForeignKey('Category')
    instructor = models.ForeignKey('Employee')

    def __str__(self):
        return self.title


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    employee_name = models.CharField(max_length=127)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.employee_name


class Instructor(models.Model):
    employee = models.ForeignKey(Employee)

    class Meta:
        permissions = (
            ("instructor", "Instructor permissions"),
        )


class Administrators(models.Model):
    employee = models.ForeignKey(Employee)

    class Meta:
        permissions = (
            ("admin", "Administrator permissions"),
        )


class HR(models.Model):
    employee = models.ForeignKey(Employee)

    class Meta:
        permissions = (
            ("HR", "HR permissions"),
        )


class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    course = models.ForeignKey('Course')
    employee = models.ForeignKey('Employee')
    progress = models.IntegerField(default=1)
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.course.title


class Module(models.Model):
    module_id = models.AutoField(primary_key=True)
    title = models.TextField(max_length=127)
    course = models.ForeignKey('Course')
    order = models.IntegerField()

    def __str__(self):
        return self.course.title + ' - Module ' + str(self.module_id)


class Component(models.Model):
    component_id = models.AutoField(primary_key=True)
    module = models.ForeignKey('Module')
    order = models.IntegerField()
    title = models.CharField(max_length=127)
    type = models.CharField(max_length=127, choices=COMPONENT_TYPEs, default='text')
    text_content = models.TextField(default='', null=True, blank=True)
    image_content = models.ImageField(upload_to='uploads', null=True, blank=True)
    file_content = models.FileField(upload_to='uploads', null=True, blank=True)
    video_url = EmbedVideoField(null=True, blank=True)
    question = models.CharField(max_length=4096, null=True, blank=True)
    answer = models.CharField(max_length=4096, null=True, blank=True)

    def __str__(self):
        return self.module.__str__() + ' - ' + self.title


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=127)

    def __str__(self):
        return self.category_name
