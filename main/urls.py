from django.urls import path, re_path
from . import views

urlpatterns = [
path("home/", views.home, name="home"),
path("", views.home, name="home"),
path("register/", views.register, name="register"),
path("login/", views.login_request, name="login"),
path("change_password", views.change_password, name='change_password'),
path("courses", views.courses, name='courses'),
path('profile/<username>', views.profile, name='profile'),
path('addrecord/<int:id>/<int:time>', views.addrecord, name='addrecord'),
path('offerform/offer/<int:id>', views.offer, name='offer'),
path('offerform/<int:id>', views.offerform, name='offerform'),
path('accept/<int:sid>/<int:cid>/<int:iid>', views.accept, name='accept'),
path('update/', views.update, name='update'),
path('updateform/<int:id>', views.updateform, name='update'),
path('editstudent/', views.editstudent, name='editstudent'),
path('edit/<int:id>', views.edit, name='edit'),
path('edit/editrecord/<int:id>', views.editrecord, name='editrecord'),
path('editstudent/editstudentform/<int:id>', views.editstudentform, name='editstudentform'),
path('editstudent/editstudentform/editstu/<int:id>', views.editstu, name='editstu'),
path('update/updateform/<int:eid>/updaterecord/<int:id>', views.updaterecord, name='update'),
path('update/updateform/<int:cid>/<int:id>', views.updateform, name='updateform'),
path('delete/<int:id>', views.delete, name='delete'),
]