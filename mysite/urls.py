"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from main import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path("register/", v.register, name="register"), 
    path("home/", v.home, name="home"),
    path("login/", v.login_request, name="login"),
    path("", v.home, name="home"),
    path("change_password", v.change_password, name='change_password'),
    path("courses", v.courses, name='courses'),
    path('profile/<username>', v.profile, name='profile'),
    path('addrecord/<int:id>/<int:time>', v.addrecord, name='addrecord'),
    path('offerform/offer/<int:id>', v.offer, name='offer'),
    path('offerform/<int:id>', v.offerform, name='offerform'),
    path('accept/<int:sid>/<int:cid>/<int:iid>', v.accept, name='accept'),
    path('edit/<int:id>', v.edit, name='edit'),
    path('edit/editrecord/<int:id>', v.editrecord, name='editrecord'),
    path('delete/<int:id>', v.delete, name='delete'),
    path('update/<int:id>', v.update, name='update'),
    path('editstudent/', v.editstudent, name='editstudent'),
    path('editstudent/editstudentform/<int:id>', v.editstudentform, name='editstudentform'),
    path('editstudent/editstudentform/editstu/<int:id>', v.editstu, name='editstu'),
    path('update/updateform/<int:eid>/updaterecord/<int:id>', v.updaterecord, name='update'),
    path('update/updateform/<int:cid>/<int:id>', v.updateform, name='updateform'),
    path('', include("main.urls")),
    path('', include("django.contrib.auth.urls")),
    #---------------------------------------------------------------
]