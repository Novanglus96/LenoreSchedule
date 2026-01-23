from django.db import models

# Create your models here.


class Group(models.Model):
    """
    Model representing a group to be used for employees.

    Fields:
    - group_name (CharField): The name of the group.  Unique.
    """

    group_name = models.CharField(unique=True)

    def __str__(self):
        return f"{self.group_name}"
