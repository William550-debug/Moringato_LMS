from django.urls import path
from .views import *

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/create/', CourseCreateView.as_view(), name='course-create'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('assignments/create/', AssignmentCreateView.as_view(), name='assignment-create'),
    path('courses/<int:course_id>/assignments/', AssignmentListView.as_view(), name='assignment-list'),
    path('courses/<int:course_id>/tutorials/', TutorialListView.as_view(), name='tutorial-list'),
   
    #path('quizzes/<int:quiz_id>/attempt/', quiz_attempt, name='quiz-attempt'),
    #path('courses/<int:course_id>/enroll/', enroll_in_course, name='enroll-course'),
    #path('enrolled-courses/', EnrolledCoursesListView.as_view(), name='enrolled-courses'),
    path('assignments/<int:pk>/submit/', AssignmentSubmissionCreateView.as_view(), name='assignment-submit'),
    #path('quiz-attempts/<int:pk>/', QuizAttemptDetailView.as_view(), name='quiz-results'),

    path('upload-assignment/', upload_assignment, name='upload-assignment'),
    path('upload-note/', upload_note, name='upload-note'),
    path('view-notes/', view_notes, name='view-notes'),
    path('upload-tutorial/', upload_tutorial, name='upload-tutorial'),

    #delete view
    path('instructor-dashboard/delete/<int:tutorial_id>' , delete_tutorial, name='delete_tutorial'),
    #path('instructor-dashboard/assignment/<int:assignment_id>', view_assignment, name='view-assignment'),
    path('delete/<int:note_id>' , delete_note, name='delete_note'),
    path('instructor-dashboard/assignment/delete/<int:assignment_id>' ,delete_assignment, name='delete-assignment'),

    


    #assignment
    path('submit-assignment/<int:assignment_id>/', submit_assignment, name='submit-assignment'),
    path('grade-submission/<int:submission_id>/', grade_submission, name='grade-submission'),
    
    #quizes
    path('upload/', QuizQuestionCreateView.as_view(), name='quiz_upload'),
    path('list/', QuizQuestionListView.as_view(), name='quiz_list'),
    path('attempt/<int:pk>/', QuizAttemptView.as_view(), name='attempt_quiz'),
    path('result/<int:pk>/', QuizResultView.as_view(), name='quiz_result'),


]