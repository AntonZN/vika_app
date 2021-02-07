import json
from fcm_django.models import FCMDevice
from rest_framework import exceptions, generics, status, viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema, ManualSchema
from rest_framework.views import APIView

from vika_app.account.authentication import FirebaseAuthentication
from vika_app.main.models import *
from . import serializers


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class Profile(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]
    serializer_class = serializers.UserSerializer

    def get(self, request, format="json"):
        """
        Получить данные пользователя.
        gender "0" - Мужской, "1" - Женский
        """
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format="json"):
        """
        Изменить данные пользователя
        gender "0" - Мужской, "1" - Женский
        """
        user = request.user
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RateVideoElement(generics.CreateAPIView):

    """
    Метод для оценки видео тренером. Используется из административной части сайта. 
    """

    permission_classes = [IsAdminUser]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = serializers.VideoElementSerializer

    def post(self, request, format="json"):
        data = json.loads(request.body.decode())
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            video = Video.objects.get(id=data["video"])
            video.trainer_id = data["trainer"]
            video.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PerformanceList(generics.ListAPIView):

    """
    Список типов выступления
    """

    serializer_class = serializers.PerformanceListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]
    queryset = Performance.objects.all()


class ElementsList(generics.ListAPIView):

    """
    Список видов элементов
    """

    serializer_class = serializers.ElementTypeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]
    queryset = ElementType.objects.all()


class VideoList(generics.ListAPIView):
    serializer_class = serializers.VideoListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]

    def get_queryset(self):
        return Video.objects.filter(user=self.request.user)

    def get(self, request, format="json"):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VideoView(generics.RetrieveAPIView):
    serializer_class = serializers.VideoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]

    def get_queryset(self, video_id):
        try:
            return Video.objects.get(id=video_id, user=self.request.user)
        except Video.DoesNotExist:
            raise exceptions.NotFound()

    def get(self, request, video_id, format="json"):
        serializer = self.serializer_class(self.get_queryset(video_id))
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddVideo(generics.CreateAPIView):

    """
    format='multipart/form-data': video_file: video_data, performance: id,
    """

    serializer_class = serializers.VideoCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]
    parser_classes = (MultiPartParser, JSONParser)

    def post(self, request, format="multipart/form-data"):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise exceptions.ValidationError(detail=serializer.errors)


class RatedElementsView(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = serializers.VideoElementSerializer

    def get_queryset(self, video_id):
        try:
            return VideoElement.objects.filter(video_id=video_id)
        except VideoElement.DoesNotExist:
            raise exceptions.NotFound()

    def get(self, request, video_id, format="json"):
        serializer = self.serializer_class(self.get_queryset(video_id), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeviceView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]
    serializer_class = serializers.DeviceSerializer

    def post(self, request, format="json"):

        if FCMDevice.objects.filter(user=self.request.user).exists():
            try:
                FCMDevice.objects.filter(user=self.request.user).update(
                    registration_id=request.data.get("registration_id")
                )
            except:
                raise exceptions.ValidationError()
        else:
            FCMDevice.objects.create(
                user=self.request.user,
                registration_id=request.data.get("registration_id"),
            )

        return Response(status=status.HTTP_200_OK)


class SendNotification(generics.RetrieveAPIView):
    serializer_class = serializers.SendNotificationSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format="json"):

        video_id = request.data.get("video_id")
        video = Video.objects.get(id=video_id)
        user = video.user
        device = FCMDevice.objects.filter(user=user).first()
        if device:
            device.send_message("Уведомление", "Пришла оценка по отправленному видео")

        return Response(status=status.HTTP_200_OK)
