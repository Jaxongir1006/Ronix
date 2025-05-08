from rest_framework import serializers
from .models import Product,Category,SubCategory,Specification,ProductDetail,ProductImages
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

class SpecificationSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Specification)

    class Meta:
        model = Specification
        fields = ['product', 'translations']

class ProductDetailSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=ProductDetail)

    class Meta:
        model = ProductDetail
        fields = ['main_image','product','translations']

class ProductImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImages
        fields = ['product','image','video']

class ProductSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Product)
    specifications = SpecificationSerializer(read_only=True)
    details = ProductDetailSerializer(many=True,read_only=True)
    images = ProductImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id','translations','barcode_color','barcode_carton','image','model','subcategory','price','specifications','images','details']

class SubCategorySerializer(TranslatableModelSerializer):
    translation = TranslatedFieldsField(shared_model=SubCategory)

    class Meta:
        model = SubCategory
        fields = ['category','translation','parent','image','id']

class CategoryTranslationSerialzer(serializers.Serializer):
    name = serializers.CharField()    

class CategorySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Category, serializer_class=CategoryTranslationSerialzer)

    class Meta:
        model = Category
        fields = ['id', 'imageURL','translations',]

class SubCategoryTranslationSerialzer(serializers.Serializer):
    name = serializers.CharField()    

class SubForCategorySerializer(TranslatableModelSerializer):
    translation = TranslatedFieldsField(shared_model=SubCategory, serializer_class=SubCategoryTranslationSerialzer)

    class Meta:
        model = SubCategory
        fields = ['id', 'imageURL', 'name', 'translation']

class CategoryDetailsSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Category)
    subcategories = SubForCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'image', 'translations','subcategories']

class ProductTranslationSerializer(serializers.Serializer):
    name = serializers.CharField()
    made_in = serializers.CharField(allow_blank=True, required=False)

class ProductForCartSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Product, serializer_class=ProductTranslationSerializer)

    class Meta:
        model = Product
        fields = ['id', 'translations', 'image', 'model', 'price']