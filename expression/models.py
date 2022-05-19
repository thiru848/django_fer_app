import django
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from .storage import OverWriteStorage
from .validators import validate_file_extension

# Create your models here.

class CustomAccountManager(BaseUserManager):
    def create_user(self, email, user_name, password, **other_fields):
        email = self.normalize_email(email) # lowercase domain part
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, email, user_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(email, user_name, password, **other_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):

    user_name = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    is_staff = models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='Staff Status')
    is_active = models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='Active')
    is_doctor = models.BooleanField(default=False, help_text='Qualifies the user as either Doctor (True) or Patient (False)', verbose_name='Is_Doctor Status')
    phone = models.CharField(max_length=10)
    otp = models.IntegerField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6)
    profile = models.ImageField(upload_to="user/profile/", storage=OverWriteStorage())
    group = models.CharField(max_length=5)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    pincode = models.CharField(max_length=6)
    last_login = models.DateTimeField(null=True, blank=True, help_text='Last login time of this account', verbose_name='Last Login')
    date_joined = models.DateTimeField(default=django.utils.timezone.now, help_text='Time at Creation of this account', verbose_name='Date Joined') 

    objects = CustomAccountManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.user_name

    def delete(self, *args, **kwargs):
        s1, p1 = self.profile.storage, self.profile.path
        super(CustomUser, self).delete(*args, **kwargs)
        s1.delete(p1)
    
    def save(self, *args, **kwargs):
        try:
            this = CustomUser.objects.get(id=self.id)
            if this.profile != self.profile and self.profile is not None:
                this.profile.delete(save=False)
        except: pass
        super(CustomUser, self).save(*args, **kwargs)


class Song(models.Model):
    title= models.TextField()
    artist= models.TextField()
    image= models.ImageField(upload_to="img/", storage=OverWriteStorage())
    audio_file = models.FileField(blank=True,null=True, upload_to="records/", validators=[validate_file_extension])
    audio_link = models.CharField(max_length=200,blank=True,null=True)
    duration=models.CharField(max_length=20)
    paginate_by = 2

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            this = Song.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
            if this.audio_file != self.audio_file:
                this.audio_file.delete(save=False)
        except: pass
        super(Song, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        s1, p1, s2, p2 = self.audio_file.storage, self.audio_file.path, self.image.storage, self.image.path
        super(Song, self).delete(*args, **kwargs)
        s1.delete(p1)
        s2.delete(p2)
