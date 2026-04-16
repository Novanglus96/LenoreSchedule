from django.db import models
from staff.models import Employee, Location

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


class CalendarEntry(models.Model):
    """
    Model representing a calendar entry (override or manual shift).

    CalendarEntries layer on top of ScheduleTemplates. A full-day absence
    (vacation, sick, etc.) leaves start_time, end_time, and location null.
    A partial override covers a specific time block within a day.

    Attributes:
        employee (ForeignKey): The employee this entry belongs to.
        calendar_date (DateField): The date of the entry.
        start_time (TimeField): Start of the time block. Null for full-day entries.
        end_time (TimeField): End of the time block. Null for full-day entries.
        confirmed (BooleanField): Whether this entry has been confirmed.
        location (ForeignKey): Where the employee is working. Optional.
        entry_type (CharField): The type of entry (scheduled, vacation, sick, etc.).
        notes (TextField): Optional free-text notes for the entry.
    """

    ENTRY_TYPE_CHOICES = [
        ("scheduled", "Scheduled"),
        ("vacation", "Vacation"),
        ("sick", "Sick"),
        ("holiday", "Holiday"),
        ("floating_holiday", "Floating Holiday"),
        ("personal", "Personal"),
        ("overtime", "Overtime"),
        ("swap", "Shift Swap"),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    calendar_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True, default=None)
    end_time = models.TimeField(null=True, blank=True, default=None)
    confirmed = models.BooleanField(default=False)
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True
    )
    entry_type = models.CharField(
        max_length=50,
        choices=ENTRY_TYPE_CHOICES,
        default="scheduled",
    )
    notes = models.TextField(null=True, blank=True, default=None)

    class Meta:
        verbose_name = "Calendar Entry"
        verbose_name_plural = "Calendar Entries"

    def __str__(self):
        return f"{self.calendar_date} {self.start_time} - {self.end_time}: {self.employee.last_name}, {self.employee.first_name}"


class ScheduleTemplate(models.Model):
    """
    Model representing one time block in an employee's typical weekly schedule.

    Multiple blocks per day are supported (e.g. 10am-2pm and 4pm-6pm on Monday).
    Days with no ScheduleTemplate rows are treated as days off.

    Attributes:
        employee (ForeignKey): The employee this template belongs to.
        day_of_week (PositiveSmallIntegerField): Day of the week (0=Monday … 6=Sunday).
        start_time (TimeField): Start of the block.
        end_time (TimeField): End of the block.
        location (ForeignKey): Where the employee works during this block. Optional.
    """

    DAY_OF_WEEK_CHOICES = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="schedule_templates",
    )
    day_of_week = models.PositiveSmallIntegerField(choices=DAY_OF_WEEK_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Schedule Template"
        verbose_name_plural = "Schedule Templates"

    def __str__(self):
        days = [
            "Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday",
        ]
        return (
            f"{self.employee} - {days[self.day_of_week]} "
            f"{self.start_time}-{self.end_time}"
        )
