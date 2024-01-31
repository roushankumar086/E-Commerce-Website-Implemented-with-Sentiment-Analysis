from django.shortcuts import render,redirect
from .models import*
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.db import connection
from django.db.models import Sum
import math
import socket
import geocoder
import pycountry
from requests import get
import json
from django.db.models import Avg
import datetime
from datetime import date
from django.urls import reverse
import requests
from textblob import TextBlob
import matplotlib.pyplot as plt


# Create your views here.


def Home(request):
	return render(request,"Home.html",{})

def Admin_Login(request):
	if request.method == "POST":
		A_username = request.POST['aname']
		A_password = request.POST['apass']
		if AdminDetails.objects.filter(username = A_username,password = A_password).exists():
			ad = AdminDetails.objects.get(username=A_username, password=A_password)
			print('d')
			messages.info(request,'Admin login is Sucessfull')
			request.session['type_id'] = 'Admin'
			request.session['UserType'] = 'Admin'
			request.session['login'] = "Yes"
			return redirect("/")
		else:
			print('y')
			messages.error(request, 'Error wrong username/password')
			return render(request, "Admin_Login.html", {})
	else:
		return render(request, "Admin_Login.html", {})

def User_Login(request):
	if request.method == "POST":
		C_name = request.POST['aname']
		C_password = request.POST['apass']
		if userDetails.objects.filter(Username=C_name,Password=C_password,Status="Accepted").exists():
			users = userDetails.objects.all().filter(Username=C_name,Password=C_password)
			messages.info(request,C_name +' logged in')
			request.session['UserId'] = users[0].id
			request.session['type_id'] = 'User'
			request.session['UserType'] = C_name
			request.session['login'] = "Yes"
			return redirect('/')
		else:
			messages.info(request, 'Admin will accept your request')
			return redirect("/User_Login/")
	else:
		return render(request,'User_Login.html',{})

def User_Registration(request):
	if request.method == "POST":
		Name= request.POST['name']
		Age= request.POST['age']
		Phone= request.POST['phone']
		Email= request.POST['email']
		Address= request.POST['address']
		Username= request.POST['Username']
		Password= request.POST['Password']
		if userDetails.objects.all().filter(Username=Username).exists():
			messages.info(request,"Username Taken")
			return redirect('/User_Registeration')
		else:
			obj = userDetails(
			Name=Name
			,Age=Age
			,Phone=Phone
			,Email=Email
			,Address=Address
			,Username=Username
			,Password=Password
			,Status = "Pending")
			obj.save()
			messages.info(request,Name+" Registered")
			return redirect('/User_Login')
	else:
		return render(request,"User_Registration.html",{})

def View_User(request):
	details = userDetails.objects.all()
	return render(request,"View_User.html",{'details':details})

def Update_Status(request,id):
	userDetails.objects.filter(id=id).update(Status="Accepted")
	return redirect('/View_User/')


def Manage_Product(request):
	data  =  Product.objects.all()
	return render(request,"Manage_Product.html",{'data':data})


def Add_Product(request):
	if request.method == "POST":
		P_name = request.POST['name']
		P_price = request.POST['price']
		P_image = request.FILES['image']
		obj = Product(Product_Image=P_image
					,Product_Name=P_name
					,Product_Price=P_price)
		obj.save()
		messages.info(request,"Product Added")
		return redirect("/Manage_Product/")
	else:
		return render(request,"Add_Product.html",{})



def Delete_Product(request,id):
	delcomp = Product.objects.get(id=id) 
	delcomp.delete()
	return redirect('/Manage_Product/')


def ViewProduct(request,id):
	Product_ID= id
	details = Product.objects.filter(id = id)
	data = Comments.objects.filter(pid=id)
	return render(request,"ViewProduct.html",{'details':details,'Product_ID':Product_ID,"data":data})

