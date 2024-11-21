from django.db import models

# Create your models here.

class Medicine(models.Model):
    CATEGORY_CHOICES = [
        ('Diabetic Care', 'Diabetic Care'),
        ('OTC Medicine', 'OTC Medicine'),
        ('Pain Relief', 'Pain Relief'),
        ('Vitamins & Supplements', 'Vitamins & Supplements'),
        ('Womens Care', 'Womens Care'),
        ('Cold & Flu', 'Cold & Flu'),
        ('Skin Care', 'Skin Care'),
        ('Others', 'Others'),
    ]

    TYPE_CHOICES = [
        ('Tablet', 'Tablet'),
        ('Syrup', 'Syrup'),
        ('Capsule', 'Capsule'),
        ('Injection', 'Injection'),
        ('Cream', 'Cream'),
        ('Gel', 'Gel'),
        ('Others', 'Others'),
    ]

    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    image = models.ImageField(upload_to='medicines/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    dosage_mg = models.PositiveIntegerField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name