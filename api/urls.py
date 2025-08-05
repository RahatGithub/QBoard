from django.urls import path
from .views import (
    EmployeeListCreateAPIView,
    EmployeeRetrieveUpdateDestroyAPIView,
    EmployeeBulkCreateAPIView,
    RegisterAPIView, 
    UserListAPIView, UserRetrieveUpdateDestroyAPIView,
    ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView,
    OrderListCreateAPIView, OrderRetrieveUpdateDestroyAPIView, 
    ProductBulkCreateAPIView, 
    DashboardSummaryAPIView, DashboardChartsAPIView,
    DashboardActivityAPIView,
    RandomDataGenerateAPIView,
)

urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    
    # Employees
    path('employees/', EmployeeListCreateAPIView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', EmployeeRetrieveUpdateDestroyAPIView.as_view(), name='employee-detail'),
    path('employees/bulk_create/', EmployeeBulkCreateAPIView.as_view(), name='employee-bulk-create'),

    # Users
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),

    # Products
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
    path('products/bulk_create/', ProductBulkCreateAPIView.as_view(), name='product-bulk-create'),

    # Orders
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyAPIView.as_view(), name='order-detail'),

    # Dashboard 
    path('dashboard/summary/', DashboardSummaryAPIView.as_view(), name='dashboard-summary'),
    path('dashboard/charts/', DashboardChartsAPIView.as_view(), name='dashboard-charts'),
    path('dashboard/activity/', DashboardActivityAPIView.as_view(), name='dashboard-activity'),

    # Random data generator
    path('generate/', RandomDataGenerateAPIView.as_view(), name='random-data-generate'),
]