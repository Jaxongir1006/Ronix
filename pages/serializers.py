from rest_framework import serializers
from .models import FAQ,NewsletterSubscriber,AboutUs
from parler_rest.serializers import TranslatableModelSerializer,TranslatedFieldsField

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email', 'name']

class AboutUsSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=AboutUs)
    class Meta:
        model = AboutUs
        fields = '__all__'