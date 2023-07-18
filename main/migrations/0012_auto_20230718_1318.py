# Generated by Django 3.2.3 on 2023-07-18 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20230718_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='HelpResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.TextField(max_length=1000)),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='main.helpsubject')),
            ],
        ),
        migrations.AddField(
            model_name='helpmessage',
            name='read_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='HelpMessageResponse',
        ),
    ]
