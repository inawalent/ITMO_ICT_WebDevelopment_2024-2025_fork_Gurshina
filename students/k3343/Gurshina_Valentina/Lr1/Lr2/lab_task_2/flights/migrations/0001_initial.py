# Generated by Django 5.1.4 on 2025-01-13 22:04

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Airline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'авиакомпания',
                'verbose_name_plural': 'авиакомпании',
                'db_table': 'airline',
            },
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('departure', 'Отлёт'), ('arrival', 'Прилёт')], max_length=9, verbose_name='Тип')),
                ('gate', models.CharField(max_length=5, verbose_name='Выход')),
                ('date', models.DateTimeField(verbose_name='Время вылета')),
                ('airline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flights', to='flights.airline', verbose_name='Авиакомпания')),
            ],
            options={
                'verbose_name': 'рейс',
                'verbose_name_plural': 'рейсы',
                'db_table': 'flight',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст')),
                ('rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='Рейтинг')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to=settings.AUTH_USER_MODEL, verbose_name='Пассажир')),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='flights.flight', verbose_name='Рейс')),
            ],
            options={
                'verbose_name': 'отзыв',
                'verbose_name_plural': 'отзывы',
                'db_table': 'feedback',
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registered', models.BooleanField(default=False, verbose_name='Зарегистрирован ли пассажир?')),
                ('ticket', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Номер брони')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL, verbose_name='Пассажир')),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='flights.flight', verbose_name='Рейс')),
            ],
            options={
                'verbose_name': 'бронь',
                'verbose_name_plural': 'брони',
                'db_table': 'booking',
            },
        ),
    ]
