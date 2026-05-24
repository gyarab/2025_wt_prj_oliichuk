from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="player",
            name="region",
            field=models.CharField(default="", max_length=16, blank=True),
        ),
        migrations.AddField(
            model_name="player",
            name="account_level",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="player",
            name="account_raw",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="player",
            name="mmr_raw",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
