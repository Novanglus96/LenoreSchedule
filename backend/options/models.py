from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.


class SingletonModel(models.Model):
    """
    Class for repersenting a Singleton model.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Overides the save to make sure there is only one instance of this model.

        Raises:
            ValidationError: A string stating there is already an instance of this
            model.

        Returns:
            (SingletonModel): The singleton model.
        """
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError("There is already one instance of this model")
        return super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Overrides delete so that you can not delete the singleton model.

        Raises:
             ValidationError: A string stating you can't delete this object.
        """
        raise ValidationError("You cannot delete this object")


class Version(SingletonModel):
    """
    Model representing app version.

    Attributes:
        version_number (CharField): The current version of the app.
    """

    version_number = models.CharField(max_length=25)

    def __str__(self):
        """
        __str__ Overrides the string representation for Version and returns the
        version number.

        Returns:
            (str): The string representation of the version number.
        """
        return self.version_number


class PayrollInfo(models.Model):
    """
    Model representing a years payroll info.

    Attributes:
        payroll_year (IntegerField): The payroll year. Unique.
        payroll_start (DateField): The 1st day of the years payroll
        payroll_frequency (CharField): Choice of frequency. 50 char max.
        first_day (PositiveSmallIntegerField): 1st day of the month for frequency. Optional.
        second_day (PositiveSmallIntegerField): 2nd day of the month for frequency. Optional.
    """

    payroll_year = models.IntegerField(unique=True)
    payroll_start = models.DateField()
    payroll_frequency = models.CharField(
        max_length=50,
        choices=[
            ("weekly", "Weekly"),
            ("biweekly", "Biweekly"),
            ("semi-monthly", "Semi-Monthly"),
            ("monthly", "Monthly"),
            ("quadriweekly", "Quadriweekly"),
            ("daily", "Daily"),
        ],
    )
    first_day = models.PositiveSmallIntegerField(
        null=True, blank=True, default=None
    )
    second_day = models.PositiveSmallIntegerField(
        null=True, blank=True, default=None
    )

    class Meta:
        verbose_name = "Payroll Info"
        verbose_name_plural = "Payroll Info"

    def __str__(self):
        """
        __str__ Overrides the string representation for PayrollInfo and returns the
        payroll year.

        Returns:
            (str): The year of the payroll.
        """
        return str(self.payroll_year)
