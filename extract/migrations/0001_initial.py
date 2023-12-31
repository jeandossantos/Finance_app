# Generated by Django 4.2.3 on 2023-07-05 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_profile', '0003_account_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashFlow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('type_cash_flow', models.CharField(choices=[('in', 'Entrada'), ('out', 'Saída')], max_length=3)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user_profile.account')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user_profile.category')),
            ],
        ),
    ]
