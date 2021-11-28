from django.db import models
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser):
    objects = UserManager()

    email = models.EmailField(_('email address'), unique=True)
    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)

    is_active = models.BooleanField('active', default=True)
    is_admin = models.BooleanField('admin', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    username = models.CharField(
        _('username'),
        max_length=150,
        default=uuid.uuid4,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    class Meta:
        ordering = ['email']


    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.email

    def __unicode__(self):
        return self.email


class Profile(models.Model):
    GENDER = (
        ('M', 'Homme'),
        ('F', 'Femme'),
    )

    #user = models.OneToOneField(settings.AUTH_USER_MODEL)
    first_name = models.CharField(max_length=120, blank=False)
    last_name = models.CharField(max_length=120, blank=False)
    gender = models.CharField(max_length=1, choices=GENDER)

    def __unicode__(self):
        return u'Profile of user: {0}'.format(self.user.email)

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=120, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

