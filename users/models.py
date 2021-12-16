from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from PIL import Image
from django.utils.text import slugify
from django.core.validators import validate_slug
from django.core.exceptions import ValidationError


class Company(models.Model):
    name = models.CharField('Company name', max_length=20, help_text='20 characters or less.',
                            unique=True)
    description = models.TextField('Company Description', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def validate_username(value):
    """
    Custom validator to counteract potential slugify duplicates in cases
    of leading and trailing hyphens and underscores in username
    """
    if value.endswith('_') or value.endswith('-') or \
            value.startswith('_') or value.startswith('-'):
        raise ValidationError("Username cannot start or end with hyphen or underscore")
    else:
        return value

def image_size(value):
    limit = 1000000 # 1MB
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 1MB.')


class User(AbstractBaseUser):
    class AccountType(models.TextChoices):
        admin = 'Admin'
        agent = 'Agent'

    image = models.ImageField(default='default.jpg', upload_to='profile_pics',
                              help_text='File size requirements: 1MB or less', validators=[image_size])
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(verbose_name='Username', max_length=30, unique=True,
                                help_text='Username must consist of letters, numbers, underscores or hyphens',
                                validators=[validate_slug, validate_username],
                                error_messages={'invalid': "Enter a valid username"})
    slug = models.SlugField(blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users', blank=True, null=True)
    account_type = models.CharField(max_length=20,
                                    choices=AccountType.choices,
                                    default=AccountType.agent)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True, default='')
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return f'{self.username}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

        # img = Image.open(self.image)
        #
        # if img.height > 300 or img.width > 300:
        #     output_size = (300, 300)
        #     img.thumbnail(output_size)
        #     img.save(self.image)

    class Meta:
        ordering = ('username',)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Profile'
