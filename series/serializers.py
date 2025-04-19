from rest_framework import serializers
from .models import Series,SeriesCategory


class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = '__all__'

class SeriesCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SeriesCategory
        fields = '__all__'

class SeriesCategoryDetailSerializer(serializers.ModelSerializer):
    series = SeriesSerializer(read_only=True)

    class Meta:
        model = SeriesCategory
        fields = '__all__'
