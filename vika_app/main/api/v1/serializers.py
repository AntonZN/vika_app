from datetime import datetime
from rest_framework import serializers

from vika_app.account.models import User
from vika_app.main.models import Comment, ElementType, Performance, Video, VideoElement


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "phone", "age", "gender"]
        read_only_fields = ["phone"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "c_d1d2",
            "c_d3d4",
            "c_e1e2",
            "c_e3e6",
        ]


class VideoElementSerializer(serializers.ModelSerializer):
    comments = CommentSerilazers()
    video = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Video.objects.all()
    )

    type = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=ElementType.objects.all()
    )

    class Meta:
        model = VideoElement
        fields = [
            "video",
            "type",
            "start_time",
            "end_time",
            "d1d2",
            "d3d4",
            "e1e2",
            "e3e6",
            "pointer",
            "comments",
        ]

    def create(self, validated_data):
        comments_data = validated_data.pop("comments")
        element = VideoElement.objects.create(**validated_data)
        Comment.objects.create(element=element, **comments_data)
        video = Video.objects.get(id=validated_data.get("video").id)
        video.is_rated = True
        video.save()

        return element


class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name"]


class VideoListSerializer(serializers.ModelSerializer):
    trainer = TrainerSerializer()

    class Meta:
        model = Video
        fields = [
            "id",
            "user_id",
            "trainer",
            "preview",
            "video_file",
            "video_duration",
            "date",
            "rate",
            "is_rated",
        ]


class ElementTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElementType
        fields = [
            "id",
            "name",
            "svg",
        ]


class VideoElementAppSerializer(serializers.ModelSerializer):
    comments = CommentSerilazer()
    type = ElementTypeSerializer()
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    class Meta:
        model = VideoElement
        fields = [
            "type",
            "start_time",
            "end_time",
            "d1d2",
            "d3d4",
            "e1e2",
            "e3e6",
            "pointer",
            "comments",
        ]

    def get_type(self, obj):
        return obj.type.name

    def get_start_time(self, obj):
        time_start = obj.start_time
        time = datetime.strptime(time_start, "%M:%S")
        a_timedelta = time - datetime(1900, 1, 1)
        seconds = a_timedelta.total_seconds()
        return seconds

    def get_end_time(self, obj):
        time_start = obj.end_time
        time = datetime.strptime(time_start, "%M:%S")
        a_timedelta = time - datetime(1900, 1, 1)
        seconds = a_timedelta.total_seconds()
        return seconds


class VideoSerializer(serializers.ModelSerializer):
    trainer = TrainerSerializer()
    elements = VideoElementAppSerializers(read_only=True, many=True)
    video_file = serializers.SerializerMethodField()
    preview = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            "id",
            "user_id",
            "trainer",
            "preview",
            "video_file",
            "video_duration",
            "date",
            "rate",
            "is_rated",
            "elements",
        ]

    def get_video_file(self, obj):
        return obj.video_file.url

    def get_preview(self, obj):
        return obj.preview.url


class ModelListField(serializers.ListField):
    def to_representation(self, data):
        return [
            self.child.to_representation(item) if item is not None else None
            for item in data
        ]


class VideoCreateSerializer(serializers.ModelSerializer):

    video_file = serializers.FileField(read_only=False, required=True)
    resolution = serializers.CharField(read_only=False, required=True)

    class Meta:
        model = Video
        fields = ["id", "video_file", "resolution"]


class PerformanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ["id", "name"]


class DeviceSerializer(serializers.Serializer):
    registration_id = serializers.CharField(required=True)


class SendNotificationSerializer(serializers.Serializer):
    video_id = serializers.CharField(required=True)
