from django.shortcuts import render, redirect
from .models import *
import json
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from .forms import *
from django.urls import reverse_lazy, reverse

from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user, allowed_users

from django.contrib.auth.models import Group

from django.db.models import Avg

from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage

import json

import requests

import datetime
# from rest_framework.viewsets import ModelViewSet

# from .serializers import ProductSerializer, RatingSerializer

# from rest_framework.permissions import IsAuthenticated

# Create your views here.
# @login_required(login_url='login')

# @allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def index(request):
   
    dests = Destination.objects.all()

    feedbacks = Feedback.objects.all()

    value=0

    if Feedback.objects.filter(customer = request.user.customer).exists(): 
         value=1

     
    user = request.user.customer
    count = 0
    orders = Order.objects.filter(customer=user)
    if orders.count() == 0:
         count = 0
    #if Order.objects.filter(customer=user).exists():
    else:
          count = 1

    context = {'dests': dests, 'feedbacks': feedbacks, 'value':value, 'count': count}    
    return render(request, 'index.html', context)


def feedback(request):
     form = FeedbackForm()
     if request.method == "POST":
          form = FeedbackForm(request.POST)
          if form.is_valid():
               feedback = form.save(commit=False)
               feedback.customer = request.user.customer
               feedback.save()
               return redirect('home')
          
     context = {'form': form}
     return render(request, 'feedback.html', context)


def search(request):
    # blogdatas = Blogs.objects.all()
    query = request.GET['query']
    if len(query) > 80:
        blogdatas= Blogs.objects.none()
    else:
        # blogdatasname = Blogs.objects.filter(name__icontains=query)
        # blogdatastag = Blogs.objects.filter(tag__icontains=query)
        blogdatasdesc = Blogs.objects.filter(description__icontains=query)

        # blogdatas = blogdatasname.union(blogdatastag)
        # blogdatas1 = blogdatas.union(blogdatasdesc)
        paginator = Paginator(blogdatasdesc, 1)
        page_number = request.GET.get('page')
        try:
             blogdatasdesc = paginator.page(page_number)
        except PageNotAnInteger:
             blogdatasdesc =paginator.page(1)
        except EmptyPage:
             blogdatasdesc = paginator.page(paginator.num_pages)
             
             
             
        # final = paginator.get_page(page_number)

    # if blogdatas.count(datas) == 0:
    #     messages.warning(request, "No Search results found. Please refine your keyword.")
    context = {'blogdatas': blogdatasdesc, 'query': query, 'page': page_number}
    return render(request, 'search.html', context)

def custom(request):
    data = json.loads(request.body)
    # print(data)
    # name = form['name']

    Custom.objects.create(
        name = data['form']['name'],
        destnation = data['form']['destination'],
        activity = data['form']['activity'],
        duration = data['form']['duration'],
        date = data['form']['date'],
    )
    print(data['form']['name'])


    return JsonResponse('Payment Complete', safe=False)

