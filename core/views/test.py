from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Avg, Max, Min, Count, Exists, OuterRef
from django.core import serializers
from django.http import JsonResponse
from core.models import Course, CourseContent, CourseMember

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
