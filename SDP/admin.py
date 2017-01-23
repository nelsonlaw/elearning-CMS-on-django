from django.contrib import admin

# Register your models here.

from .models import Course
from .models import Employee
from .models import Instructor
from .models import Administrators
from .models import HR
from .models import Enrollment
from .models import Module
from .models import Component
from .models import Category

admin.site.register(Course)
admin.site.register(Employee)
admin.site.register(Instructor)
admin.site.register(Administrators)
admin.site.register(HR)
admin.site.register(Enrollment)
admin.site.register(Module)
admin.site.register(Component)
admin.site.register(Category)
