from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from core import models as core_models

# Create your models here.


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.
    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, username, password, email=None):
        """Create and return a `User` with an email, username and password."""

        user = self.model(username=username)
        if email:
            user.email = self.normalize_email(email)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password, email=None):
        """
        Create and return a `User` with superuser powers.
        Superuser powers means that this use is an admin that can do anything
        they want.
        """

        user = self.create_user(username, password, email)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, core_models.TimeStampModel):
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(null=True, max_length=128, blank=True, unique=True)

    # When a user no longer wishes to use our platform, they may try to delete
    # there account. That's a problem for us because the data we collect is
    # valuable to us and we don't want to delete it. To solve this problem, we
    # will simply offer users a way to deactivate their account instead of
    # letting them delete it. That way they won't show up on the site anymore,
    # but we can still analyze the data.
    is_active = models.BooleanField(default=True)

    # The `is_staff` flag is expected by Django to determine who can and cannot
    # log into the Django admin site. For most users, this flag will always be
    # falsed.
    is_staff = models.BooleanField(default=False)

    # More fields required by Django when specifying a custom user model.

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case, we want that to be the email field.
    USERNAME_FIELD = "username"

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            Profile.objects.get(user=self)
        except Profile.DoesNotExist:
            Profile.objects.create(user=self)


class Profile(core_models.TimeStampModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.ForeignKey(
        core_models.Gender, limit_choices_to={"is_active": True}, on_delete=models.DO_NOTHING, default=None, blank=True, null=True
    )
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.ForeignKey(
        core_models.City, limit_choices_to={"is_active": True}, on_delete=models.DO_NOTHING, default=None, blank=True, null=True
    )
    relation_type = models.ManyToManyField(core_models.RelationType, limit_choices_to={"is_active": True}, blank=True)

    def __str__(self):
        return self.user.username

    def get_profile_completed(self):
        if self.gender and self.date_of_birth and self.location and self.relation_type:
            return True
        return False
