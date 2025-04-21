from rest_framework import serializers
from .models import Series,SeriesCategory,SeriesCategoryDetail
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField


class SeriesSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Series)
    class Meta:
        model = Series
        fields = '__all__'

class SeriesCategorySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=SeriesCategory)
    class Meta:
        model = SeriesCategory
        fields = '__all__'

class SeriesCategoryDetailSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=SeriesCategory)
    series = SeriesSerializer(read_only=True)

    class Meta:
        model = SeriesCategoryDetail
        fields = '__all__'
