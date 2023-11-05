from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetCompleteView, \
    PasswordResetConfirmView, PasswordResetDoneView
from django.urls import path
from . import views
from .views import CustomLoginView, RegisterView, showDetails, lunchDelete, breakfastDelete, dinnerDelete

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('favourite_foods/',views.favourite_foods,name='favourite_foods'),
    path('account_details/', views.showDetails, name='showDetails'),
    path('password_change/', views.password_change, name='password_change'),
    path('password-reset/', PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm_email.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('lunchDelete/<str:pk>/',
         lunchDelete.as_view(),name='lunchDelete'),
    path('breakfastDelete/<str:pk>/',
         breakfastDelete.as_view(), name='breakfastDelete'),
    path('dinnerDelete/<str:pk>/',
         dinnerDelete.as_view(), name='dinnerDelete'),
    path('showBmi/',views.showBmi, name='showBmi'),
]

