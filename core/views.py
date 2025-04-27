from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Avg, Max, Min, Count
from django.core import serializers
from django.http import JsonResponse
from core.models import Course

def test(request):

    test_user = User.objects.filter(username="testuser")

    if not test_user.exists():
        test_user = User.objects.create_user(
            username="testuser",
            email="testuser@mail.com",
            password="password"
        )

    all_users = serializers.serialize('python', User.objects.all())

    admin = User.objects.get(username="testuser")

    test_user.delete()

    after_delete = serializers.serialize('python', User.objects.all())

    response = {
        "admin_user": serializers.serialize('python', [admin])[0],
        "all_users": all_users,
        "users_after_delete": after_delete
    }

    return JsonResponse(response)

def allCourse(request):

    all_course = Course.objects.all()

    results = []

    for course in all_course:
        record = {
            'id': course.id,
            'name': course.name,
            'description': course.description,
            'price': course.price,
            'teacher': {
                'id': course.teacher.id,
                'username': course.teacher.username,
                'email': course.teacher.email,
                'fullname': f"{course.teacher.first_name} {course.teacher.last_name}"
            }
        }
        results.append(record)

    return JsonResponse(results, safe=False)

def userCourses(request):
    user = User.objects.get(pk=3)
    courses = Course.objects.filter(teacher=user.id)
    course_data = []

    for course in courses:
        record = {
            "id": course.id,
            "name": course.name,
            "description": course.description,
            "price": course.price
        }
        course_data.append(record)

    result = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "fullname": f"{user.first_name} {user.last_name}",
        "courses": course_data
    }

    return JsonResponse(result, safe=False)

def courseStat(request):
    courses = Course.objects.all()
    stats = courses.aggregate(
        max_price=Max("price"),
        min_price=Min("price"),
        avg_price=Avg("price"),
    )

    result = { "course_count": len(courses), "courses": stats }

    return JsonResponse(result, safe=False)

def courseMemberStat(request):
    courses = Course.objects.filter(description__contains="python") \
        .annotate(member_num=Count("coursemember"))

    course_data = []

    for course in courses:
        record = {
            "id": course.id,
            "name": course.name,
            "price": course.price,
            "member_count": course.member_num
        }
        course_data.append(record)

    result = { "data_count": len(course_data), "data": course_data }

    return JsonResponse(result)
