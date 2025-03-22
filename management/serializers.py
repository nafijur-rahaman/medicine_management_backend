from rest_framework import serializers
from .models import CustomUser, Customer, Category, Medicine, MedicineStock, Order
import random
import string


# Customer Serializer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'email', 'address']

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']

# Medicine Serializer
class MedicineSerializer(serializers.ModelSerializer):
    # Change the category to accept a string (category name)
    category = serializers.CharField(write_only=True)  # Receive category as string
    category_name = serializers.CharField(source='category.category_name', read_only=True)

    class Meta:
        model = Medicine
        fields = ['id', 'name', 'brand_name', 'category', 'category_name', 'unit_price', 'pack_size', 'total_pack', 'status']

    def create(self, validated_data):
        category_name = validated_data.pop('category')
        category, created = Category.objects.get_or_create(category_name=category_name)
        medicine = Medicine.objects.create(category=category, **validated_data)
        return medicine

    def update(self, instance, validated_data):
        category_name = validated_data.pop('category', None)

        if category_name:
         
            category = Category.objects.filter(category_name=category_name).first()

            if not category:
                category = Category.objects.create(category_name=category_name)

            instance.category = category

  
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

  
        instance.save()

        return instance


# Medicine Stock Serializer
class MedicineStockSerializer(serializers.ModelSerializer):

    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    

    medicine = serializers.CharField(write_only=True)

    class Meta:
        model = MedicineStock
        fields = ['id', 'medicine', 'medicine_name', 'total_pack', 'purchase_price', 'date']

    def create(self, validated_data):

        medicine_name = validated_data.get('medicine')
        try:
            medicine = Medicine.objects.get(name=medicine_name)
        except Medicine.DoesNotExist:
            raise serializers.ValidationError(f"Medicine with name {medicine_name} does not exist.")
    
        # Check if a stock entry for this medicine already exists
        existing_stock = MedicineStock.objects.filter(medicine=medicine).first()
    
        if existing_stock:
            raise serializers.ValidationError(f"Stock for medicine '{medicine_name}' already exists.")
    
        validated_data['medicine'] = medicine
        return super().create(validated_data)


    def update(self, instance, validated_data):

        medicine_name = validated_data.get('medicine')
        

        try:
            medicine = Medicine.objects.get(name=medicine_name)
        except Medicine.DoesNotExist:
            raise serializers.ValidationError(f"Medicine with name {medicine_name} does not exist.")
        
  
        validated_data['medicine'] = medicine
        return super().update(instance, validated_data)


# Order Serializer



class OrderSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(source='customer.name', read_only=True)
    customer_phone = serializers.CharField(source='customer.phone', read_only=True)
    customer_email = serializers.EmailField(source='customer.email', read_only=True)
    customer_address = serializers.CharField(source='customer.address', read_only=True)


    medicine_name = serializers.CharField(source='medicine.name', read_only=True)


    ordered_by_username = serializers.CharField(source='ordered_by.username', read_only=True)

  
    customer = serializers.CharField(write_only=True)
    medicine = serializers.CharField(write_only=True)
    ordered_by = serializers.CharField(write_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_no', 'customer', 'customer_name', 'customer_phone', 'customer_email', 
            'customer_address', 'medicine', 'medicine_name', 'total_pack', 'order_amount', 
            'order_date', 'ordered_by', 'ordered_by_username'
        ]
        read_only_fields = ['order_no', 'customer_name', 'customer_phone', 'customer_email', 'customer_address']

    def create(self, validated_data):
        customer_name = validated_data.pop('customer')
        medicine_name = validated_data.pop('medicine')
        ordered_by_username = validated_data.pop('ordered_by')

        customer = Customer.objects.get(name=customer_name)
        medicine = Medicine.objects.get(name=medicine_name)
        ordered_by = CustomUser.objects.get(username=ordered_by_username)

        order_id = self.generate_order_id()

        validated_data['customer'] = customer
        validated_data['medicine'] = medicine
        validated_data['ordered_by'] = ordered_by
        validated_data['order_no'] = order_id

        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'customer' in validated_data:
            customer_name = validated_data.pop('customer')
            instance.customer = Customer.objects.get(name=customer_name)

        if 'medicine' in validated_data:
            medicine_name = validated_data.pop('medicine')
            instance.medicine = Medicine.objects.get(name=medicine_name)

        if 'ordered_by' in validated_data:
            ordered_by_username = validated_data.pop('ordered_by')
            instance.ordered_by = CustomUser.objects.get(username=ordered_by_username)


        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def generate_order_id(self):
     
        random_number = random.randint(100, 999)  # Generate a random number between 100 and 999
        order_id = f"ORD{random_number}"
        return order_id



