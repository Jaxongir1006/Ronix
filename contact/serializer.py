from .models import ContactUs
from rest_framework import serializers

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'phone', 'message']

    def create(self, validated_data):
        contact_us = ContactUs.objects.create(**validated_data)
        return contact_us
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.message = validated_data.get('message', instance.message)
        instance.save()
        return instance
    def validate(self, data):
        if not data.get('name'):
            raise serializers.ValidationError("Name is required.")
        if not data.get('email'):
            raise serializers.ValidationError("Email is required.")
        if not data.get('phone'):
            raise serializers.ValidationError("Phone number is required.")
        if not data.get('message'):
            raise serializers.ValidationError("Message is required.")
        return data
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['created_at'] = instance.created_at.strftime('%d-%m-%Y')
        return rep