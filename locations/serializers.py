from rest_framework import serializers
from .models import Branch
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField


class BranchSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Branch)
    name = serializers.CharField(source='translations.name', read_only=True)

    class Meta:
        model = Branch
        fields = ['id', 'name', 'image', 'address', 'phone', 'translations']
