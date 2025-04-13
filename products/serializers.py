from rest_framework import serializers
from .models import Product,Category
from django.utils import translation


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_name(self, obj):
        lang = translation.get_language()
        return getattr(obj, f"name_{lang}", obj.name)

    def get_description(self, obj):
        lang = translation.get_language()
        return getattr(obj, f"description_{lang}", obj.description)
    
    def get_features(self, obj):
        lang = translation.get_language()
        return getattr(obj, f"features_{lang}", obj.features)
    
class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_name(self, obj):
        lang = translation.get_language()
        return getattr(obj, f'name_{lang}', obj.name)
    
    def get_description(self, obj):
        lang = translation.get_language()
        return getattr(obj, f"description_{lang}", obj.description)
    