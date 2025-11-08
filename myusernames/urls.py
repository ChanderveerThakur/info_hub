from django.urls import path
from .views import signup_view, CustomLoginView, manual_logout

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', manual_logout, name='logout'),  # ✅ points to your manual view
]
