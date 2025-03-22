from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from .models import  *
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from .forms import *
from django.http import JsonResponse, HttpResponseRedirect

# -------------------------------
# COURSE VIEWS
# -------------------------------

class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    fields = ['title', 'description']
    template_name = 'course_create.html'
    success_url = reverse_lazy('course-list')

    def test_func(self):
        # Ensure only instructors can create courses
        return self.request.user.userprofile.role == 'instructor'

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super().form_valid(form)

class CourseListView(ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'

class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_detail.html'
    context_object_name = 'course'

# -------------------------------
# ASSIGNMENT VIEWS
# -------------------------------

class AssignmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Assignment
    fields = ['course', 'title', 'description', 'due_date']
    template_name = 'assignment_create.html'
    success_url = reverse_lazy('assignment-list')

    def test_func(self):
        return self.request.user.userprofile.role == 'instructor'

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super().form_valid(form)

class AssignmentListView(LoginRequiredMixin, ListView):
    model = Assignment
    template_name = 'assignment_list.html'
    context_object_name = 'assignments'

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        return Assignment.objects.filter(course=course)

class AssignmentSubmissionCreateView(LoginRequiredMixin, CreateView):
    model = AssignmentSubmission
    fields = ['assignment', 'file']
    template_name = 'assignment_submission_create.html'
    success_url = reverse_lazy('assignment-list')

    def form_valid(self, form):
        form.instance.student = self.request.user
        return super().form_valid(form)
    



# -------------------------------
# TUTORIAL VIEWS
# -------------------------------

class TutorialListView(LoginRequiredMixin, ListView):
    model = Tutorial
    template_name = 'tutorial_list.html'
    context_object_name = 'tutorials'

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        return Tutorial.objects.filter(course=course)

# -------------------------------
# QUIZ VIEWS
# -------------------------------

class QuizQuestionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = QuizQuestion
    form_class = QuizQuestionForm
    template_name = './instructor/questions_form.html'
    success_url = reverse_lazy('quiz_list')

    def test_func(self):
        return self.request.user.userprofile.role == 'instructor'

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super().form_valid(form)
    
class QuizQuestionListView(ListView):
    model = QuizQuestion
    template_name = './instructor/questions_list.html'
    context_object_name = 'questions'
    
    

"""
@login_required
def quiz_attempt(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()  # Fetch questions related to the quiz

    # Prevent duplicate quiz attempts
    if QuizAttempt.objects.filter(student=request.user, quiz=quiz).exists():
        messages.warning(request, "You have already attempted this quiz.")
        return redirect('quiz-results', quiz_id=quiz.id)

    if request.method == 'POST':
        score = 0
        total_questions = questions.count()

        for question in questions:
            user_answer = request.POST.get(f'question_{question.id}')  # Get student answer
            if user_answer == question.correct_option:
                score += 1  # Increment score if answer is correct

        final_score = (score / total_questions) * 100  # Convert to percentage

        # Save attempt
        QuizAttempt.objects.create(student=request.user, quiz=quiz, score=final_score)

        messages.success(request, "Quiz submitted successfully.")
        return redirect('quiz-results', quiz_id=quiz.id)

    return render(request, './student/quiz_attempt.html', {'quiz': quiz, 'questions': questions})
"""

class QuizAttemptView(LoginRequiredMixin, DetailView):
    model = QuizQuestion
    template_name = 'quiz/attempt_quiz.html'
    context_object_name = 'question'

    def post(self, request, *args, **kwargs):
        question = self.get_object()
        selected_answer = request.POST.get('selected_answer')
        is_correct = selected_answer == question.correct_answer

        QuizAttempt.objects.create(
            student=request.user,
            question=question,
            selected_answer=selected_answer,
            is_correct=is_correct
        )

        return HttpResponseRedirect(reverse_lazy('quiz_result', kwargs={'pk': question.id}))
    

class QuizResultView(LoginRequiredMixin, DetailView):
    model = QuizQuestion
    template_name = './student/quiz_result.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attempt = QuizAttempt.objects.filter(student=self.request.user, question=self.object).first()
        context['attempt'] = attempt
        return context

# -------------------------------
# ENROLLMENT VIEWS
# -------------------------------

"""def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)

    if created:
        messages.success(request, "Successfully enrolled in the course.")
    else:
        messages.info(request, "You are already enrolled in this course.")

    return redirect('course-detail', pk=course.id)"""

"""class EnrolledCoursesListView(LoginRequiredMixin, ListView):
    model = Enrollment
    template_name = 'enrolled_courses.html'
    context_object_name = 'enrollments'

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user).select_related('course')
"""
# -------------------------------
# QUIZ SCORING FUNCTION
# -------------------------------

def calculate_score(post_data):
    score = 0
    total_questions = 0

    for question_id, selected_option in post_data.items():
        try:
            question = Question.objects.get(id=question_id)
            if question.correct_option == selected_option:
                score += 1
            total_questions += 1
        except Question.DoesNotExist:
            continue  # Skip invalid question IDs

    return (score / total_questions) * 100 if total_questions > 0 else 0


# -------------------------------
# Recent Activity
# -------------------------------

def recent_activity(request):
    graded_assignments = AssignmentSubmission.objects.filter(assignment__course__instructor=request.user, graded=True).order_by('-submission_date')[:5]
    new_submissions = AssignmentSubmission.objects.filter(assignment__course__instructor=request.user, graded=False).order_by('-submission_date')[:5]

    context = {
        'graded_assignments': graded_assignments,
        'new_submissions': new_submissions,
    }
    return context

# -------------------------------
# File uploads
# -------------------------------
def upload_file(request, file_type):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        # Save file metadata to the database
        return redirect('./instructor/instructor_dashboard.html')
    
@login_required
def upload_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.instructor = request.user
            assignment.save()
            return redirect('instructor-dashboard')
    else:
        form = AssignmentForm()
    assignment = Assignment.objects.all()
    return render(request, './instructor/issue_assignment.html', {'form': form})
@login_required
def upload_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.instructor = request.user
            note.save()
            messages.success(request, 'Note uploaded successfully!')
            return redirect('upload-note')
    else:
        form = NoteForm()
    return render(request, './instructor/upload_notes.html', {'form': form})

@login_required
def upload_tutorial(request):
    if request.method == 'POST':
        form = TutorialForm(request.POST, request.FILES)
        if form.is_valid():
            tutorial = form.save(commit=False)
            tutorial.instructor = request.user
            tutorial.save()
            messages.success(request, 'Tutorial uploaded successfully')  # Inform user of successful submission
            return redirect('upload-tutorial')
        

    else:
        form = TutorialForm()

    tutorials  = Tutorial.objects.all()

    return render(request, './instructor/upload_tutorial.html', {'form': form, "tutorials": tutorials})
    
# -------------------------------
# Grade Submissions
# -------------------------------

def grade_submission(request, submission_id):
    submission = get_object_or_404(AssignmentSubmission, id=submission_id)
    if request.method == 'POST':
        form = GradeSubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
           
            return JsonResponse({'status': 'success', 'grade': submission.grade})
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# -------------------------------
# STUDENT ACCESS
# -------------------------------


# Student View Notes
@login_required
def view_notes(request):
 
    
    notes = Note.objects.filter(instructor=request.user)
    return render(request, './instructor/view_notes.html', {'notes': notes})
    
@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = request.user
            submission.assignment = assignment
            submission.save()
            return redirect('home')
    else:
        form = AssignmentSubmissionForm()
    return render(request, './student/submit_assignment.html', {'form': form, 'assignment': assignment})



# -------------------------------
# Instructor ACCESS
# -------------------------------
@login_required
def view_submissions(request):
    submissions = AssignmentSubmission.objects.filter(assignment__instructor=request.user)
    return render(request, 'view_submissions.html', {'submissions': submissions})


@login_required
def view_tutorials(request):
    tutorials = Tutorial.objects.all()
    return render(request, 'view_tutorials.html', {'tutorials': tutorials})

@login_required
def view_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, instructor=request.user)
    return render(request, './instructor/view_assignment.html', {'assignment': assignment})


# -------------------------------
# DELETE VIEWS
# -------------------------------
# Instructor: Delete Tutorial


def delete_tutorial(request, tutorial_id):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id, instructor=request.user)
    tutorial.file.delete()
    tutorial.delete()
    return redirect('upload-tutorial')


#delete assignments
def delete_assignment(request , assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, instructor=request.user)
    assignment.delete()
    return redirect('view-assignment')







#delete note
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, instructor=request.user)
    note.file.delete()
    note.delete()
    return redirect('view-notes')