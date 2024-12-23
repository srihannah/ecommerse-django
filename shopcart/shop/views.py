from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from shop.form import customUserForm,CheckoutForm,OrderForm
from .models import *
import json
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
 

 

def home(request):
    products= Product.objects.filter(trending=1)
    return render(request,'shop/home.html',{'products':products})

def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart")

def remove_fav(request,fid):
    favouriteitem=Favourite.objects.get(id=fid)
    favouriteitem.delete()
    return redirect("/favviewpage")

def favviewpage(request):
   if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        return render(request,"shop/fav.html",{"fav":fav})

def cart_page(request):
    cart = Cart.objects.filter(user=request.user)  # Assuming user is authenticated
    # Add logic here to get the product ID
    product = cart.first().product if cart.exists() else None  # Example of getting a product

    return render(request, "shop/cart.html", {
        "cart": cart,
        "product": product,  # Pass the product to the template
    })
 
def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=Product.objects.get(id=product_id)
      if product_status:
         if Favourite.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Favourite.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)

def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty =data['product_qty']
            product_id=data['pid']
            # print(request.user.id)
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Cart'}, status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Added to Cart'}, status=200)
                    else:
                        return JsonResponse({'status':'Product Stock Not Available'}, status=200)
          
        else:
            return JsonResponse({'status':'Login to Add Cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Loout  Successfully....")
    return redirect("/")
    

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
     if request.method=='POST':
        name=request.POST.get('username')
        pwd= request.POST.get('password')
        user = authenticate(request,username=name,password=pwd)
        if user is not None:
            login(request,user)
            messages.success(request,"Login Successfully....")
            return redirect("/")
    return render(request,'shop/login.html')

def register(request):
    form=customUserForm()
    if request.method=='POST':
        form=customUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success You Can Login Now....!")
            return redirect('/login')
    return render(request,'shop/register.html',{'form':form})

def collection(request):
    catagory = Catagory.objects.filter(status=0)
    return render(request,'shop/collection.html',{'catagory':catagory})
    
def collectionview(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
       products = Product.objects.filter(Category__name=name)
       return render(request,'shop/products/index.html',{'products':products,"category_name":name})
    else:
        messages.warning(request,"no such catagory found")
        return redirect('collection')
    

def product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request, "shop/products/product_details.html", {"products": products})
        else:
            messages.error(request,"No such Product found")
            return redirect('collection')
    else:
        messages.error(request,"No such catagory found")
        return redirect('collection')
    
def checkout(request, product_id):
    # Fetch the specific product using product_id
    product = get_object_or_404(Product, id=product_id)
    cart_total = product.selling_price 
    cart = Cart.objects.filter(user=request.user)  # Assuming the user is authenticated
    cart_total = sum(item.total_cost for item in cart) # Replace with logic if there are multiple items

    if request.method == 'POST':
        form = OrderForm(request.POST)  # Initialize form with POST data
        if form.is_valid():
            try:
                # Create order object but don't save to database yet
                order = form.save(commit=False)
                order.user = request.user
                order.total = cart_total
                order.save()  # Save order to database

                # Handle payment processing here (if applicable)

                # Optionally clear cart or handle product-specific actions
                # Cart.objects.filter(user=request.user).delete() # Uncomment if using a cart

                messages.success(request, "Order placed successfully!")
                return redirect('order_success')
            except Exception as e:
                # Log the exception if any occurs during save
                print(f"Error saving order: {e}")
                messages.error(request, 'Failed to place the order. Please try again.')
        else:
            # Print form errors to debug validation issues
            print("Form is not valid. Errors:", form.errors)
            messages.error(request, "There was an error with your order. Please check your details.")
    else:
        form = OrderForm()

    return render(request, 'shop/checkout.html', {
        'form': form,
        'product': product,
        'cart': cart,
        'cart_total': cart_total,
    })


def checkout_home(request, product_id):
    # Fetch a single Product instance based on the product_id
    product = get_object_or_404(Product, id=product_id)

    # Calculate the cart total for a single product scenario
    cart_total = product.selling_price  # Ensure product is a single instance, not a QuerySet

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                # Prepare the order but do not save to the database yet
                order = form.save(commit=False)
                order.user = request.user  # Link the order to the current logged-in user
                order.total = cart_total
                order.save()  # Save order to generate an order ID

                # Create an order item (or order entry) for the selected product
                Order.objects.create(
                    order=order,
                    product=product,
                    quantity=1,  # Quantity is 1 in this simplified example
                    price=product.selling_price
                )

                # Success message and redirect to the order success page
                messages.success(request, "Order placed successfully!")
                return redirect('order_success')
            except Exception as e:
                # Catch errors related to saving orders and display a message
                print(f"Error saving order: {e}")
                messages.error(request, 'Failed to place the order. Please try again.')
        else:
            # Handle case when the form is invalid
            print("Form is not valid. Errors:", form.errors)
            messages.error(request, "There was an error with your order. Please check your details.")
    else:
        # Initialize a new form for GET requests
        form = OrderForm()

    # Render the checkout page with the form, product, and cart total
    return render(request, 'shop/checkout.html', {
        'form': form,
        'product': product,
        'cart_total': cart_total,
    })

def order_success(request):
    return render(request, 'shop/order_success.html')






