# Generated by Django 3.2 on 2023-07-25 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20230725_1017'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cotizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.cliente')),
                ('proforma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.proforma')),
            ],
        ),
    ]
