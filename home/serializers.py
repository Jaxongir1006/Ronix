from rest_framework import serializers
from .models import HomeBanner, CustomerReview
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

class HomeBannerSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=HomeBanner)
    title = serializers.CharField(source='title')
    subtitle = serializers.CharField(source='subtitle')
    imageURL = serializers.ReadOnlyField()

    class Meta:
        model = HomeBanner
        fields = ['id', 'title', 'subtitle', 'imageURL', 'translations']


