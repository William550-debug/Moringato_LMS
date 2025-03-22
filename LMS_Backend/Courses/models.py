from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from User.models import UserProfile  # Ensure correct import
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import  get_user_model

# Course Model
class Course(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Courses"

# Assignment Model
class Assignment(models.Model):
    instructor = models.ForeignKey(
        User, on_delete=models.CASCADE,
        limit_choices_to={"userprofile__role": "instructor"},
        related_name="assignments"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, related_name="assignments")
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    file = models.FileField(upload_to="assignments/") 

    def __str__(self):
        return f"{self.title} - Due: {self.due_date}"

    class Meta:
        verbose_name_plural = "Assignments"

# Tutorial Model
class Tutorial(models.Model):
    instructor = models.ForeignKey(
        User, on_delete=models.CASCADE,
        limit_choices_to={"userprofile__role": "instructor"},
        related_name="tutorials"
    )
    description = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="tutorials/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"self.title"

    class Meta:
        verbose_name_plural = "Tutorials"

# Notes Model
class Note(models.Model):
    instructor = models.ForeignKey(
        User, on_delete=models.CASCADE,
        limit_choices_to={"userprofile__role": "instructor"},
        related_name="notes"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, related_name="notes")
    topic = models.CharField(max_length=200)
    file = models.FileField(upload_to="notes/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic} - {self.uploaded_at}"

    class Meta:
        verbose_name_plural = "Notes"




#Student Models 



# Student Profile Model
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    student_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    enrolled_courses = models.ManyToManyField("Course", related_name="students", blank=True)

    def __str__(self):
        return f"{self.user.username} - Student"

    class Meta:
        verbose_name_plural = "Student Profiles"


# Enrollment Model



# Assignment Submission Model
class AssignmentSubmission(models.Model):
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    assignment = models.ForeignKey("Assignment", on_delete=models.CASCADE, related_name="submissions")
    file = models.FileField(upload_to="assignments_submissions/" , blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    GRADE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
    ]
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"

    class Meta:
        verbose_name_plural = "Assignment Submissions"





# Quiz Model
User = get_user_model()
class QuizQuestion(models.Model):
    instructor = models.ForeignKey(
        User, on_delete=models.CASCADE,
        limit_choices_to={"userprofile__role": "instructor"},
        related_name="quiz_questions"
    )
    question_text = models.CharField(max_length=255)
    choices = models.JSONField()
    correct_answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question_text} "

    class Meta:
        verbose_name_plural = "Quizzes"

# Quiz Attempt Model
class QuizAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz_attempts")
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, null=True, blank=True)
    selected_answer = models.CharField(max_length=255 ,null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username}'s attempt on - {self.question.question_text}"

    class Meta:
        verbose_name_plural = "Quiz Attempts"



