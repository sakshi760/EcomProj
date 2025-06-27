from django.db import models
from django.contrib.auth.models import User

# State choices
CITY_CHOICES = (
    ('Mumbai', 'Mumbai'),
    ('Pune', 'Pune'),
    ('Nagpur', 'Nagpur'),
    ('Nashik', 'Nashik'),
    ('Thane', 'Thane'),
    ('Aurangabad', 'Aurangabad'),
    ('Solapur', 'Solapur'),
    ('Amravati', 'Amravati'),
    ('Kolhapur', 'Kolhapur'),
    ('Navi Mumbai', 'Navi Mumbai'),
    ('Kalyan-Dombivli', 'Kalyan-Dombivli'),
    ('Vasai-Virar', 'Vasai-Virar'),
    ('Mira-Bhayandar', 'Mira-Bhayandar'),
    ('Bhiwandi', 'Bhiwandi'),
    ('Malegaon', 'Malegaon'),
    ('Jalgaon', 'Jalgaon'),
    ('Akola', 'Akola'),
    ('Latur', 'Latur'),
    ('Dhule', 'Dhule'),
    ('Ahmednagar', 'Ahmednagar'),
    ('Chandrapur', 'Chandrapur'),
    ('Parbhani', 'Parbhani'),
    ('Ichalkaranji', 'Ichalkaranji'),
    ('Sangli', 'Sangli'),
    ('Jalna', 'Jalna'),
    ('Nanded', 'Nanded'),
    ('Ratnagiri', 'Ratnagiri'),
    ('Beed', 'Beed'),
    ('Yavatmal', 'Yavatmal'),
    ('Osmanabad', 'Osmanabad'),
    ('Satara', 'Satara'),
    ('Wardha', 'Wardha'),
    ('Gondia', 'Gondia'),
    ('Baramati', 'Baramati'),
    ('Hingoli', 'Hingoli'),
    ('Buldhana', 'Buldhana'),
    ('Washim', 'Washim'),
)


CATEGORY_CHOICES = (
    ('DR', 'Drinks'),
    ('MM', 'Momos'),
    ('SC', 'Snacks'),
    ('DS', 'Desserts'),
    ('MF', 'Muffins'),
    ('CK', 'Cookies'),
    ('VW', 'Veggie Wraps'),
    ('FR', 'Fries'),
    ('GB', 'Garlic Bread'),
    ('GS', 'Sandwiches'),
    ('MH', 'Mocha'),
    ('MC', 'Masala Chai'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField()  # Fixed the typo (conposition -> composition)
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')

    def __str__(self):
        return self.title

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(choices=CITY_CHOICES,max_length=100)
    mobile = models.IntegerField(default=0)  # Changed to CharField to handle phone numbers
    zipcode = models.IntegerField()
    state = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
)

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=False)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,default='')
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

#class CartItem(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    #product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    #quantity = models.PositiveIntegerField(default=1)
    #date_added = models.DateTimeField(auto_now_add=True)

    #def __str__(self):
        #return f"{self.product.title} - {self.quantity}"

    # You can also add a method to get the total price for the cart item
    #def total_price(self):
        #return self.product.price * self.quantity

    #class Meta:
        #verbose_name = 'Cart Item'
        #verbose_name_plural = 'Cart Items'