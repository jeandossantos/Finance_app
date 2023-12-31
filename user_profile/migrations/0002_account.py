# Generated by Django 4.2.3 on 2023-07-03 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=50)),
                ('bank', models.CharField(choices=[('NU', 'Nubank'), ('CE', 'Caixa Econômica'), ('BR', 'Banco do Brasil'), ('IT', 'Itaú'), ('SF', 'Banco Safra'), ('SG', 'Santander Group')], max_length=2)),
                ('type_of_person', models.CharField(choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], max_length=2)),
                ('value', models.FloatField()),
                ('icon', models.ImageField(upload_to='icons')),
            ],
        ),
    ]
