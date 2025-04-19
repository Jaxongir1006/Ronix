from rest_framework import serializers
from .models import HomeBanner, CustomerReview
from products.models import Product

class HomeBannerSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='title')
    subtitle = serializers.CharField(source='subtitle')
    imageURL = serializers.ReadOnlyField()

    class Meta:
        model = HomeBanner
        fields = ['id', 'title', 'subtitle', 'imageURL']

class CustomerReviewSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='title')
    description = serializers.CharField(source='description')
    videoURL = serializers.ReadOnlyField()

    class Meta:
        model = CustomerReview
        fields = ['id', 'title', 'description', 'videoURL']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'model', 'image']