from django.db import models
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File

class Book(models.Model):
    name = models.CharField(max_length=150)
    cost = models.DecimalField(max_digits=3, decimal_places=000)
    year = models.PositiveIntegerField(default=2015)
    author = models.CharField(max_length=100)
    country_id = models.CharField(max_length=1)
    manufacturer_id = models.CharField(max_length=6)
    product_id = models.CharField(max_length=5)
    qrcode = models.ImageField(upload_to='qr/', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        EAN = barcode.get_barcode_class('ean13')
        ean = EAN(f"{self.country_id}{self.manufacturer_id}{self.product_id}", writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        self.qrcode.save(f"{self.name}_qrcode.png",File(buffer), save=False)
        return super().save(*args, **kwargs)
