from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("options", "0002_alter_payrollinfo_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="payrollinfo",
            name="week_start_day",
            field=models.CharField(
                choices=[("sun", "Sunday"), ("mon", "Monday")],
                default="sun",
                max_length=3,
            ),
        ),
    ]
