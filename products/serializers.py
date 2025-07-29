from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from .models import Product, Category, SubCategory

# Product uchun translation
class ProductTranslationSerializer(serializers.Serializer):
    name = serializers.CharField()
    made_in = serializers.CharField(allow_blank=True, required=False)

# Product for Cart
class ProductForCartSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Product, serializer_class=ProductTranslationSerializer)

    class Meta:
        model = Product
        fields = ['id', 'translations', 'image', 'model', 'price']

# SubCategory translation (optional)
class SubCategoryTranslationSerializer(serializers.Serializer):
    name = serializers.CharField()

# SubCategory
class SubCategorySerializer(TranslatableModelSerializer):
    translation = TranslatedFieldsField(shared_model=SubCategory, serializer_class=SubCategoryTranslationSerializer)

    class Meta:
        model = SubCategory
        fields = ['id', 'category', 'parent', 'image', 'translation']

# Category
class CategorySerializer(TranslatableModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'image']

# Category + Subcategories
class SubForCategorySerializer(TranslatableModelSerializer):
    translation = TranslatedFieldsField(shared_model=SubCategory, serializer_class=SubCategoryTranslationSerializer)

    class Meta:
        model = SubCategory
        fields = ['id', 'imageURL', 'name', 'translation']

class CategoryDetailsSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Category)
    subcategories = SubForCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'image', 'translations', 'subcategories']

# Product
class ProductSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Product)

    class Meta:
        model = Product
        fields = ['id', 'translations', 'barcode_color', 'barcode_carton', 'image', 'model', 'subcategory', 'price']
