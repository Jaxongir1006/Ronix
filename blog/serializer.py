from rest_framework import serializers
from .models import BlogCategory,Blog,BlogImages,BlogContent,BlogReview,Comment
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

class BlogCategorySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=BlogCategory)

    class Meta:
        model = BlogCategory
        fields = ['title', 'imageURL', 'translations']

class BlogSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Blog)

    class Meta:
        model = Blog
        fields = '__all__'

class BlogImagesSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=BlogImages)

    class Meta:
        model = BlogImages
        fields = '__all__'

class BlogContentSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=BlogContent)

    class Meta:
        model = BlogContent
        fields = ['title', 'description']

class BlogReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogReview
        fields = ['rate']
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['name','text']