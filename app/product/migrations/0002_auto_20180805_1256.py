# Generated by Django 2.0.7 on 2018-08-05 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParentCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('PARENT_CATEGORY_side', '밑반찬'), ('PARENT_CATEGORY_soup', '국,찌개'), ('PARENT_CATEGORY_main', '메인반찬'), ('PARENT_CATEGORYSIDE_child', '아이반찬'), ('PARENT_CATEGORYSIDE_regular', '정기반찬'), ('PARENT_CATEGORYSIDE_simple', '간편식'), ('PARENT_CATEGORYSIDE_snack', '간식'), ('PARENT_CATEGORYSIDE_brand', '브랜드관')], max_length=250)),
            ],
        ),
        migrations.DeleteModel(
            name='Coupon',
        ),
        migrations.AddField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(default=1, max_length=250, on_delete=django.db.models.deletion.CASCADE, to='product.ParentCategory'),
            preserve_default=False,
        ),
    ]