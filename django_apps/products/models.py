from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class products(models.Model):
  PRODUCT_TYPE_CHOICE = [
    ('IN', 'INTERIOR'),
    ('EX', 'EXTERIOR'),
    ('MCH', 'MECHANICAL'),
    ('RM', 'RIMS'),
    ('SPI', 'SPOILER'),
    ('WRP', 'WRAPS'),
    ('LED', 'LEDLIGHTS'),
    ('ACS', 'ACCESSORIES'),
    ('TR', 'TYRES')
  ]
  user = models.ForeignKey(User, on_delete = models.CASCADE)
  product = models.CharField(max_length = 250)
  photo = models.ImageField(upload_to = 'photos/', blank=True, null=True)
  type = models.CharField(max_length = 4, choices = PRODUCT_TYPE_CHOICE)
  details = models.TextField(max_length = 500, default = 'empty')
  warranty = models.CharField(max_length = 250, default = 'N/A')
  price = models.DecimalField(max_digits=10, decimal_places=2)
  date_added = models.DateTimeField(default = timezone.now)

  def __str__(self):
    return self.product
  


