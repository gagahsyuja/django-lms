from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField("course name", max_length=100)
    description = models.TextField("description", default="-")
    price = models.IntegerField("price", default=10000)
    image = models.ImageField("image", null=True, blank=True)
    teacher = models.ForeignKey(User, verbose_name="teacher", on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Course",
        verbose_name_plural = "Courses"

    def __str__(self) -> str:
        return self.name + " : " + str(self.price)

ROLE_OPTIONS = [('std', 'Student'), ('ast', 'Assistant')]

class CourseMember(models.Model):
    course_id = models.ForeignKey(Course, verbose_name="course", on_delete=models.RESTRICT)
    user_id = models.ForeignKey(User, verbose_name="student", on_delete=models.RESTRICT)
    roles = models.CharField("roles", max_length=3, choices=ROLE_OPTIONS, default='std')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Course Member",
        verbose_name_plural = "Course Members",

    def __str__(self) -> str:
        return self.course_id + " : " + self.user_id

class CourseContent(models.Model):
    name = models.CharField("content title", max_length=200)
    description = models.TextField("description", default="-")
    video_url = models.CharField("video URL", max_length=200, null=True, blank=True)
    file_attachment = models.FileField("file", null=True, blank=True)
    course_id = models.ForeignKey(Course, verbose_name="course", on_delete=models.RESTRICT)
    parent_id = models.ForeignKey("self", verbose_name="parent", on_delete=models.RESTRICT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Course Content",
        verbose_name_plural = "Course Contents"

    def __str__(self) -> str:
        return "[" + self.course_id + "]" + self.name

class Comment(models.Model):
    content_id = models.ForeignKey(CourseContent, verbose_name="content", on_delete=models.CASCADE)
    member_id = models.ForeignKey(CourseMember, verbose_name="member", on_delete=models.CASCADE)
    comment = models.TextField("comment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Comment",
        verbose_name_plural = "Comments"

    def __str__(self) -> str:
        return "Comment: " + self.content.id.name + " - " + self.user_id
