# account/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.db.models import Count


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have a valid email address!")
        if not username:
            raise ValueError("Users must have a username!")
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
            )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def get_profile_picture_filepath(self, filename):
    return'profile_images/' + str(self.pk) + '/profile_image.png'



#default image func could also be asserted here: point one image's path

class Account(AbstractBaseUser):
    
# unique = True, nobody can share the same email and username, also we need to now when they're joined
    email=models.EmailField(verbose_name="email", max_length=60, unique=True)
    username=models.CharField(max_length=30, unique=True)
    # when the person sign-up this auto now will be set
    date_joined=models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    # everytime the person enters this part will be overwrite 
    last_login=models.DateTimeField(verbose_name="last login", auto_now=True)
    # below four is included in the abstract base user class, needed to overwrite
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    # need third-party
    # ImageField: package supports image
    # profile pic is a must, if no add default argument
    # upload to = where the image is going to be stored set a pathway
    profile_image=models.ImageField(max_length=255, upload_to=get_profile_picture_filepath, null=False, blank=False)
    hide_email=models.BooleanField(default=True)
    interests= models.ManyToManyField('matcher.Interest', blank=True)

    objects = MyAccountManager()

    #could also be email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # publicity
    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    