def Cart(request):

	if request.method == "POST":
		user_id = request.session['UserId']
		print('Userid: ',user_id)
		prod_id = request.POST['Product_id']
		print('Productid: ',prod_id)
		quantity = request.POST['quantity']
		# count = []
		prod_data = Product.objects.filter(id=prod_id)
		for i in prod_data:
			Prod_name = i.Product_Name
			price = i.Product_Price

			#details=cart.objects.all().
		if cart.objects.filter(uid=user_id,prod_id=prod_id).exists():
			CartDetails = cart.objects.filter(uid=user_id,prod_id=prod_id)
			cid = CartDetails[0].id
			print('cid: ',cid)
			Qnt = CartDetails[0].Prod_quantity
			print('Qnt: ',Qnt)
			Cprice = CartDetails[0].Prod_price
			print('Cprice: ',Cprice)
			prodquantity = int(Qnt) + int(quantity)
			print('New quantity: ',prodquantity)
			ProdPrice = int(Cprice) + int(price)
			print(ProdPrice)
			TotalPrice = int(price) * int(prodquantity)
			print('TotalPrice: ',TotalPrice)
			cart.objects.filter(id=cid).update(Prod_quantity=prodquantity,Prod_price=TotalPrice)
			#details = cart.objects.all().filter(uid=user_id)
			#return render(request,'cart1.html',{'details':details})
		else:
			TotalPrice = int(price) * int(quantity)
			print('quantity: ',quantity)
			print('TotalPrice: ',TotalPrice)
			objects = cart(uid=user_id,prod_id =prod_id,Prod_name=Prod_name,Prod_price=TotalPrice,Prod_quantity=quantity,Initial_price=price)
			objects.save()
		CT = cart.objects.filter(uid=user_id).aggregate(Sum('Prod_price'))
		CartTotal = CT['Prod_price__sum']
		print(CT)
		print(CartTotal)
		count = cart.objects.filter(uid=user_id)
		print(count)
		count = len(count)
		print(count)		
		details = cart.objects.all().filter(uid=user_id)
		return render(request,'Cart.html',{'details':details,'CartTotal':CartTotal})
	else:
		user_id = request.session['UserId']
		CT = cart.objects.filter(uid=user_id).aggregate(Sum('Prod_price'))
		CartTotal = CT['Prod_price__sum']
		print(CT)
		print(CartTotal)
		count = cart.objects.filter(uid=user_id)
		print(count)
		count = len(count)
		print(count)
		if count == 0:
			print("Cart is empty")

		details = cart.objects.all().filter(uid=user_id)
		return render(request,'Cart.html',{'details':details,'CartTotal':CartTotal,'count':count})

def deletecart(request,id):
	cart.objects.filter(id=id).delete()
	return redirect('/Cart')

def Checkout(request):
	user_id = request.session['UserId']
	CT = cart.objects.filter(uid=user_id).aggregate(Sum('Prod_price'))
	quantity =  cart.objects.filter(uid=user_id).aggregate(Sum('Prod_quantity'))
	print(quantity)
	quantity = quantity['Prod_quantity__sum']
	print(quantity)
	carts = []
	quant = []
	CartTotal = CT['Prod_price__sum']
	print(CT)
	print(CartTotal)
	CartTotal = int(CartTotal)
	print(CartTotal)
	quant.append(quantity)
	carts.append(CartTotal)
	print(carts)
	info = userDetails.objects.all().filter(id=user_id)
	details = cart.objects.all().filter(uid=user_id)
	return render(request,'Checkout.html',{'details':details,'carts':carts,'quant':quant,'info':info,'CartTotal':CartTotal})


def Order(request):
	user_id = request.session['UserId']
	CT = cart.objects.filter(uid=user_id).aggregate(Sum('Prod_price'))
	quantity =  cart.objects.filter(uid=user_id).aggregate(Sum('Prod_quantity'))
	print(quantity)
	quantity = quantity['Prod_quantity__sum']
	print(quantity)
	carts = []
	quant = []
	CartTotal = CT['Prod_price__sum']
	print(CT)
	print(CartTotal)
	CartTotal = int(CartTotal)
	print(CartTotal)
	quant.append(quantity)
	carts.append(CartTotal)
	print(carts)
	info = userDetails.objects.all().filter(id=user_id)
	details = cart.objects.all().filter(uid=user_id)
	names = []
	for i in details:
		U_id = details[0].uid
	print("User :"+U_id)
	Product_Names = []
	Product_Id = []
	Prod_Q = []
	for i in details:
		Names = i.Prod_name
		ID = str(i.prod_id)
		q = str(i.Prod_quantity)
		print(f"{ID}/{Names} ({q})")
		Product_Names.append(f"{ID}/{Names} ({q})")
		Product_Id.append(ID)
		Prod_Q.append(q)
	print("Product_Names :"+str(Product_Names))
	Names = ','.join(Product_Names)
	ID = ','.join(Product_Id)
	q = ','.join(Prod_Q)
	print(Names)
	print(ID)
	today = date.today()
	obj = UserOrder(uid=user_id,Total=CartTotal,Items=Names,Status="Pending")
	obj.save()
	messages.info(request,"Order Saved")
	cart.objects.all().filter(uid=user_id).delete()
	return redirect('/Manage_Product')



