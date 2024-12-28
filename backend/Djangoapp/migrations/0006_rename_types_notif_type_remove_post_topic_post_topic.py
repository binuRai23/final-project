# Generated by Django 4.2 on 2024-12-28 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Djangoapp', '0005_topic_post_notif_comment_bookmarks'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notif',
            old_name='types',
            new_name='type',
        ),
        migrations.RemoveField(
            model_name='post',
            name='Topic',
        ),
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='Djangoapp.topic'),
        ),
    ]
