from django.db import models

# Create your models here.


class Group(models.Model):
    """
    Model representing a group to be used for employees.

    Attributes:
        group_name (CharField): The name of the group.  Unique.
    """

    group_name = models.CharField(unique=True)

    def __str__(self):
        """
        __str__ Overrides the string representation for Group and returns the
        group name.

        Returns:
            (str): The string representation of the group name.
        """
        return f"{self.group_name}"
