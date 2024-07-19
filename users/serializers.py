from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Comment, CommentReply, Like, ConfirmedDonation, Donation


class DonationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Donation
        fields = ['id', 'user', 'amount', 'date', 'confirmation_file', 'comment', 'is_verified']
        read_only_fields = ['user', 'is_verified']

class ConfirmedDonationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    amount = serializers.ReadOnlyField(source='donation.amount')

    class Meta:
        model = ConfirmedDonation
        fields = ['id', 'user', 'amount', 'date', 'comment']


class UserProfileSerializers(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserProfile
        exclude = ['id']


class CommentSerializers(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at']


class CommentReplySerializers(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = CommentReply
        fields = ['id', 'author', 'text', 'created_at']


class LikeSerializers(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = ['id', 'user']
