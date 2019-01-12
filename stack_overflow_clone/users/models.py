# Third Party Stuff
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.postgres.fields import CIEmailField
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Stack Overflow Clone Stuff
from stack_overflow_clone.base.models import UUIDModel
from stack_overflow_clone.base.utils import upload_to


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: str, is_staff: bool, is_superuser: bool, **extra_fields):
        """Creates and saves a User with the given email and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractBaseUser, UUIDModel, PermissionsMixin):
    name = models.CharField(_('Name'), max_length=120, blank=True)
    # https://docs.djangoproject.com/en/1.11/ref/contrib/postgres/fields/#citext-fields
    email = CIEmailField(_('email address'), unique=True, db_index=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text='Designates whether the user can log into this admin site.')
    about_me = models.CharField(_('Name'), max_length=120, blank=True)
    is_active = models.BooleanField('active', default=True,
                                    help_text='Designates whether this user should be treated as '
                                              'active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_login = models.DateTimeField(_('last login'), auto_now=True, null=True, blank=True)
    reputation = models.PositiveIntegerField(_('Reputation'), default=0)
    profile_photo = models.ImageField(upload_to=upload_to, blank=True, verbose_name='Profile Photo')

    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-date_joined', )

    def __str__(self):
        return str(self.id)
