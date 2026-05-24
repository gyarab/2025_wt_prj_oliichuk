from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_remove_player_account_level_and_more"),
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
