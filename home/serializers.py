from .models import HomeBanner, CustomerReview
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

class HomeBannerSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=HomeBanner)

    class Meta:
        model = HomeBanner
        fields = ['id', 'title', 'subtitle', 'imageURL', 'translations']


class customerReviewSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=CustomerReview)

    class Meta:
        model = CustomerReview
        fields = ['id', 'title', 'description', 'videoURL', 'translations']