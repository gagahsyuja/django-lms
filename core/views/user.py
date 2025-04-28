from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Avg, Max, Min, Count, Exists, OuterRef
from django.core import serializers
from django.http import JsonResponse
from core.models import Course, CourseContent, CourseMember

def users(request):
    result = serializers.serialize('python', User.objects.all())
    return JsonResponse(result, safe=False)

def userStat(request):

    users = User.objects.all()

    usersWithCourseCount = User.objects.filter(
        Exists(Course.objects.filter(teacher=OuterRef("pk")))
    ).count()

    # usersWithCourseCount = Course.objects \
    #     .values("teacher") \
    #     .annotate(count=Count("name")) \
    #     .order_by("teacher") \
    #     .count()

    usersWithoutCourseCount = User.objects.exclude(
        Exists(Course.objects.filter(teacher=OuterRef("pk")))
    ).count()

    courseFollowedCount = CourseMember.objects \
        .values("course_id") \
        .annotate(member_count=Count("user_id"))

    courseFollowedByOneUserCount = courseFollowedCount \
        .filter(member_count=1) \
        .count()
        # .aggregate(average_course_followed_by_one_user=Avg(member_count))

    userFollowCount = CourseMember.objects \
        .values("user_id") \
        .annotate(course_followed_count=Count("course_id")) \

    userMostFollowedCourse = userFollowCount \
        .order_by("-course_followed_count")[:3]

    userFollowedMostCourse = courseFollowedCount \
        .filter(member_count=1) \
        .count()

    userWithNoCourse = userFollowCount \
        .filter(course_followed_count=0)

    result = {
        "user_count": users.count(),
        "user_with_course_count": usersWithCourseCount,
        "user_without_course_count": usersWithoutCourseCount,
        "average_course_followed_by_a_user": courseFollowedByOneUserCount,
        "user_with_most_followed_course": list(userMostFollowedCourse),
        "user_with_no_course_followed": list(userWithNoCourse)
    }

    return JsonResponse(result, safe=False)

