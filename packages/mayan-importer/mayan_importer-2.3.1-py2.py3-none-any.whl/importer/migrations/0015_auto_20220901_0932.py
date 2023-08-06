from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('importer', '0014_auto_20201227_0610')
    ]

    operations = [
        migrations.AlterModelOptions(
            name='importsetupitem',
            options={
                'ordering': ('import_setup', 'identifier'),
                'verbose_name': 'Import setup item',
                'verbose_name_plural': 'Import setup items'
            }
        ),
        migrations.AlterField(
            model_name='importsetupitem',
            name='state',
            field=models.IntegerField(
                choices=[
                    (1, 'None'), (2, 'Error'), (3, 'Queued'),
                    (4, 'Downloaded'), (5, 'Complete')
                ], db_index=True, default=1, verbose_name='State'
            )
        )
    ]
