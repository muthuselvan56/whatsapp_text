from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signin/',views.signin, name='signin'),
    path('signout/',views.signout, name='signout'),
    path('signup/',views.signup, name='signup'),
    path('profile/',views.profile.as_view(), name='profile'),
    path('viewlist/',views.import_excel, name='excel'),
    path('catpillar',views.Export_excel,name='catpillar'),
    path('adddetails',views.add_user ,name='adddetails'),
    path('centerpillar',views.add_user_method ,name='centerpillar'),
    path('edit/', views.edit, name='edit'),
    path('editadd/',views.edit_store,name='catwaser'),
    path('delete/', views.delete, name='delete'),
    path('whatsapp/', views.upload_excel, name='upload_excel'), 
    path('txt_collapse/', views.message_send , name='txt_collapse'),
    path('img_collapse/', views.image_send , name='img_collapse'),
    path('uploaded/',views.sendmsg_to_excel,name='carpillar'),
    path('sendwhats/',views.senddata,name='sendwhats'),
    # path('delete_all/',views.delete_all,name='delete_all'),
]