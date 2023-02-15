from django.db import models
from django.contrib.auth.models import User

# Create your models here
STATE_CHOICES=(
    ('Andaman and Nicobar Island','Andaman and Nicobar Island'),
    ('Andra pradesh','Andra pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Kerala','Kerala'),
    ('Delhi','Delhi'),
    ('Goa','Goa'),
    ('Hariyana','Hariyana'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Tamilnadu','Tamilnadu'),
    ('Karnataka','Karnataka'),
    ('WestBengal','WestBengal'),
    ('Uttarpradesh','Uttarpradesh'),
    ('Madhyapradesh','Madhyapradesh'),
    ('Gujarat','Gujarat'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Odisa','Odisa'),
    ('Nagaland','Nagaland'),
    ('Sikkim','Sikkim'),
    ('Uttarakhand','Uttarakhand'),
    ('Arunachalpradesh','Arunachalpradesh'),
    ('Jammukashmir','Jammukashmir'),


)

CATEGORY_CHOICES=(
    ('CR','Curd'),
    ('ML','Milk'),
    ('LS','Lassi'),
    ('MS','Milkshake'),
    ('GH','Ghee'),
    ('PN','Paneer'),
    ('CZ','Cheese'),
    ('IC','Ice-creams'),
)

    

class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    composition=models.TextField(default='')
    prodapp=models.TextField(default='')
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image=models.ImageField(upload_to='product')
    def __str__(self):
        return self.title


class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    mobile=models.IntegerField(default=91)
    state=models.CharField(choices=STATE_CHOICES,max_length=100)

    zipcode=models.IntegerField()
    
    def __str__(self):
        return self.name


class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    

STATUS_CHOICES= (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way','On the way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
)       
class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.FloatField()

    razorpay_order_id=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id=models.CharField(max_length=100,blank=True,null=True)
    paid=models.BooleanField(default=False)


class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='Accepted')
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

class Wishlist(models.Model):
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     product=models.ForeignKey(Product,on_delete=models.CASCADE)
    


