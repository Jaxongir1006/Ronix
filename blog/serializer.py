from rest_framework import serializers
from .models import BlogCategory,Blog,BlogImages,BlogContent,BlogReview,Comment

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['title', 'imageURL']

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

class BlogImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImages
        fields = '__all__'

class BlogContentSerializer(serializers.ModelSerializer):
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