from django.db import models

# Create your models here.


class AdminDetails(models.Model):
	username = models.CharField(max_length=100,default=None)
	password = models.CharField(max_length=100,default=None)
	class Meta:
		db_table = 'AdminDetails'


class userDetails(models.Model):
	Username 	= models.CharField(max_length=100,default=None,null=True)
	Password 	= models.CharField(max_length=100,default=None,null=True)
	Name 		= models.CharField(max_length=100,default=None,null=True)
	Age 		= models.CharField(max_length=200,default=None,null=True)
	Phone 		= models.CharField(max_length=100,default=None,null=True)
	Email 		= models.CharField(max_length=100,default=None,null=True)
	Address 		= models.CharField(max_length=100,default=None,null=True)
	Status 		= models.CharField(max_length=100,default=None,null=True)
	class Meta:
		db_table = 'userDetails'


class Product(models.Model):
	Product_Image = models.ImageField(upload_to="images/",null=True)
	Product_Name = models.CharField(max_length=100,default=None,null=True)
	Product_Price = models.CharField(max_length=100,default=None,null=True)
	class Meta:
		db_table = 'Product'

class cart(models.Model):
	uid 			= models.CharField(max_length=100,default=None)
	prod_id 		= models.CharField(max_length=100,default=None)
	Prod_name 		= models.CharField(max_length=100,default=None)
	Prod_price 		= models.CharField(max_length=100,default=None)
	Prod_quantity 	= models.IntegerField(max_length=100,default=None)
	Initial_price 	= models.CharField(max_length=100,default=None)

	class Meta:
		db_table = "cart"


class UserOrder(models.Model):
	uid 			= models.CharField(max_length=100,default=None)
	Total 			= models.CharField(max_length=100,default=None)
	Items 			= models.CharField(max_length=100,default=None)
	Status 			= models.CharField(max_length=100,default=None,null=True)
	User_Status 			= models.CharField(max_length=100,default=None,null=True)

	class Meta:
		db_table = "UserOrder"

class Comments(models.Model):
	pid  = models.CharField(max_length=100,default=None)
	uid 			= models.ForeignKey(userDetails, on_delete=models.CASCADE,null=True)
	comment 		= models.CharField(max_length=100,default=None)
	class Meta:
		db_table = "Comments"


class Queries(models.Model):
	User_id = models.CharField(max_length=100,default=None,null=True)
	Query = models.CharField(max_length=300,default=None,null=True)
	Answer = models.CharField(max_length=300,default=None,null=True)
	class Meta:
		db_table = "UserFeedback"