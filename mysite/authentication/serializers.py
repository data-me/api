from rest_framework import serializers
from datame.models import Company


class CompanySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=False, max_length=100)
    description = serializers.CharField()
    nif = serializers.CharField()
    logo = serializers.CharField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('name', instance.name)
        instance.code = validated_data.get('description', instance.description)
        instance.linenos = validated_data.get('nif', instance.nif)
        instance.language = validated_data.get('logo', instance.logo)
        instance.style = validated_data.get('id', instance.id)
        instance.save()
        return instance