from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from . models import Product
from . forms import CustomerRegistrationForm
from .forms import CustomerProfileForm
from django.contrib import messages
from .models import Customer
from .models import Cart
from django.db.models import Q
#from .forms import PaymentForm
from .models import OrderPlaced
#from .models import CartItem



# Create your views here.
def home(request):
    return render(request, "app/home.html")

def about(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, "app/about.html", {'totalitem': totalitem})

def contact(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, "app/contact.html", {'totalitem': totalitem})

def orders(request):
    return render(request, 'app/orders.html')

class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html",locals())

class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())

class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        return render(request,"app/productdetail.html",locals())

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', locals())


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations! Profile saved successfully')
            return redirect('home')  # Redirect to home page after saving profile
        else:
            messages.warning(request, 'Invalid Input Data')
        return render(request, 'app/profile.html', locals())



class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,'Congratulations! Profile Update Successfully')
        else:
            messages.warning(request,'Invalid Input Data')
        return redirect('address')

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', locals())


def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    return render(request, 'app/addtocart.html',locals())

class Checkout(View):  # Capitalize the class name
    def get(self, request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        return render(request, 'app/checkout.html', locals())

def place_order(request):
    if request.method == "POST":
        # Process the order (save to database, update stock, etc.)
        messages.success(request, "Your order has been placed successfully!")
        return redirect("home")  # Redirect to homepage after order

    return redirect("checkout") 

def orders(request):
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',locals())

def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
            totalamount = amount + 40
        data={    
            'quantity': c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)


#class PaymentFormView(View):
    #def get(self, request):
        #form = PaymentForm()  # Initialize the form
        #return render(request, 'app/payment_form.html', {'form': form})

    #def post(self, request):
        #form = PaymentForm(request.POST)
        #if form.is_valid():
            ## Handle the form submission, save data, etc.
            # Add any necessary logic here
           # return redirect('success')  # Redirect to a success page or somewhere else
        #return render(request, 'app/payment_form.html', {'form': form})

#def process_payment(request):
    #if request.method == "POST":
        # Here, you would handle the payment logic, like updating the database or contacting a payment gateway
        #messages.success(request, "Payment processed successfully!")
        #return redirect('home')  # Redirect to the home page after payment
    #else:
        #messages.error(request, "Invalid payment request")
        #return redirect('checkout') 

def process_payment(request):
    if request.method == "POST":
        selected_address = request.POST.get("selected_address")
        totalamount = request.POST.get("totalamount")

        if not selected_address:
            messages.error(request, "Please select an address before proceeding.")
            return redirect("checkout")

        # Proceed with your payment processing logic here (e.g., Razorpay integration)
        messages.success(request, "Payment successful! Your order has been placed.")
        return redirect("home")  # Redirect to homepage after successful payment

    return redirect("checkout")

#def home(request):
    # Fetch the cart items for the current user (adjust logic as needed)
    #cart_items = CartItem.objects.filter(user=request.user)
    
    # Calculate the cart item count
    #cart_item_count = cart_items.count()

    return render(request, 'app/home.html', {
        'cart_item_count': cart_item_count,
        'cart_items': cart_items
    })

#def search(request):
    #query = request.GET['search']
    #product = Product.objects.filter(Q(title_icontains=query))
    #return render(request,'app/search.html',locals())


