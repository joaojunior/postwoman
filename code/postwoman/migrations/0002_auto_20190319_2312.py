# Generated by Django 2.1.7 on 2019-03-19 23:12

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('postwoman', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(default=0)),
                ('longitude', models.FloatField(default=0)),
                ('date', models.DateField(default=datetime.date.today)),
                ('delivered', models.BooleanField(default=False)),
                ('postwoman', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postwoman.PostWoman')),
            ],
        ),
        migrations.AddIndex(
            model_name='letter',
            index=models.Index(fields=['date', 'postwoman'], name='postwoman_l_date_6e2d74_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='letter',
            unique_together={('latitude', 'longitude', 'date')},
        ),
    ]