import uuid
import os

from django.db import models
from django.utils import timezone
from vika_app.account.models import User


class Performance(models.Model):
    class Meta:
        verbose_name = "Вид выступления"
        verbose_name_plural = "Виды выступлений"

    name = models.CharField("Вид выступления", max_length=100)

    def __str__(self):
        return self.name


class Video(models.Model):
    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Загруженные видео"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь(ребенок)",
        on_delete=models.CASCADE,
        related_name="videos",
    )
    trainer = models.ForeignKey(
        User,
        null=True,
        blank=True,
        verbose_name="Тренер",
        on_delete=models.SET_NULL,
        related_name="+",
    )
    performance = models.ForeignKey(
        Performance,
        null=True,
        verbose_name="Тип выступления",
        blank=True,
        on_delete=models.SET_NULL,
        related_name="videos",
    )
    video_file = models.FileField("Видео файл", upload_to="video")
    video_duration = models.FloatField("Длительность видео", blank=True, null=True)
    preview = models.ImageField("Превью", upload_to="images/previews", blank=True)
    date = models.DateTimeField("Дата создания", default=timezone.now)
    rate = models.FloatField("Общий бал", default=0)
    is_rated = models.BooleanField("Оценен", default=False)
    resolution = models.CharField(default="1920x1080", max_length=15)

    def __str__(self):
        return f"Видео {self.id}"


class ElementType(models.Model):
    class Meta:
        verbose_name = "Элемент"
        verbose_name_plural = "Список элементов"

    name = models.CharField("Название Элемента", max_length=1000)
    svg = models.FileField("Иконка svg", upload_to="images/icons", blank=True)

    def __str__(self):
        return self.name


class VideoElement(models.Model):
    class Meta:
        verbose_name = "Элемент"
        verbose_name_plural = "Элементы в видео"

    video = models.ForeignKey(
        Video, verbose_name="Видео", related_name="elements", on_delete=models.CASCADE
    )
    type = models.ForeignKey(
        ElementType,
        related_name="+",
        verbose_name="Вид элемента",
        null=True,
        on_delete=models.SET_NULL,
    )
    start_time = models.CharField("Время начала", max_length=100)
    end_time = models.CharField("Время конца", max_length=100)
    d1d2 = models.FloatField("d1d2", default=0)
    d3d4 = models.FloatField("d3d4", default=0)
    e1e2 = models.FloatField("e1e2", default=0)
    e3e6 = models.FloatField("e3e6", default=0)
    pointer = models.CharField("Точка", blank=True, max_length=100)

    def __str__(self):
        return f"Элемент {self.pk}"


class Comment(models.Model):
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    element = models.OneToOneField(
        VideoElement,
        verbose_name="Элемент",
        related_name="comments",
        on_delete=models.CASCADE,
    )
    c_d1d2 = models.CharField(
        "Комментарий к оценке d1d2", max_length=500, blank=True, null=True
    )
    c_d3d4 = models.CharField(
        "Комментарий к оценке d3d4", max_length=500, blank=True, null=True
    )
    c_e1e2 = models.CharField(
        "Комментарий к оценке e1e2", max_length=500, blank=True, null=True
    )
    c_e3e6 = models.CharField(
        "Комментарий к оценке e3e6", max_length=500, blank=True, null=True
    )

    def __str__(self):
        return f"Комментарий {self.pk}"
