#Feature list
-------------
- Course management
- User permission management
- Multi-media support, such as video, image, youtube video ...


# Tested environment:
OS              : Windows 7, Ubuntu 16.06
python verion   : python 3
python modules  : django 1.10.3 pillow 3.4.2 django-embed-video 1.1.0

# Installation
1) Initialize a virtualenv environment.(optional)
2) pip install django
3) pip install pillow
4) pip install django-embed-video
5) run python manage.py runserver 8000


# Default accounts for demo propose:
student1 : participant
instruct : instructor
admin123 : administrator
human123 : HR
All with password comp3297


# Limitation:
1) For instructor, changing modules/components ordering is not fool proof. SDP will display modules/components numerically.
2) For instructor, invalid youtube link will not rejected by SDP. Please make sure the youtube link provided is valid.



