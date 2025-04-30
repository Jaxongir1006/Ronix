from rest_framework import serializers
from .models import Product,Category,SubCategory,Specification,ProductDetail,ProductImages
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

class SpecificationSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Specification)

    class Meta:
        model = Specification
        fields = "__all__"

class ProductDetailSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=ProductDetail)

    class Meta:
        model = ProductDetail
        fields = "__all__"

class ProductImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImages
        fields = "__all__"

class ProductSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Product)
    specifications = SpecificationSerializer(read_only=True)
    details = ProductDetailSerializer(many=True,read_only=True)
    images = ProductImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class SubCategorySerializer(TranslatableModelSerializer):
    translation = TranslatedFieldsField(shared_model=SubCategory)

    class Meta:
        model = SubCategory
        fields = "__all__"
    
class CategorySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Category)
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'imageURL', 'translations', 'subcategories']