def Add_Comments(request):
	if request.method == "POST":
		prod_id = request.POST['Product_id']
		print(prod_id)
		comment = request.POST['comment']
		user_id = request.session['UserId']
		user= userDetails.objects.get(id=user_id)
		obj = Comments(uid=user,comment=comment,pid=prod_id)
		obj.save()
		messages.info(request,"Review Posted")
	return redirect('/ViewProduct/'+str(prod_id))


def Logout(request):
	Session.objects.all().delete()
	return redirect("/")


def show_plot(request, product_id):
    # Fetch the comments for the specified product_id
    comments = Comments.objects.filter(pid=product_id)
    
    if comments:
        sentiments = []
        
        # Perform sentiment analysis on each comment
        for comment in comments:
            analysis = TextBlob(comment.comment)
            if analysis.sentiment.polarity > 0:
                sentiment = "Positive"
            elif analysis.sentiment.polarity < 0:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"
            
            sentiments.append(sentiment)
        
        # Count the occurrences of each sentiment
        sentiment_counts = {
            "Positive": sentiments.count("Positive"),
            "Negative": sentiments.count("Negative"),
            "Neutral": sentiments.count("Neutral")
        }
        
        # Plot the sentiment distribution as a pie chart
        labels = sentiment_counts.keys()
        counts = sentiment_counts.values()
        
        plt.pie(counts, labels=labels, autopct='%1.1f%%')
        plt.title("Sentiment Analysis")
        plt.axis('equal')
        plt.show()
    
    # Redirect back to manage_products page
    return redirect('Manage_Product')


def View_Order(request):
	details = UserOrder.objects.all()
	return render(request,"View_Order.html",{'details':details})


def Update_OrderStatus(request,id):
	UserOrder.objects.filter(id=id).update(Status="Accepted")
	return redirect('/View_Order/')


def Track_Order(request):
	user_id = request.session['UserId']
	details = UserOrder.objects.filter(uid=user_id)
	return render(request,"Track_Order.html",{'details':details})

def Update_DeliverStatus(request,id):
	user_id = request.session['UserId']
	UserOrder.objects.filter(id=id).update(User_Status="Delivered")
	return redirect('/Track_Order/')

def Update_Product(request):
    if request.method == "POST":
        Product_id = request.POST['updateid']
        Product_name = request.POST['updatename']
        details = Product.objects.filter(id=Product_id)
        for i in details:
            image1 = details[0].Product_Image
        uploaded_image = request.FILES.get('image', image1)
        print(uploaded_image)
        Image = "images/" + str(uploaded_image)
        description = request.POST['updatestate']
        description = description.strip()
        Product.objects.filter(id=Product_id).update(Product_Name=Product_name, Product_Price=description, Product_Image=Image)
        file_path = 'C:/Python Projects/TravelTogether/media/' + str(Image)
        with open(file_path, 'wb') as file:
            file.write(uploaded_image.read())
    return redirect('/Manage_Product')


def Ask_Queries(request):
	if request.method == "POST":
		user_id = request.session['UserId']
		query = request.POST['feedback']
		obj = Queries(User_id=user_id,Query=query)
		obj.save()
		return redirect('/Ask_Queries')
	else:
		return render(request,"Ask_Queries.html",{})


def View_Query(request):
	details = Queries.objects.all()
	return render(request,"View_Query.html",{'details':details})

def Answer(request):
	if request.method=="POST":
		query_id = request.POST['query_id']
		answer = request.POST['answer']
		Queries.objects.filter(id=query_id).update(Answer=answer)
		messages.info(request,"Query Answered")
	return redirect('/View_Query')
