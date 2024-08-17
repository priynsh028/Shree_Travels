from django.contrib import admin
from django.urls import path, include
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name="home"),
    path('login/',views.loginUser,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('about/',views.about,name="about"),
    path('package/<int:id>/',views.package_detail,name="package_detail"),
    path('packages/',views.package,name="package"),
    path('Gallery/',views.Gallery,name="gallery"),
    path('signup/',views.signup,name="signup"),
    path('detail/',views.detail,name="detail"),
    path('book/',views.book,name="book"),
    path('payment/',views.payment,name="payment"),
    

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)