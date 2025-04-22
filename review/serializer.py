from rest_framework import serializers
from .models import Review,Rate,CustomerReview
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user', 'comment']

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = '__all__'

class CustomerReviewSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=CustomerReview)
    title = serializers.CharField(source='title')
    description = serializers.CharField(source='description')
    videoURL = serializers.ReadOnlyField()

    class Meta:
        model = CustomerReview
        fields = ['id', 'title', 'description', 'videoURL', 'translations']
