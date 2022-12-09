from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(models.Model):
    username = models.CharField(max_length=64)
    course_ID = models.IntegerField()
    start_time = models.IntegerField()

class Dep(models.Model):
    username = models.CharField(max_length=64)
    section_id = models.IntegerField(db_column='section_ID')  # Field name made lowercase.
    instructor_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'Dep'

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)


    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Classroom(models.Model):
    classroom_id = models.AutoField(db_column='classroom_ID', primary_key=True)  # Field name made lowercase.
    building_name = models.CharField(max_length=225, blank=True, null=True)
    class_capacity = models.IntegerField(blank=True, null=True)
    room_number = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'classroom'


class Courses(models.Model):
    course_id = models.AutoField(db_column='course_ID', primary_key=True)  # Field name made lowercase.
    instructor_id = models.IntegerField(db_column='instructor_ID')  # Field name made lowercase.
    department_id = models.IntegerField(db_column='department_ID')  # Field name made lowercase.
    course_name = models.CharField(max_length=225, blank=True, null=True)
    department_name = models.CharField(max_length=225, blank=True, null=True)
    credit_hours = models.IntegerField(blank=True, null=True)
    semester = models.CharField(max_length=225, blank=True, null=True)
    batch_year = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'courses'


class Department(models.Model):
    department_id = models.AutoField(db_column='department_ID', primary_key=True)  # Field name made lowercase.
    department_name = models.CharField(max_length=225, blank=True, null=True)
    building_name = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'department'


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Instructor(models.Model):
    instructor_id = models.AutoField(db_column='instructor_ID', primary_key=True)  # Field name made lowercase.
    department_id = models.IntegerField(db_column='department_ID')  # Field name made lowercase.
    instructor_name = models.CharField(max_length=225, blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    instructor_office_addr = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instructor'


class MainProfile(models.Model):
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'main_profile'


class Prereqs(models.Model):
    course_id = models.AutoField(db_column='course_ID', primary_key=True)  # Field name made lowercase.
    prereqs_id = models.IntegerField(db_column='prereqs_ID')  # Field name made lowercase.
    prereqs_names = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prereqs'


class Section(models.Model):
    section_id = models.AutoField(db_column='section_ID', primary_key=True)  # Field name made lowercase.
    instructor_id = models.IntegerField(db_column='instructor_ID')  # Field name made lowercase.
    course_id = models.IntegerField(db_column='course_ID')  # Field name made lowercase.
    batch_year = models.TextField(blank=True, null=True)  # This field type is a guess.
    semester = models.CharField(max_length=225, blank=True, null=True)
    number_students = models.IntegerField(blank=True, null=True)
    section_capacity = models.IntegerField(blank=True, null=True)
    room_number = models.IntegerField(blank=True, null=True)
    section_name = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'section'


class Students(models.Model):
    student_id = models.AutoField(db_column='student_ID', primary_key=True)  # Field name made lowercase.
    department_id = models.IntegerField(db_column='department_ID')  # Field name made lowercase.
    student_name = models.CharField(max_length=225, blank=True, null=True)
    batch_year = models.TextField(blank=True, null=True)  # This field type is a guess.
    major = models.CharField(max_length=225, blank=True, null=True)
    total_credithours = models.IntegerField(blank=True, null=True)
    student_semester = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'students'


class Timeslot(models.Model):
    timeslot_id = models.AutoField(db_column='timeslot_ID', primary_key=True)  # Field name made lowercase.
    course_id = models.IntegerField(db_column='course_ID')  # Field name made lowercase.
    classroom_id = models.IntegerField(db_column='classroom_ID')  # Field name made lowercase.
    section_id = models.IntegerField(db_column='section_ID')  # Field name made lowercase.
    start_time = models.IntegerField(blank=True, null=True)
    end_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'timeslot'
