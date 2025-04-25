from rest_framework import serializers
from .models import HomeBanner
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

class HomeBannerSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=HomeBanner)

    class Meta:
        model = HomeBanner
        fields = ['id', 'title', 'subtitle', 'imageURL', 'translations']


