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
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'category', 'tags', 'created_at', 'updated_at', 'user']
        read_only_fields = ['user']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        note = Note.objects.create(**validated_data)
        if tags_data:
            note.tags.set(tags_data)
        return note

    def update(self, instance, validated_data):
        category = validated_data.get('category', instance.category)
        if category:
            instance.category = category

        tags_data = validated_data.get('tags', None)
        if tags_data is not None:
            instance.tags.set(tags_data)
        elif 'tags' in validated_data:
            instance.tags.clear()

        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()

        return instance
