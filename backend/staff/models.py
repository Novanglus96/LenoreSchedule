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


class Department(models.Model):
    """
    Model representing a department to be used for employees.

    Attributes:
        department_name (CharField): The name of the department.  Unique.
    """

    department_name = models.CharField(unique=True)

    def __str__(self):
        """
        __str__ Overrides the string representation for Department and returns the
        department name.

        Returns:
            (str): The string representation of the department name.
        """
        return f"{self.department_name}"


class Employee(models.Model):
    """
    Model representing an employee.

    Attributes:
        first_name (CharField): The first name of the employee. Required. 256 chars.
        last_name (CharField): The last name of the employee. Required. 256 chars.
        email (CharField): The email of the employee. 512 chars. Unique. Required.
        department (ForeignKey): The department of the employee.  Required.
        group (ForeignKey): The group for the employee. Required.
    """

    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.CharField(max_length=512, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        """
        __str__ Overrides the string representation for employee and returns last_name,
        first_name.

        Returns:
            (str): The string representation of the employee.
        """
        return f"{self.last_name}, {self.first_name}"
