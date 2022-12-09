from django import forms
from django.forms import ModelForm
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import connection
from .models import Courses

class RegisterForm(UserCreationForm):
      
    class Meta:
        model = User
        fields = ["username","first_name","last_name","password1","password2"]

    def clean_first_name(self):
        f = self.cleaned_data["first_name"].strip()
        if f == '':
            raise forms.ValidationError("First name is required.")
        
        cursor = connection.cursor()
        cursor.execute("select student_name from students")
        # cursor.close()
        query = cursor.fetchall()
        cursor = connection.cursor()
        cursor.execute("select instructor_name from instructor")
        # cursor.close()
        query2 = cursor.fetchall()
        #student name check
        newq = []
        newq2 = []
        newq3 = ["Humanities","Science","Business"]
        for x in query:
            newq.append(x[0].split(" ")[0]);
        for x in query2:
            newq2.append(x[0].split(" ")[1]);
        
        counter = 0 
        for i in newq:
            if (f==str(i)):
                counter += 1
        for i in newq2:
            if (f==str(i)):
                counter += 1
        for i in newq3:
            if (f==i):
                counter += 1
        if (counter==0):
            raise forms.ValidationError("First name does not exist")
    
            
        return self.cleaned_data["first_name"]

    def clean_last_name(self):
        l = self.cleaned_data["last_name"].strip()
        if l == '':
            raise forms.ValidationError("Last name is required.")
        
        cursor = connection.cursor()
        cursor.execute("select student_name from students")
        # cursor.close()
        query = cursor.fetchall()
        cursor = connection.cursor()
        cursor.execute("select instructor_name from instructor")
        # cursor.close()
        query2 = cursor.fetchall()
        #student name check
        newq = []
        newq2 = []
        for x in query:
            newq.append(x[0].split(" ")[1]);
        for x in query2:
            newq2.append(x[0].split(" ")[2]);
        counter = 0 
        for i in newq:
            if (l==str(i)):
                counter += 1
        for i in newq2:
            if (l==str(i) or l=="Department"):
                counter += 1
        if (counter==0):
            raise forms.ValidationError("Last name does not exist")

        return self.cleaned_data["last_name"]

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name','username']

class AddCourseForm(forms.ModelForm):

    class Meta:
        fields = ['course']
