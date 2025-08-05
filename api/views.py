from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import User, Employee, Product, Order, OrderItem
from .serializers import (
    EmployeeSerializer, RegisterSerializer, UserSerializer, 
    ProductSerializer, OrderSerializer
)
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from faker import Faker
import random


# User registration
class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []  

# Employees:
# single insert
class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['department', 'position']  
    search_fields = ['name', 'position', 'department']  
    ordering_fields = ['salary', 'hire_date', 'performance_score', 'department']  

class EmployeeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

# Bulk insert
class EmployeeBulkCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Check if the request.data is a list (for bulk create)
        if isinstance(request.data, list):
            serializer = EmployeeSerializer(data=request.data, many=True)
        else:
            serializer = EmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Users
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['role', 'is_active']  
    search_fields = ['username', 'email']     
    ordering_fields = ['date_joined', 'username', 'role']

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]



# Products: 
# Single insert
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['category']
    search_fields = ['name', 'category']
    ordering_fields = ['price', 'stock']

# Bulk insert
class ProductBulkCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Check if the request.data is a list (for bulk create)
        if isinstance(request.data, list):
            serializer = ProductSerializer(data=request.data, many=True)
        else:
            serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Read, Update, Delete
class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


# Orders
class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'user']
    search_fields = []
    ordering_fields = ['order_date', 'total_amount'] 

class OrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


# Dashboard
class DashboardSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_users = User.objects.count()
        total_employees = Employee.objects.count()
        total_products = Product.objects.count()
        total_orders = Order.objects.count()
        pending_orders= Order.objects.filter(status='pending').count() #added later
        completed_orders= Order.objects.filter(status='completed').count() #added later
        cancelled_orders= Order.objects.filter(status='cancelled').count() #added later
        total_revenue = Order.objects.filter(status='completed').aggregate(
            revenue=Sum('total_amount')
        )['revenue'] or 0
        due_revenue = Order.objects.filter(status='pending').aggregate(
            revenue=Sum('total_amount')
        )['revenue'] or 0

        return Response({
            "total_users": total_users,
            "total_employees": total_employees,
            "total_products": total_products,
            "total_orders": total_orders,
            "pending_orders":pending_orders, #added later
            "completed_orders":completed_orders, #added later
            "cancelled_orders":cancelled_orders, #added later
            "total_revenue": total_revenue,
            "due_revenue": due_revenue, # added later
        })



class DashboardChartsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Orders per month (last 6 months)
        six_months_ago = timezone.now() - timedelta(days=180)
        orders_per_month = (
            Order.objects.filter(order_date__gte=six_months_ago)
            .annotate(month=TruncMonth('order_date'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )

        # Top 5 products by order count
        top_products = (
            Order.objects.values('product__name', 'product__category', 'product__price')
            .annotate(order_count=Count('id'))
            .order_by('-order_count')[:5]
        )

        return Response({
            "orders_per_month": orders_per_month,
            "top_products": top_products,
        })


class DashboardActivityAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recent_orders = Order.objects.order_by('-order_date')[:5]
        recent_users = User.objects.order_by('-date_joined')[:5]
        recent_employees = Employee.objects.order_by('-hire_date')[:5]
        return Response({
            "recent_orders": OrderSerializer(recent_orders, many=True).data,
            "recent_users": UserSerializer(recent_users, many=True).data,
            "recent_employees": EmployeeSerializer(recent_employees, many=True).data,
        })



class RandomDataGenerateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        fake = Faker()
        data_type = request.data.get('type')
        amount = int(request.data.get('amount', 10))
        created = 0

        if data_type == 'users':
            for _ in range(amount):
                User.objects.create_user(
                    username=fake.unique.user_name(),
                    email=fake.unique.email(),
                    password='password123',
                    role=random.choice(['user', 'manager', 'admin'])
                )
                created += 1

        elif data_type == 'employees':
            for _ in range(amount):
                Employee.objects.create(
                    name=fake.name(),
                    position=fake.job(),
                    department=fake.random_element(elements=('Sales', 'HR', 'IT', 'Finance')),
                    salary=round(random.uniform(30000, 120000), 2),
                    hire_date=fake.date_between(start_date='-5y', end_date='today'),
                    performance_score=random.randint(1, 10)
                )
                created += 1

        elif data_type == 'products':
            for _ in range(amount):
                Product.objects.create(
                    name=fake.unique.word().capitalize(),
                    category=fake.random_element(elements=('Electronics', 'Books', 'Clothing', 'Furniture')),
                    price=round(random.uniform(5, 500), 2),
                    stock=random.randint(0, 400)
                )
                created += 1

        elif data_type == 'orders':
            users = list(User.objects.all())
            products = list(Product.objects.all())
            if not users or not products:
                return Response({"error": "Need users and products to create orders."}, status=status.HTTP_400_BAD_REQUEST)
            for _ in range(amount):
                user = random.choice(users)
                order_date = fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone())
                order_status = random.choice(['pending', 'completed', 'cancelled'])
                num_items = random.randint(1, 3)
                chosen_products = random.sample(products, min(num_items, len(products)))
                items = []
                for product in chosen_products:
                    quantity = random.randint(1, 5)
                    items.append({
                        "product": product.id,
                        "quantity": quantity
                    })
                order_data = {
                    "user": user.id,
                    "status": order_status,
                    "order_date": order_date,
                    "items": items
                }
                serializer = OrderSerializer(data=order_data)
                if serializer.is_valid():
                    serializer.save()
                    created += 1
                else:
                    # Skip this order and continue
                    continue

        else:
            return Response({"error": "Invalid type. Use one of: users, employees, products, orders."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "message": f"Successfully created {created} {data_type}.",
                "type": data_type,
                "count": created
            },
            status=status.HTTP_201_CREATED
        )