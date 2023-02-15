from django.shortcuts import render,redirect
from django .views  import View
from . models import Product,Customer,Cart,OrderPlaced,Wishlist
from django.db.models import Count
from . forms import CustomerRegistrationForm, CustomerProfileForm 
from django.contrib import messages
from django.http import JsonResponse  
from django.db.models import Q  
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

    


# Create your views here.
@login_required
def home(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))

    return render(request,"home.html",locals())
@login_required    
def about(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"about.html",locals())
@login_required    
def contact(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"contact.html",locals())

@method_decorator( login_required,name='dispatch')
class CategoryView(View):
    def get(self,request,val):
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
          wishitem = len(Wishlist.objects.filter(user=request.user))
        product=Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title')
        return render(request,'category.html',locals()) 
@method_decorator( login_required,name='dispatch')
class CategoryTitle(View):
    def get(self,request,val):
        product=Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        totalitem = 0
        wishitem=0
       
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))

        return render(request,'category.html',locals()) 
@method_decorator( login_required,name='dispatch')
class ProductDetail(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        wishlist=Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
           wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request,'productdetail.html',locals()) 

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
           wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request,'customerregistration.html',locals()) 
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)    
        if form.is_valid():
            form.save()
            messages.success(request,"congratulation!user register successfully")
        else:
            messages.warning(request,"invalid data")    
        return render(request,'customerregistration.html',locals())     
@method_decorator( login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request,'profile.html',locals()) 
    def post(self,request):
       form = CustomerProfileForm(request.POST)
       if form.is_valid():
          user=request.user
          name=form.cleaned_data['name']
          locality=form.cleaned_data['locality']
          city=form.cleaned_data['city']
          mobile=form.cleaned_data['mobile']
          state=form.cleaned_data['state']
          zipcode=form.cleaned_data['zipcode']
          reg=Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
          reg.save()
          messages.success(request,"congratulations profile save successfully")
       else:
        messages.warning(request,"Invalid Data") 

       return render(request,'profile.html',locals()) 
@login_required    
def address(request):
    add=Customer.objects.filter(user=request.user)
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,'address.html',locals())
@method_decorator( login_required,name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
       add=Customer.objects.get(pk=pk)
       form = CustomerProfileForm(instance=add)
       totalitem = 0
       wishitem=0
       if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
          wishitem = len(Wishlist.objects.filter(user=request.user))

       return render(request,'updateAddress.html',locals())

    def post(self,request,pk):
       form = CustomerProfileForm(request.POST)
       if form.is_valid():
          add=Customer.objects.get(pk=pk)

          
          add.name=form.cleaned_data['name']
          add.locality=form.cleaned_data['locality']
          add.city=form.cleaned_data['city']
          add.mobile=form.cleaned_data['mobile']
          add.state=form.cleaned_data['state']
          add.zipcode=form.cleaned_data['zipcode']
          
          add.save()
          messages.success(request,"congratulations profile update successfully")
       else:
        messages.warning(request,"Invalid Data") 
       return redirect('address')
@login_required    
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id = product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")
@login_required    
def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.quantity * p.product.discounted_price
        amount=amount + value
    totalamount= amount + 40
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,'addtocart.html',locals())    
@method_decorator( login_required,name='dispatch')
class checkout(View):
    def get(self,request):
        totalitem = 0
        wishitem=0
         
        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
           wishitem = len(Wishlist.objects.filter(user=request.user))
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount= famount + value
        totalamount= famount + 40
        

        return render(request,'checkout.html',locals())    
@login_required    
def orders(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
           wishitem = len(Wishlist.objects.filter(user=request.user))
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request,'orders.html',locals())
       
def plus_cart(request):
  if request.method == 'GET':
    prod_id=request.GET['prod_id']
    
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity +=1
    c.save()
    user=request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    
    data={
        'quantity':c.quantity,
        'amount':amount,
        'totalamount':totalamount


    }
    return JsonResponse(data)
  
def minus_cart(request):
  if request.method == 'GET':
    prod_id=request.GET['prod_id']
    
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity -=1
    c.save()
    user=request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    
    data={
        'quantity':c.quantity,
        'amount':amount,
        'totalamount':totalamount


    }
    return JsonResponse(data)
   
def remove_cart(request):
  if request.method == 'GET':
    prod_id=request.GET['prod_id']
    
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.delete()
    user=request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    
    data={
       
        'amount':amount,
        'totalamount':totalamount


    }
    return JsonResponse(data)
@login_required    
def cod(request):
    user=request.user
   
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,product=c.product,quantity=c.quantity).save()
        c.delete()

    return redirect('orders')    
@login_required    
def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request,'orders.html',locals())    
  
def plus_wishlist(request):
     if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user=request.user
        Wishlist(user=user,product=product).save()
        data={
           'message':"wishlist added successfully",
        }
        return JsonResponse(data)
 
def minus_wishlist(request):
     if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user=request.user
        Wishlist.objects.filter(user=user,product=product).delete()
        data={
           'message':"wishlist deleted successfully",
        }
        return JsonResponse(data)
@login_required    
def search(request):
    query=request.GET['search']
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
           wishitem = len(Wishlist.objects.filter(user=request.user))
    product=Product.objects.filter(Q(title__icontains=query))  
    return render(request,'search.html',locals())
