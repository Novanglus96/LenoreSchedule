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


class Division(models.Model):
    """
    Model representing a division to be used for employees.

    Attributes:
        division_name (CharField): The name of the division.  Unique.
    """

    division_name = models.CharField(unique=True)

    def __str__(self):
        """
        __str__ Overrides the string representation for Division and returns the
        division name.

        Returns:
            (str): The string representation of the division name.
        """
        return f"{self.division_name}"


class Location(models.Model):
    """
    Model representing a division to be used for employees.

    Attributes:
        division_name (CharField): The name of the division.  Unique.
    """

    location_name = models.CharField(unique=True)

    def __str__(self):
        """
        __str__ Overrides the string representation for Location and returns the
        location name.

        Returns:
            (str): The string representation of the location name.
        """
        return f"{self.location_name}"


class Employee(models.Model):
    """
    Model representing an employee.

    Attributes:
        first_name (CharField): The first name of the employee. Required. 256 chars.
        last_name (CharField): The last name of the employee. Required. 256 chars.
        email (CharField): The email of the employee. 512 chars. Unique. Required.
        division (ForeignKey): The division of the employee.  Required.
        group (ForeignKey): The group for the employee. Required.
        location (ForeignKey): The locations for the employee. Required.
        start_date (date): The start date for the employee. Optional. Default None.
        end_date (date): The end date for the employee. Optional. Default None.
    """

    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.CharField(max_length=512, unique=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    start_date = models.DateField(default=None, null=True, blank=True)
    end_date = models.DateField(default=None, null=True, blank=True)

    def __str__(self):
        """
        __str__ Overrides the string representation for employee and returns last_name,
        first_name.

        Returns:
            (str): The string representation of the employee.
        """
        return f"{self.last_name}, {self.first_name}"


class Holiday(models.Model):
    """
    Model representing a holiday.

    Attributes:
        holiday_name (CharField): The name of the holiday
        rule_type (CharField): Type of repeating rule for the holiday.
        month (PositiveSmallIntegerField): The month of the year for the holiday.
          Optional. Default None.
        day (PositiveSmallIntegerField): The day of the month for the holiday.
          Optional. Default None.
        weekday (PositiveSmallIntegerField): The day of the week for the holiday.
          Optional. Default None.
        week (PositiveSmallIntegerField): The week of the month for the holiday.
          Optional. Default None.
        observed_rule (CharField): Observed rule for the holiday. Required. Default None.
    """

    holiday_name = models.CharField(max_length=100, unique=True)
    rule_type = models.CharField(
        max_length=50,
        choices=[
            ("fixed_date", "Fixed date"),
            ("nth_weekday", "Nth weekday of month"),
            ("last_weekday", "Last weekday of month"),
            ("custom", "Custom rule"),
        ],
    )
    month = models.PositiveSmallIntegerField(
        null=True, blank=True, default=None
    )
    day = models.PositiveSmallIntegerField(null=True, blank=True, default=None)
    weekday = models.PositiveSmallIntegerField(
        null=True, blank=True, default=None
    )  # 0=Mon
    week = models.PositiveSmallIntegerField(
        null=True, blank=True, default=None
    )  # 1–5
    observed_rule = models.CharField(
        max_length=50,
        choices=[
            ("none", "No observation"),
            ("next_business_day", "Next business day"),
            ("nearest_weekday", "Nearest weekday"),
        ],
        default="none",
    )

    def __str__(self):
        return self.holiday_name
