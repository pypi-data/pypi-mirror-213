from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('importer', '0015_auto_20220901_0932')
    ]

    operations = [
        migrations.AddField(
            model_name='importsetup',
            name='item_time_buffer',
            field=models.PositiveIntegerField(
                default=100, help_text='Delay in milliseconds between '
                'item import tasks execution.',
                verbose_name='Item time buffer'
            )
        )
    ]
