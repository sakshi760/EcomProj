from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm
from django.contrib.auth.views import LogoutView
from .views import home
from .views import orders
#from .views import PaymentFormView
  # Import the view

urlpatterns = [
    path('', views.home),
    path('about/', views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('category/<slug:val>', views.CategoryView.as_view(), name="category"),
    path('category-title/<val>', views.CategoryTitle.as_view(), name="category-title"),  # Corrected here
    path('product-detail/<int:pk>', views.ProductDetail.as_view(), name="product-detail"),
    path('profile/',views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('updateAddress/<int:pk>', views.updateAddress.as_view(),name='updateAddress'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Make sure checkout is defined
    path('process_payment/', views.process_payment, name='process_payment'), 
    path('', home, name='home'),
    path('orders/', orders, name='orders'),
    
    #path('payment/', PaymentFormView.as_view(), name='payment'),
    
    #path('search/',views.search,name='search'),


    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'),
    path('checkout/', views.Checkout.as_view(), name='Checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path('pluscart/', views.plus_cart),

    #login authentication
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm) , name='login'),
    path('password-reset/', auth_view.PasswordResetView.as_view
    (template_name='app/password_reset.html', form_class=MyPasswordResetForm) ,
    name='password_reset'),
    path(
    'passwordchange/',
    auth_view.PasswordChangeView.as_view(
        template_name='app/changepassword.html',
        form_class=MyPasswordChangeForm,
        success_url='/passwordchangedone'
    ),
    name='passwordChange'
),
path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),

path('logout/', LogoutView.as_view(), name='logout'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)