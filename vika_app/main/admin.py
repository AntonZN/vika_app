from django.contrib import admin
from django import forms

from .models import Performance, Video, ElementType, VideoElement, Comment
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from django.utils.html import escape, mark_safe
from vika_app.account.models import User


class CommentInline(NestedStackedInline):
    model = Comment
    extra = 0

    
class VideoElementInline(NestedStackedInline):
    inlines = (CommentInline,)
    model = VideoElement
    extra = 0


class VideoForm(forms.ModelForm):
    trainer = forms.ModelChoiceField(
        label='Тренер', widget=forms.Select(),
        queryset=User.objects.filter(user_type=User.UserType.TRAINER), required=True)
        
    user = forms.ModelChoiceField(
        label='Тренер', widget=forms.Select(),
        queryset=User.objects.filter(user_type=User.UserType.USER), required=True)

    class Meta:
        model = Video
        fields = '__all__'

        
class VideoAdmin(NestedModelAdmin):
    inlines = (VideoElementInline,)
    list_display = ('__str__', 'user', 'date', 'is_rated', 'image_tag')
    ordering = ('is_rated', '-date')
    readonly_fields = ('date',)
    exclude = ('resolution',)
    form = VideoForm

    def user(self, obj):
        return obj.user.name
    
    def image_tag(self, obj):
        if obj.preview:
            return mark_safe(f'<img width="150px" src="{obj.preview.url}"/>')

    image_tag.short_description = 'Миниатюра'
    image_tag.allow_tags = True

    
        
    user.short_description = 'Ребенок'


class ElementTypeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'image_tag')
    
    def image_tag(self, obj):
        if obj.svg:
            return mark_safe(f'<img width="50px" style="background: #000b;" src="{obj.svg.url}"/>')

    image_tag.short_description = 'Миниатюра'
    image_tag.allow_tags = True


admin.site.register(Performance)
admin.site.register(Video, VideoAdmin)
admin.site.register(ElementType, ElementTypeAdmin)
