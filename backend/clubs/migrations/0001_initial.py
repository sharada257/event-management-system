# Generated by Django 5.1.7 on 2025-03-15 13:52

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('departments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('club_name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clubs', to='departments.department')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supervised_clubs', to='accounts.teacher')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ClubMembership',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('role', models.CharField(choices=[('PRESIDENT', 'President'), ('VICE_PRESIDENT', 'Vice President'), ('BOARD_MEMBER', 'Board Member'), ('TREASURER', 'Treasurer'), ('CLUB_MEMBER', 'Club Member'), ('VOLUNTEER', 'Volunteer')], default='CLUB_MEMBER', max_length=20)),
                ('can_post_event', models.BooleanField(default=False)),
                ('joined_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='clubs.club')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='club_memberships', to='accounts.student')),
            ],
            options={
                'indexes': [models.Index(fields=['student', 'club'], name='clubs_clubm_student_08ab32_idx'), models.Index(fields=['role'], name='clubs_clubm_role_9c2345_idx')],
                'unique_together': {('student', 'club')},
            },
        ),
    ]
