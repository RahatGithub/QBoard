from rest_framework import serializers
from .models import User, Employee, Product, Order, OrderItem
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'date_joined']



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data.get('role', 'user')
        )
        return user



class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']




class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'order_date', 'total_amount', 'items']
        read_only_fields = ['total_amount', 'order_date']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        # Check stock for all items before creating any
        for item_data in items_data:
            product = Product.objects.get(pk=item_data['product'].id if isinstance(item_data['product'], Product) else item_data['product'])
            if product.stock < item_data['quantity']:
                raise ValidationError(f"Not enough stock for product '{product.name}'. Available: {product.stock}, Requested: {item_data['quantity']}")
        # If all stock is sufficient, create items and update stock
        for item_data in items_data:
            product = Product.objects.get(pk=item_data['product'].id if isinstance(item_data['product'], Product) else item_data['product'])
            OrderItem.objects.create(order=order, **item_data)
            if order.status == 'pending':
                product.stock -= item_data['quantity']
                product.save()
        order.save()
        return order

    def update(self, instance, validated_data):
        # Prevent update if order is completed or cancelled
        if instance.status in ['completed', 'cancelled']:
            raise ValidationError(f"Order is already {instance.status} and cannot be updated.")

        items_data = validated_data.pop('items', None)
        old_status = instance.status
        new_status = validated_data.get('status', instance.status)

        # If status is being changed to 'cancelled', restock products
        if old_status != 'cancelled' and new_status == 'cancelled':
            for item in instance.items.all():
                product = item.product
                product.stock += item.quantity
                product.save()
        # If status is being changed from 'cancelled' to 'pending', reduce stock again
        elif old_status == 'cancelled' and new_status == 'pending':
            for item in instance.items.all():
                product = item.product
                if product.stock < item.quantity:
                    raise ValidationError(f"Not enough stock for product '{product.name}' to re-activate order.")
                product.stock -= item.quantity
                product.save()

        # Update order fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # If items are being updated, handle stock accordingly
        if items_data is not None:
            # First, restock all old items if status is pending
            if instance.status == 'pending':
                for item in instance.items.all():
                    product = item.product
                    product.stock += item.quantity
                    product.save()
            # Delete old items
            instance.items.all().delete()
            # Create new items and reduce stock
            for item_data in items_data:
                product = Product.objects.get(pk=item_data['product'].id if isinstance(item_data['product'], Product) else item_data['product'])
                if instance.status == 'pending':
                    if product.stock < item_data['quantity']:
                        raise ValidationError(f"Not enough stock for product '{product.name}'. Available: {product.stock}, Requested: {item_data['quantity']}")
                    product.stock -= item_data['quantity']
                    product.save()
                OrderItem.objects.create(order=instance, **item_data)
            instance.save()
        return instance