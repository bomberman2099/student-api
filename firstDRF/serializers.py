from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Article
from .models import Comment
from django.utils.timezone import now


class UserSerializer(serializers.ModelSerializer):
    articles = serializers.SlugRelatedField(read_only=True, many=True, slug_field='title')

    class Meta:
        model = User
        fields = '__all__'


def check_title(attrs):
    if 'fuck' in attrs['title']:
        raise serializers.ValidationError({'title': 'title can not be that word'})


class CheckTitle:
    def __call__(self, value):
        if 'html' in value['title']:
            raise serializers.ValidationError({'title': 'title can not be that word'})


# class ArticleSerializer(serializers.Serializer):
#     id = serializers.IntegerField(required=False)
#     title = serializers.CharField()
#     text = serializers.CharField()
#     status = serializers.BooleanField(required=False)
#
#     def create(self, validated_data):
#         return Article.objects.create(**validated_data)

class CommentSerializer(serializers.ModelSerializer):
    days_ago = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_days_ago(self, obj):
        return (now().date() - obj.date).days


class ArticleSerializer(serializers.ModelSerializer):
    # status = serializers.BooleanField(write_only=True)
    comment = serializers.SerializerMethodField()  # the list of the items that will serializing
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['id']
        validators = [
            check_title,
            CheckTitle()
        ]

    def get_comment(self, obj):
        serializer = CommentSerializer(instance=obj.comments.all(), many=True)
        return serializer.data

    # def validate_title(self, value):
    #     if 'fuck' in value:
    #         raise serializers.ValidationError('you cant use the fuck word')
    #     return value

    def validate(self, attrs):
        if attrs['title'] == attrs['text']:
            raise serializers.ValidationError('the title and text cant be same')
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return Article.objects.create(**validated_data)
