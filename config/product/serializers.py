from rest_framework import serializers
from product.models import Product, Store, Review
from rest_framework.reverse import reverse


def firstLetterCapital(value):  # validator
    if not str(value).isupper():
        raise serializers.ValidationError("First letter must be capitalized.")


class ReviewSerializer(serializers.ModelSerializer):
    apiuser = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    discountedPrice = serializers.SerializerMethodField()
    Reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def get_discountedPrice(self, obj):
        discounted_price = obj.price - 250
        return discounted_price

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
            raise serializers.ValidationError(
                "Name and description must be different."
            )
        return data


class StoreSerializer(serializers.ModelSerializer):
    stores = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="product-detail"  # Corrected view_name
    )

    class Meta:
        model = Store
        fields = "__all__"