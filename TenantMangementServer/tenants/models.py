from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.hashers import make_password


class User (models.Model):
    
    class PropertyType(models.TextChoices):
        RESIDENTIAL = "residential","Residential"
        COMMERCIAL = "commercial", "Commercial"
        AGRICULTURE = "agriculture", "Agriculture"
        INDUSTRIAL = "industrial", "Industrial"
    
    class UserType(models.TextChoices):
        BUSINESS = "business","Business"
        LESSER = "lesser","Lesser"
        LESSEE = "lessee","Lessee"

    class LeaseType(models.TextChoices):
        FIXED = "fixed", "Fixed"
        NOT_FIXED = "revenue","Revenue"

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = PhoneNumberField(unique=True)
    password = models.CharField(max_length=255)
    access_token = models.CharField(default="",max_length=255,blank=True)
    refresh_token = models.CharField(default="",max_length=255,blank=True)
    username = models.CharField(max_length=50)
    property_type = models.CharField(
        max_length=50,
        choices = PropertyType.choices,
        default = PropertyType.RESIDENTIAL
        )
    user_type = models.CharField(
        max_length=50,
        choices = UserType.choices,
        default = UserType.BUSINESS
    )
    lease_type = models.CharField(
        max_length = 50,
        choices = LeaseType.choices,
        default = LeaseType.FIXED
    )
    
    


    def save(self, *args, **kwargs):
        if self.password and not  self.password.startswith('pbkdf2_sha256$'):
            # checks if the password is not null and
            # password starts with this string
            self.password = make_password(self.password)
        
        super().save(*args, **kwargs)

    
    def __str__(self):
        return self.name