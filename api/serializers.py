from django.db import transaction
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from api import models
from api import helpers

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        exclude = ['feed_item', 'user']
        ordering = ['created']

    def create(self, validated_data):

        # Add user to validated_data
        data = validated_data.copy()
        data['user'] = self.context['request'].user

        return super(ImageSerializer, self).create(data)

class FeedItemCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FeedItemComment
        exclude = ['feed_item']
        ordering = ['created']

    def create(self, validated_data):
        data = validated_data.copy()
        data['feed_item_id'] = helpers.feedItem_forURLPath(self.context.get('request').get_full_path()).id
        comment = models.FeedItemComment.objects.create(**data)
        return comment
        
class FeedItemSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True, read_only=True)
    comments = FeedItemCommentSerializer(many=True, read_only=True)

    class Meta:
        model = models.FeedItem
        exclude = ['user']
        ordering = ['created']

    def _add_existing_images_ids(self, feed_item: models.FeedItem, existing_image_ids: [str]):

        for id in existing_image_ids:
            try:
                image = models.Image.objects.get(id=id, user_id=self.context['request'].user.id)
                if image.feed_item_id is not None:
                    if image.feed_item_id == feed_item.id:
                        print("Image already added to feed item")
                        continue
                    else:
                        raise ValidationError()

                image.feed_item_id = feed_item.id
                image.save()
            except Exception as e:
                print(e)
                raise ValidationError('Invalid id in existing_image_ids')

    @transaction.atomic
    def create(self, validated_data):

        # Add user to validated_data
        data = validated_data.copy()
        data['user'] = self.context['request'].user

        # Create FeedItem
        feed_item = super(FeedItemSerializer, self).create(data)

        # dd FeedItem to images
        exiting_image_ids = self.context.get('request').data.get('existing_image_ids', [])
        self._add_existing_images_ids(feed_item, exiting_image_ids)

        return feed_item

    @transaction.atomic
    def update(self, instance, validated_data):

        # Add FeedItem to images
        exiting_image_ids = self.context.get('request').data.get('existing_image_ids', [])
        self._add_existing_images_ids(instance, exiting_image_ids)

        return super(FeedItemSerializer, self).update(instance, validated_data)