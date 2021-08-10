from django.db import models
from datetime import date, datetime
import re

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password  should be at least 8 characters"
        if postData['password'] != postData['password_conf']:
            errors["password"] = "Passwords must match"
        email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.search(email_regex,postData['email'])):
            pass
        else:
            errors["email"] = "Please format your email correctly"
        bad_email = User.objects.filter(email = postData['email'])
        if len(bad_email) > 0:
                errors["email"] = "Please use a different email"
        t_date = date.today()
        r_date =postData['birth_date']
        try:
            fr_date = datetime.strptime(r_date,'%Y-%m-%d')
            if fr_date.year > t_date.year:
                errors["birth_date"] = "Birthday should be in the past"
            elif fr_date.year == t_date.year and fr_date.month > t_date.month:
                errors["birth_date"] = "Birthday should be in the past"
            elif fr_date.year == t_date.year and fr_date.month == t_date.month and fr_date.day > t_date.day:
                errors["birth_date"] = "Birthday should be in the past"
        except:
            errors["birth_date"] = "Birthday can't be blank"
        return errors

    def login_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['password']) < 8:
            errors["password"] = "Password  should be at least 8 characters"
        email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.search(email_regex,postData['email'])):
            pass
        else:
            errors["email"] = "Please format your email correctly"
        bad_email = User.objects.filter(email = postData['email'])
        if len(bad_email) > 0:
                errors["email"] = "Please use a different email"
        return errors
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    birth_date = models.DateField(blank=True, null=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f"User object: {self.first_name} {self.last_name} ({self.id})"
