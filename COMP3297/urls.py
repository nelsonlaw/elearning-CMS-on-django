"""COMP3297 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import SDP.views
from django.contrib.auth import views as auth_views
from SDP.login_form import LoginForm

urlpatterns = [
                  url(r'^$', SDP.views.home),
                  url(r'^admin/', admin.site.urls),
                  url(r'^home/$', SDP.views.home),
                  url(r'^home_instructor/$', SDP.views.home_instructor),
                  url(r'^home_hr/$', SDP.views.home_hr),
                  url(r'^home_admin/$', SDP.views.home_admin),
                  url(r'^course/(?P<course_id>\d+)', SDP.views.course),
                  url(r'^modify_course/(?P<course_id>\d+)', SDP.views.modify_course),
                  url(r'^modify_course_order/(?P<course_id>\d+)', SDP.views.modify_course_order),
                  url(r'^enrol/(?P<course_id>\d+)', SDP.views.enrol),
                  url(r'^drop/(?P<course_id>\d+)', SDP.views.drop),
                  url(r'^category/(?P<cid>\d+)', SDP.views.category),
                  url(r'^create/', SDP.views.create),
                  url(r'^create_module/(?P<course_id>\d+)', SDP.views.create_module),
                  url(r'^create_component/(?P<module_id>\d+)/(?P<type>\w+)', SDP.views.create_component),
                  url(r'^logout/$', auth_views.logout, {'next_page': '/login'}),
                  url(r'^login/$', auth_views.login, {'template_name': 'login.html', 'authentication_form': LoginForm},
                      name='login'),
                  url(r'^register/$', SDP.views.register),
                  url(r'^record/$', SDP.views.record),
                  url(r'^role/$', SDP.views.role),
                  url(r'^designate/$', SDP.views.designate),
                  url(r'^control_access/$', SDP.views.control_access),
                  url(r'^open_course/(?P<course_id>\d+)', SDP.views.open_course),
                  url(r'^next_module/(?P<course_id>\d+)', SDP.views.next_module),
                  url(r'^manage_category/$', SDP.views.manage_category),
                  url(r'^no_permission', SDP.views.no_permission)

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
