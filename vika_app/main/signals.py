from django.db.models.signals import pre_save, post_save, pre_delete
from vika_app.main.models import VideoElement, Video
from django.dispatch import receiver
from moviepy.editor import *
import random
import os
from django.conf import settings
from django.core.files import File
from PIL import Image


@receiver(post_save, sender=VideoElement)
def element_created(sender, instance, created, **kwargs):
    if created:
        d = 0
        e = 0
        for element in VideoElement.objects.filter(video=instance.video).values(
            "d1d2", "d3d4", "e1e2", "e3e6"
        ):
            d += element["d1d2"] + element["d3d4"]
            e += element["e1e2"] + element["e3e6"]

        rate = d + e
        video = instance.video
        video.rate = rate
        video.save()


@receiver(post_save, sender=Video)
def video_created(sender, instance, created, **kwargs):
    if created:
        if not os.path.exists(os.path.join(settings.BASE_DIR, "thumbnails")):
            os.makedirs(os.path.join(settings.BASE_DIR, "thumbnails"))
        video_size = instance.resolution.split("x")
        v_w = int(video_size[0])
        v_h = int(video_size[1])
        clip = VideoFileClip(instance.video_file.url, target_resolution=[v_h, v_w])
        video_name = os.path.basename(instance.video_file.name)
        video_name = video_name.split(".")[0]
        thumbnail_name = f"thumbnail_{instance.id}_{video_name}.jpg"
        thumbnail = os.path.join(
            settings.BASE_DIR, os.path.join("thumbnails", thumbnail_name)
        )
        clip.save_frame(thumbnail)
        img = Image.open(thumbnail)

        if v_h < v_w:
            left = (v_w - v_h) / 2
            top = (v_h - v_h) / 2
            right = (v_w + v_h) / 2
            bottom = (v_h + v_h) / 2
            img = img.crop((left, top, right, bottom))
        else:
            left = (v_w - v_w) / 2
            top = (v_h - v_w) / 2
            right = (v_w + v_w) / 2
            bottom = (v_h + v_w) / 2
            img = img.crop((left, top, right, bottom))

        img.save(thumbnail)
        preview = File(open(thumbnail, "rb"))
        instance.preview.save(thumbnail_name, preview, save=True)
        instance.video_duration = clip.duration
        instance.save()
        os.remove(thumbnail)
