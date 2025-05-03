from django.urls import path

from api.views.customer import CustomerViewSet, SingleCustomerViewSet
from api.views.order import OrderViewSet, SingleOrderViewSet
from api.views.product import ProductViewSet, SingleProductViewSet
from api.views.employee import EmployeeViewSet, ExternalEmployeeViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('employee', EmployeeViewSet.as_view()),
    path('employee/<email>', ExternalEmployeeViewSet.as_view()),
    path('product', ProductViewSet.as_view()),
    path('product/<int:pk>', SingleProductViewSet.as_view()),
    path('customer', CustomerViewSet.as_view()),
    path('customer/<int:pk>', SingleCustomerViewSet.as_view()),
    path('order', OrderViewSet.as_view()),
    path('order/<int:pk>', SingleOrderViewSet.as_view()),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
