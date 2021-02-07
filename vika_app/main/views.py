from django.http import HttpResponse
from django.http.response import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.views.generic.list import ListView

from vika_app.account.models import User
from vika_app.main.models import *


def video_list(request):

    context = {
        "users": User.objects.filter(user_type=User.UserType.USER),
        "videos": Video.objects.filter(is_rated=False).order_by("-date"),
    }

    return render(request, "find.html", context=context)


def video_rating(request, video_uuid):

    context = {
        "users": User.objects.filter(user_type=User.UserType.USER),
        "video": Video.objects.get(id=video_uuid),
        "elements": ElementType.objects.all(),
    }

    return render(request, "rating.html", context=context)
