from django.shortcuts import render
from . import services
from django.http import Http404, JsonResponse


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
    lessons_queryset = services.get_course_lessons(course_id=course_id)
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
    context = {
        "lesson_obj": lesson_obj
    }
    # return JsonResponse({"data": lesson_obj.pk})
    return render(request, "courses/lesson.html", context)