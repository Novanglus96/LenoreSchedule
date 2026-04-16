from django.db import models
from django.contrib.auth.models import User
from staff.models import Division


class UserProfile(models.Model):
    """
    Model representing a user's profile and division access.

    Each app user has exactly one profile (auto-created on user creation via
    signal). Division membership controls which employees the user can see —
    a user with no divisions assigned has no access to employee data.

    Attributes:
        user (OneToOneField): The auth.User this profile belongs to.
        divisions (ManyToManyField): Divisions the user is allowed to see.
            Superusers and staff bypass this restriction entirely.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    divisions = models.ManyToManyField(
        Division, blank=True, related_name="user_profiles"
    )

    def __str__(self):
        return self.user.username
