from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from api import models
from api import helpers

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = '__all__'
        ordering = ['created']

class FeedItemCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FeedItemComment
        fields = '__all__'
        ordering = ['created']

    def create(self, validated_data):
        data = validated_data.copy()
        data['feed_item_id'] = helpers.feedItem_forURLPath(self.context.get('request').get_full_path()).id #TODO: is there a better way to accomplish this
        comment = models.FeedItemComment.objects.create(**data)
        return comment
        
class FeedItemSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True, read_only=True)
    comments = FeedItemCommentSerializer(many=True, read_only=True)

    class Meta:
        model = models.FeedItem
        fields = '__all__'
        ordering = ['created']

    @transaction.atomic
    def create(self, validated_data):
        feed_item = models.FeedItem.objects.create(**validated_data)

        for id in self.context.get('request').data.get('exiting_image_ids', []):

            try:
                image = models.Image.objects.get(id=id)
                if image.feed_item_id is not None:
                    raise ValidationError()
                image.feed_item_id = feed_item.id
                image.save()
            except Exception as e:
                raise ValidationError('Invalid id in exiting_image_ids')

        return feed_item