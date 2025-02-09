from rest_framework import serializers
from product.models import Product


def firstLetterCapital(value): #validator
    if not str(value).isupper():
        raise serializers.ValidationError("First letter must be capitalized.")


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200, validators=[firstLetterCapital])
    description = serializers.CharField(max_length=1000)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    active = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)
        instance.quantity = validated_data.get("quantity", instance.quantity)
        instance.active = validated_data.get("active", instance.active)
        instance.save()
        return instance

    def validate_price(self, value):  # field level validation
        if value < 0:
            raise serializers.ValidationError("Price must be positive.")
        return value

    def validate(self, data):  # object level validation
        if data["name"] == data["description"]:
            raise serializers.ValidationError("Name and description must be different.")
        return data
