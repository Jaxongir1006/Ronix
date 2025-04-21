from .models import Country,Content
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

class CountrySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Country)

    class Meta:
        model = Country
        fields = ['id', 'translations', 'flag', 'languages', 'continent']


class ContentSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Content)
    country = CountrySerializer()

    class Meta:
        model = Content
        fields = ['id', 'translations', 'country']