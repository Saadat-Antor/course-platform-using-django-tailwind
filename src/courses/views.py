from django.shortcuts import render
from . import services
from django.http import Http404, JsonResponse


def course_list_view(request):
    queryset = services.get_published_courses()
    return JsonResponse({"data": [x.pk for x in queryset]})
    # return render(request, "courses/list.html", {})

def course_detail_view(request, course_id=None, *args, **kwargs):
    course_obj = services.get_course_details(course_id=course_id)
    if course_obj is None:
        raise Http404
    lessons_queryset = services.get_course_lessons(course_id=course_id)
    return JsonResponse({"data": course_obj.pk, "lessons_id": [x.pk for x in lessons_queryset]})
    # return render(request, "courses/detail.html", {})

def lesson_detail_view(request, course_id=None, lesson_id=None):
    lesson_obj = services.get_lesson_details(course_id=course_id, lesson_id=lesson_id)
    if lesson_obj is None:
        raise Http404
    return JsonResponse({"data": lesson_obj.pk})
    # return render(request, "courses/lesson.html", {})