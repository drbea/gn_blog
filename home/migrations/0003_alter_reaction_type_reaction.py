# Generated by Django 5.1.3 on 2024-12-06 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_rename_utilisateur_reaction_autheur_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reaction',
            name='type_reaction',
            field=models.CharField(choices=[('like', 'like'), ('jadore', 'jadore'), ('cool', 'cool'), ('dislike', 'dislike')], max_length=50),
        ),
    ]
