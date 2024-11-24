from django.db import models
from django.contrib.auth.models import User
import uuid

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


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='carts')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.medicine.price * self.quantity  # Calculate price based on quantity

    def __str__(self):
        return f"{self.user.username} - {self.medicine.name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    medicines = models.ManyToManyField(Medicine, through='OrderItem', related_name='orders')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ordered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  

    def __str__(self):
        return f"{self.user.username} - {self.total}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.order.user.username} - {self.medicine.name}"



class Doctor(models.Model):
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    qualifications = models.TextField()
    image = models.ImageField(upload_to='doctors/')
    
    def __str__(self):
        return self.name

class Hospital(models.Model):
    doctor = models.ManyToManyField(Doctor, related_name='hospitals')
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    logo = models.ImageField(upload_to='hospitals/')

    def __str__(self):
        return self.name
    
class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='schedules')
    start_time = models.TimeField()
    end_time = models.TimeField()
    days_available = models.CharField(max_length=255) 
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    pay_first = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor.name} at {self.hospital.name}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    image = models.ImageField(upload_to='profiles/', default='profiles/default.png')

    def __str__(self):
        return self.user.username
        
class Appointment (models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='appointments')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='appointments')
    patient_contact = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    
    STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled')
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

   
    def __str__(self):
        return f"{self.patient.username} - {self.doctor.name} at {self.hospital.name}"