@unauthenticated_user
def loginPage(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            
            else:
                messages.info(request, "Username or Password incorrect")
                return render(request, 'login.html')

        context = {}
        return render(request, 'login.html', context)

@unauthenticated_user
def register(request):
     form = CreateUserForm()

     if request.method == 'POST':
          form = CreateUserForm(request.POST)
          if form.is_valid():
               user =form.save()
               username = form.cleaned_data.get('username')

               group = Group.objects.get(name = 'customer')

               user.groups.add(group)

               Customer.objects.create(
                    user = user,
                    name= user.username,
               )

          messages.success(request, 'Account was created for ' + username )
          return redirect('login')
     context = {'form': form}
     return render(request, 'register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
     
     context = {}
     return render(request, 'userpage.html', context)


def ratingPage(request, dest_id):
    #  user = request.user
     destination = Destination.objects.get(id=dest_id)
     reviews = Rating.objects.filter(destination=destination)
     avg_reviews = reviews.aggregate(Avg('rating'))
     reviews_count = reviews.count()
     user = request.user
     form = ratingForm()

     if request.method == 'POST':
          form = ratingForm(request.POST)
          
          if form.is_valid:
               rate = form.save(commit=False)
               rate.user = request.user
               rate.destination = destination
               rate.save()
               return redirect('home')

     context = {'form': form, 'destination': destination, 'avg_reviews' : avg_reviews,'reviews_count' : reviews_count}
     return render(request, 'rating.html', context)
# from rest framework


def destination_details(request, dest_id):
     
    if Destination.objects.filter(id=dest_id).exists():
        destination = Destination.objects.get(id=dest_id)
        reviews = Rating.objects.filter(destination=destination)
        avg_reviews = reviews.aggregate(Avg('rating'))
        reviews_count = reviews.count()

    user = request.user
    print(user, destination)
    count=0
    if Rating.objects.filter(user=user, destination=destination).exists():
         count = 1
    

    context = {'destination': destination, 'reviews_count': reviews_count, 'avg_reviews': avg_reviews, 'reviews':reviews, 'count': count}
    return render(request, 'destination_details.html', context)


def maps(request):
     return render(request, 'maps.html')

def mapsktm(request):
     return render(request, 'mapsktm.html')
def mapsbkt(request):
     return render(request, 'mapsbkt.html')
def mapslpr(request):
     return render(request, 'mapslpr.html')

def mapsboudha(request):
     return render(request, 'mapsboudha.html')
     

def products(request):
     if request.user.is_authenticated:
        customer = request.user.customer    
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
       
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items_number
     else:
        items =[]
        order = {'get_cart_total':0, 'get_cart_items_number':0, 'shipping': False}
        cartItems = order['get_cart_items_number']
     products = product.objects.all()
     context = {'products': products, 'cartItems': cartItems}
     return render(request, 'products.html', context)

def update_item(request):
     data = json.loads(request.body)
     productId = data['productId']
     action = data['action']

     print('Product', productId)
     print('action', action)

     customer = request.user.customer
     productt = product.objects.get(id=productId)
     order, created = Order.objects.get_or_create(customer=customer, complete = False)
     orderItem, created = OrderItem.objects.get_or_create(order=order, product=productt)


     if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
     elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

     orderItem.save()

     if orderItem.quantity <= 0:
        orderItem.delete()
     return JsonResponse('Item was added', safe=False)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer    
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
       
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items_number
    else:
        items =[]
        order = {'get_cart_total':0, 'get_cart_items_number':0}
        cartItems = order['get_cart_items_number']
        #for item in items:
            #count = item.quantity * item.product.price
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, "cart.html", context,)

def viewPage(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer= customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items_number

    else:
        items=[]
        order = {'get_cart_total': 0, 'get_cart_items_number': 0}
        cartItems = order['get_cart_items_number']
    form = OrderForm()
        
#     if request.method == "POST":
       
#             form = OrderForm(request.POST)
            
#             # rate = form.save(commit=False)
#             # rate.save()
#             orderForm = form.save(commit=False)
            
#             orderForm.save()

#             print(orderForm.id)
            
#             pm = form.cleaned_data.get("payment_method")
#             print(pm)
#             if pm == "Khalti":
#                print("Payment method is khalti")
#                return redirect(reverse("khalti-request-cart") + "?o_id=" + str(orderForm.id))
#             #  elif pm == "Esewa":
            #      return redirect(reverse("ecomapp:esewarequest") + "?o_id=" + str(order.id))
        
#     context={'form':form}
#     form = OrderForm()
        
#     if request.method == "POST":
       
#             form = OrderForm(request.POST)
#             orderForm = form.save(commit=False)
         
#             # rate = form.save(commit=False)
#             # rate.save()
            
            
#             pm = form.cleaned_data.get("payment_method")
#             print(pm)
#             if pm == "Khalti":
#                  print("Payment method is khalti")
#                  return redirect(reverse("khalti-request") + "?o_id=" )
#             # elif pm == "Esewa":
#             #     return redirect(reverse("ecomapp:esewarequest") + "?o_id=" + str(order.id))
        
        

    context = {'items': items, 'order': order, 'cartItems': cartItems, "form":form}
    return render(request, "view.html", context)

def processOrder(request):
     transaction_id = datetime.datetime.now().timestamp()

     

     if request.user.is_authenticated:
          customer = request.user.customer
          data = json.loads(request.body)
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          total = float(data['form']['total'])
          order.transaction_id = transaction_id

          print(total)
          print(order.get_cart_total)
          if total == order.get_cart_total:
               order.complete = True
               order.save()

    
          ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
            )
     else:
          print('user is not logged in..')
     return JsonResponse('Payment completed', safe=False)

        
@login_required(login_url='login')
def payment(request, dest_id):
        destination = Destination.objects.get(id=dest_id)
        form = CheckoutForm()
        
        if request.method == "POST":
       
            form = CheckoutForm(request.POST)
            
            # rate = form.save(commit=False)
            # rate.save()
            order = form.save(commit=False)
            order.destination = destination
            order.price = destination.price
            order.ordered_by = request.user
            order.save()

            print(order.id)
            
            pm = form.cleaned_data.get("payment_method")
            print(pm)
            if pm == "Cash on Delivery":
                 return redirect(reverse("cashondelivery")+ "?o_id=" + str(order.id) + "&dest_id=" + str(dest_id))
            if pm == "Khalti":
                 print("Payment method is khalti")
                 return redirect(reverse("khalti-request") + "?o_id=" + str(order.id) + "&dest_id=" + str(dest_id))
            elif pm == "Esewa":
                 return redirect(reverse("esewa-request") + "?o_id=" + str(order.id) + "&dest_id=" + str(dest_id))
        
        context={'form':form}
        return render(request, 'payment.html', context)
   
    # dests = Destination.objects.all()
    # context = {'dests': dests}   
        


def KhaltiRequest(request):
    o_id = request.GET.get("o_id")
    dest_id = request.GET.get("dest_id")
    destination = Destination.objects.get(id = dest_id)
    order = Destination_Order.objects.get(id = o_id)
    context = {"destination": destination, "order": order}
    return render(request, "khaltirequest.html", context)

def cashondelivery(request):
    o_id = request.GET.get("o_id")
    dest_id = request.GET.get("dest_id")
    destination = Destination.objects.get(id = dest_id)
    order = Destination_Order.objects.get(id = o_id)
    context = {"destination": destination, "order": order}
    return render(request, "cashondelivery.html", context)


def KhaltiVerify(request):
     context = {}
     token = request.GET.get("token")
     amount = request.GET.get("amount")
     order_id = request.GET.get("order_id")

     url = "https://khalti.com/api/v2/payment/verify/"

     payload = {
     'token': token,
     'amount': amount
     }

     headers = {
     'Authorization': 'Key test_secret_key_17ade6c645e640b1a2f9bdab45ba808f'
     }

     order_obj = Destination_Order.objects.get(id=order_id)
     response = requests.request("POST", url, headers=headers, data=payload)
     resp_obj = response.json()
     if resp_obj.get("idx"):
          success = True
          order_obj.payment_completed = True
          
          order_obj.save()

     else:
          success = False



     print(token, amount, order_id)
     data={
          "success" : success
     }
     return JsonResponse(data)


def EsewaRequest(request):
     o_id = request.GET.get("o_id")
     dest_id = request.GET.get("dest_id")
     destination = Destination.objects.get(id=dest_id)

     context = {'destination': destination}
     return render(request, "EsewaRequest.html", context )


@login_required(login_url='login')
def payment1(request):
    

    return render(request, 'view.html')

#     return render(request, 'payment.html')

def KhaltiRequestCart(request):
     o_id = request.GET.get("o_id")
     
     customer = request.user.customer
     order, created = Order.objects.get_or_create(customer=customer, complete=False)
     print(order.get_cart_total)


   

     
   
    
#     dest_id = request.GET.get("dest_id")
#     destination = Destination.objects.get(id = dest_id)
#     order = Destination_Order.objects.get(id = o_id)
     context = {"order": order}
     return render(request, "khaltirequestcart.html", context )

def submit_order(request):
     order_id = request.GET.get("order_id")
     if request.user.is_authenticated:
          customer = request.user.customer
          order_obj, created = Order.objects.get_or_create(id=order_id)  
          order_obj.complete = True
          order_obj.save()
          return redirect("home")


def KhaltiVerifyCart(request):
     context = {}
     token = request.GET.get("token")
     amount = request.GET.get("amount")
     order_id = request.GET.get("order_id")

     url = "https://khalti.com/api/v2/payment/verify/"

     payload = {
     'token': token,
     'amount': amount
     }

     headers = {
     'Authorization': 'Key test_secret_key_17ade6c645e640b1a2f9bdab45ba808f'
     }

     if request.user.is_authenticated:
          customer = request.user.customer
          order_obj, created = Order.objects.get_or_create(id=order_id)
          response = requests.request("POST", url, headers=headers, data=payload)
          resp_obj = response.json()
          if resp_obj.get("idx"):
               success = True
               order_obj.payment_completed = True
               order_obj.payment_method = "Khalti"
               order_obj.complete = True
               order_obj.save()
               # orderItem, created = OrderItem.objects.get_or_create(order=order_obj, product=productt)

          else:
               success = False



          print(token, amount, order_id, order_obj)
          data={
               "success" : success
          }
          return JsonResponse(data)
     


def UserProfile(request):
     customer = request.user.customer
     userOrder = Order.objects.filter(customer=customer)
     userdestOrder = Destination_Order.objects.filter(ordered_by=request.user)
     for orders in userOrder:
          print(orders , orders.orderitem_set.all())
          
     for order in userdestOrder:
          print(order)


     context = {'userOrder': userOrder, 'userdestOrder': userdestOrder}

     return render(request, "userpage.html", context)

def showOrderitems(request, order_id):
     order = Order.objects.get(id=order_id)
     orderitems = order.orderitem_set.all()
     context = {'orderitems': orderitems, 'order':order}
     return render(request, 'orderitems.html', context)


def update_review(request, dest_id, review_id):
     review =  Rating.objects.get(id = review_id)
     form = ratingForm(instance=review)
     destination = Destination.objects.get(id=dest_id)

     if request.method == 'POST':
          form = ratingForm(request.POST, instance=review)
          if form.is_valid():
               form.save()
               return redirect('home')

     context = {'form': form, 'destination': destination}
     return render(request, 'rating.html', context)

def delete_review(request, dest_id, review_id):
     review = Rating.objects.get(id=review_id)
     if request.method == "POST":
          review.delete()
          return redirect('home')
     context = {'review': review}
     return render(request, 'delete_review.html', context)



