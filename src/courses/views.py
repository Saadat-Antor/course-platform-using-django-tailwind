from django.shortcuts import render
from . import services
from django.http import Http404, JsonResponse
import helpers


def course_list_view(request):
    queryset = services.get_published_courses()
    # return JsonResponse({"data": [x.public_id for x in queryset]})
    context = {
        "object_list": queryset
    }
    return render(request, "courses/list.html", context)

def course_detail_view(request, course_id=None, *args, **kwargs):
    course_obj = services.get_course_details(course_id=course_id)
    if course_obj is None:
        raise Http404
    lessons_queryset = services.get_course_lessons(course_obj)
    context = {
        "object": course_obj,
        "lessons_queryset": lessons_queryset
    }
    # return JsonResponse({"data": course_obj.path, "lessons_id": [x.path for x in lessons_queryset]})
    return render(request, "courses/detail.html", context)

def lesson_detail_view(request, course_id=None, lesson_id=None):
    lesson_obj = services.get_lesson_details(course_id=course_id, lesson_id=lesson_id)
    if lesson_obj is None:
        raise Http404
    template_name = "courses/lesson-coming-soon.html"
    context = {
        "lesson_obj": lesson_obj
    }
    if not lesson_obj.is_coming_soon and lesson_obj.has_video:
        template_name = "courses/lesson.html"
        video_embed_html = helpers.get_cloudinary_video_obj(
            lesson_obj, 
            field_name='video',
            width=1250,
            as_html=True)
        context['video_embed'] = video_embed_html
    # return JsonResponse({"data": lesson_obj.pk})
    return render(request, template_name, context)