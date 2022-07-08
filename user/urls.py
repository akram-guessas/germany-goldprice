from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from django.conf import settings
from .views import ItemCreateView, ItemUpdateView, ItemDeleteView,CustomerSignUpView,VendorSignUpView

# from .views import SingUp,CustomerSignUpView,VendorSignUpView

urlpatterns = [
    path(r'^list$', views.index, name='home'),
    path('new_item/', ItemCreateView.as_view(), name='new_item'),
    path('new_item/detail/<str:item_name>/<int:item_id>',views.Item_detail,name='detail'),
    path('new_item/detail/<slug:pk>/update/', ItemUpdateView.as_view(), name='item-update'),
    path('new_item/detail/<slug:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),

    # path('أضافة منتج جديد/', views.ItemCreateView, name='new_item'),
    path('register/', views.register, name='register'),
    # path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('login/', views.login_user, name='login'),
    # path('logout/', LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile_update/', views.profile_update, name='profile_update'),
    
    path('singup/',views.SingUp,name='singup'),
    path('signup/customer/', CustomerSignUpView.as_view(), name='customer_signup'),
    path('signup/vendor/', VendorSignUpView.as_view(), name='vendor_signup'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
