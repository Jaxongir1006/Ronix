from rest_framework import serializers
from .models import Product,Category
from django.utils import translation
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

class ProductSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Product)
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        depth = 2
    
    def get_name(self, obj):
        lang = translation.get_language()
        return getattr(obj, f"name_{lang}", obj.name)

    def get_description(self, obj):
        lang = translation.get_language()
        return getattr(obj, f"description_{lang}", obj.description)
    
    def get_features(self, obj):
        lang = translation.get_language()
        return getattr(obj, f"features_{lang}", obj.features)
    
class CategorySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Category)
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    imageURL = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'imageURL', 'translations']

    def get_name(self, obj):
        return obj.safe_translation_getter('name', any_language=True)

    def get_description(self, obj):
        return obj.safe_translation_getter('description', any_language=True)
    

class ProductByCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'features', 'category']
        depth = 2
    