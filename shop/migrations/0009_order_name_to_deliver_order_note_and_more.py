# Generated by Django 4.2.7 on 2023-12-08 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_product_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='name_to_deliver',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='note',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='phone_to_deliver',
            field=models.CharField(default='', max_length=11),
            preserve_default=False,
        ),
    ]