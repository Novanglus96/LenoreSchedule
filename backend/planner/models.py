from django.db import models

# Create your models here.


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
