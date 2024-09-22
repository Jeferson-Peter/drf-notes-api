# notes/serializers.py

from rest_framework import serializers
from .models import Category, Tag, Note


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class NoteSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'category', 'tags', 'created_at', 'updated_at', 'user', 'is_favorite', 'slug']
        read_only_fields = ['user']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['category'] = instance.category.name
        ret['tags'] = TagSerializer(instance.tags.all(), many=True).data
        return ret

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        note = Note.objects.create(**validated_data)
        note.tags.set(tags_data)
        return note

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        if tags_data is not None:
            instance.tags.set(tags_data)

        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.category = validated_data.get('category', instance.category)
        instance.is_favorite = validated_data.get('is_favorite', instance.is_favorite)
        instance.save()
        return instance