from .models import (Course,
                     Lesson,
                     PublishStatus)

def get_published_courses():
    return Course.objects.filter(status=PublishStatus.PUBLISHED)

def get_course_details(course_id=None):
    if course_id is None:
        return None
    obj = None
    try:
        obj = Course.objects.get(status=PublishStatus.PUBLISHED,
                                 id=course_id)
    except:
        pass
    return obj

def get_lesson_details(course_id=None, lesson_id=None):
    if lesson_id is None:
        return None
    obj = None
    try:
        obj = Lesson.objects.get(course___id=course_id, 
                                 course___status=PublishStatus.PUBLISHED,
                                 id=lesson_id,
                                 status=PublishStatus.PUBLISHED
                                 )
    except:
        pass
    return obj

def get_course_lessons(course_id=None):
    if course_id is None:
        return []
    return Lesson.objects.filter(course_id=course_id)