# Generated by Django 4.2.20 on 2025-05-01 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_appointments', '0004_alter_appointments_date_alter_appointments_patientid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointments',
            name='status',
            field=models.CharField(choices=[('available', 'متاح'), ('booked', 'محجوز'), ('finished', 'منتهي'), ('canceled', 'ملغي'), ('no_show', 'لم يحضر'), ('rescheduled', 'مؤجل'), ('pending', 'قيد الانتظار'), ('confirmed', 'مؤكد'), ('in_progress', 'قيد التنفيذ'), ('completed', 'مكتمل')], default='available', max_length=15),
        ),
    ]
