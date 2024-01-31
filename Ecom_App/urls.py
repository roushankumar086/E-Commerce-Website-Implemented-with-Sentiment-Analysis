from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views


urlpatterns = [
				path('',views.Home,name="Home"),
				path('Manage_Product/',views.Manage_Product,name="Manage_Product"),
				path('Admin_Login/',views.Admin_Login,name="Admin_Login"),
				path('User_Login/',views.User_Login,name="User_Login"),
				path('User_Registration/',views.User_Registration,name="User_Registration"),
				path('Add_Product/',views.Add_Product,name='Add_Product'),
				path('Delete_Product/<int:id>',views.Delete_Product,name='Delete_Product'),
				path('View_User/',views.View_User,name='View_User'),
				path('Update_Status/<int:id>',views.Update_Status,name='Update_Status'),
				path('ViewProduct/<int:id>',views.ViewProduct,name='ViewProduct'),
				path('deletecart/<int:id>',views.deletecart,name='deletecart'),
				path('Checkout/',views.Checkout,name='Checkout'),
				path('Answer/',views.Answer,name='Answer'),
				path('Cart/',views.Cart,name='Cart'),
				path('View_Query/',views.View_Query,name='View_Query'),
				path('Order/',views.Order,name='Order'),
				path('Ask_Queries/',views.Ask_Queries,name='Ask_Queries'),
				path('View_Order/',views.View_Order,name='View_Order'),
				path('Track_Order/',views.Track_Order,name='Track_Order'),
				path('Add_Comments/',views.Add_Comments,name='Add_Comments'),
				path('Update_Product/',views.Update_Product,name='Update_Product'),
				path('Show_Plot/<int:product_id>/', views.show_plot, name='show_plot'),
				path('Update_OrderStatus/<int:id>/', views.Update_OrderStatus, name='Update_OrderStatus'),
				path('Update_DeliverStatus/<int:id>/', views.Update_DeliverStatus, name='Update_DeliverStatus'),
				path('Logout/',views.Logout,name="Logout"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)