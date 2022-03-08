from unicodedata import name
from .views import LogoutView, RegistrationView,VerificationView,UsernameValidationView,LoginView,EmailValidationView, profile_edit
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
  path('register',RegistrationView.as_view(),name="register"),
  path('login',LoginView.as_view(),name="login"),
  path('logout',LogoutView.as_view(),name="logout"),
  path('validate-username',csrf_exempt(UsernameValidationView.as_view()),name="validate-username"),
  path('validate-email',csrf_exempt(EmailValidationView.as_view()),name="validate-email"),
  path('activate/<uidb64>/<token>',VerificationView.as_view(),name="activate"),
  path('edit-profile/<int:id>' ,views.profile_edit, name = "profile-edit"),
  path('profile',views.profile_view,name="profile")
]
