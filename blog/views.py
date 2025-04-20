from .serializer import BlogCategorySerializer,BlogSerializer,BlogImagesSerializer,BlogContentSerializer,BlogReviewSerializer,CommentSerializer
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import BlogCategory,Blog,BlogImages,BlogContent
from rest_framework.decorators import action

class BlogViewSet(ViewSet):
    @action(detail=False, methods=['get'])
    def categories(self, request):
        categories = BlogCategory.objects.all()
        
        category_data = BlogCategorySerializer(categories, many=True).data

        return Response({"categories": category_data}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def blogs(self, request):
        blogs = Blog.objects.all()
        
        blog_data = BlogSerializer(blogs, many=True).data

        return Response({"blogs": blog_data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def images(self, request):
        blog_images = BlogImages.objects.all()
        
        blog_image_data = BlogImagesSerializer(blog_images, many=True).data

        return Response({"blog_images": blog_image_data}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def content(self, request):
        blog_content = BlogContent.objects.all()
        
        blog_content_data = BlogContentSerializer(blog_content, many=True).data

        return Response({"blog_content": blog_content_data}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def review(self, request):
        serializer = BlogReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def comment(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)