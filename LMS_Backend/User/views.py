from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *
from Courses.models import *
from django.http import JsonResponse

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime


    




@login_required
def InstructorDashboard(request):
    """
    Render the instructor dashboard page for authenticated users.

    This function is decorated with @login_required, which ensures that only
    authenticated users can access this view. If a user is not authenticated,
    they will be redirected to the login page.

    Parameters:
    request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
    HttpResponse: A rendered HTML response of the 'instructor_dashboard.html' template,
                  which represents the instructor dashboard page of the application.
    """
    total_courses = Course.objects.filter(instructor=request.user).count()
    #active_students = Enrollment.objects.filter(course__instructor=request.user).values('student').distinct().count()
    assignments_due = Assignment.objects.filter(course__instructor=request.user, due_date__gte=timezone.now()).count()
    new_messages = 3  # Placeholder for message count
    submissions = AssignmentSubmission.objects.filter(assignment__instructor=request.user)

    context = {
        'total_courses': total_courses,
        'assignments_due': assignments_due,
        'new_messages': new_messages,
        'submissions': submissions,
        'username': request.user.username,
    }

    return render(request, './instructor/instructor_dashboard.html' , context)

    
@login_required(login_url='login')
def Home(request):
    """
    Render the home page for authenticated students.

    This view function retrieves various educational resources (notes, assignments, submissions, tutorials, and a quiz question)
    and handles quiz submissions. It requires user authentication.

    Parameters:
    request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
    HttpResponse: A rendered HTML response of the 'index.html' template with context data including:
        - assignments: All Assignment objects.
        - notes: All Note objects.
        - submissions: AssignmentSubmission objects for the current user.
        - tutorials: All Tutorial objects.
        - username: The username of the current user.
        - quiz_question: The first QuizQuestion object.

    If a POST request is received, it processes a quiz submission, creating a new QuizAttempt object.
    """
    notes = Note.objects.all()
    assignments = Assignment.objects.all()
    submissions = AssignmentSubmission.objects.filter(student=request.user)
    tutorials = Tutorial.objects.all()
    quizzes = QuizQuestion.objects.all()

 


    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Handle AJAX quiz submission
        selected_answer = request.POST.get('selected_answer')
        quiz_id = request.POST.get('quiz_id')

        quiz = QuizQuestion.objects.get(id=quiz_id)

        if quiz and selected_answer:
            is_correct = selected_answer == quiz.correct_answer
            QuizAttempt.objects.create(
                student=request.user,
                question=quiz,
                selected_answer=selected_answer,
                is_correct=is_correct
            )
            return JsonResponse({
                'result': is_correct,
                'selected_answer': selected_answer,
                'correct_answer': quiz.correct_answer,
                'quiz_id': quiz.id,  # Return the quiz ID for dynamic updates
            })

    context = {
        'assignments': assignments,
        'notes': notes,
        'submissions': submissions,
        'tutorials': tutorials,
        'username': request.user.username,
        'quizzes': quizzes,
    }
    return render(request, './student/index.html', context)
    
def RegisterView(request):
    """
    This function handles the user registration process. It collects user data from the registration form, validates the data,
    and creates a new user if the data is valid. If the data is invalid, it displays error messages and redirects the user back to the registration page.

    Parameters:
    request (HttpRequest): The request object containing information about the HTTP request. This parameter is expected to be an instance of Django's HttpRequest class.

    Returns:
    HttpResponseRedirect: A redirect to the login page if the user registration is successful.
    HttpResponseRedirect: A redirect to the registration page with error messages if the user data is invalid.
    HttpResponse: The rendered register.html template if the request method is not POST.
    """
    #incoming form submission
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        #check if user data has error
        user_data_has_error = False

        #validate if email and username are in use
        if User.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, 'Username is already taken')

        #Validate if email exists
        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, 'Email is already registered')

        #validate if password length is valid
        if len(password)  < 5:
            user_data_has_error = True
            messages.error(request, 'Password must be at least 5 characters Long ')

        #if there are no errors, create new user
        if not user_data_has_error:
            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )

            #Assign the role to the user profile
            UserProfile.objects.create(user=new_user, role=role)

            messages.success(request, "Account created successfully")
            return redirect('login')
        else:
            return redirect('register')

    return render(request, './authentication/register.html')
        
        
    


def LoginView(request):
    """
    This function handles the user login process. It authenticates the user using the provided username and password.
    If the credentials are valid, it logs in the user and redirects them to the appropriate dashboard based on their role.
    If the credentials are invalid, it displays an error message and redirects them back to the login page.

    Parameters:
    request (HttpRequest): The request object containing information about the HTTP request. This parameter is expected to be an instance of Django's HttpRequest class.

    Returns:
    HttpResponseRedirect: A redirect to the instructor dashboard if the user is an instructor.
    HttpResponseRedirect: A redirect to the home page if the user is a student.
    HttpResponseRedirect: A redirect to the login page with an error message if the credentials are invalid.
    HttpResponse: The rendered login.html template if the request method is not POST.
    """
    #incoming form submission
    if request.method == "POST":     

        username = request.POST.get('username')
        password = request.POST.get('password')

        #authenticate user
        user = authenticate(request, username=username, password=password)

        if  user is not  None:

            #Login user if the credentials are valid
            login(request, user)

            #retrieve the user role
            try:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.role == 'instructor':
                    #redirect to instructor dashboard
                    return redirect('instructor-dashboard')
                else:
                    #redirect to home page
                    return redirect('home')
            except UserProfile.DoesNotExist:
                messages.error(request,"User profile DoesNotExist")
                #redirect to home page
                return redirect('login')

            #redirect to home page
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')


    return render(request, './authentication/login.html')



def LogoutView(request):
    """
    This function handles the user logout process. It logs out the user from the current session and redirects them to the login page.

    Parameters:
    request (HttpRequest): The request object containing information about the HTTP request. This parameter is expected to be an instance of Django's HttpRequest class.

    Returns:
    HttpResponseRedirect: A redirect to the login page. This return value indicates that the user has been successfully logged out and redirected to the login page.
    """
    logout(request)

    #redirect user to login page
    return redirect('login')



def ForgotPassword(request):
    """
    This function handles the forgot password process. It checks if a user with the provided email exists in the database.
    If the user exists, it generates a password reset token, creates a password reset URL, sends an email to the user with the URL,
    and redirects the user to the password reset sent page. If the user does not exist, it displays an error message and redirects
    the user back to the forgot password page.

    Parameters:
    request (HttpRequest): The request object containing information about the HTTP request.

    Returns:
    HttpResponseRedirect: A redirect to the password reset sent page with the reset_id if the user exists and the email is sent successfully.
    HttpResponseRedirect: A redirect to the forgot password page with an error message if the user does not exist.
    HttpResponse: The rendered forgot_password.html template if the request method is not POST.
    """
    if request.method == 'POST':
        email = request.POST.get('email')

        #check if user exists
        try:
            user = User.objects.get(email=email)

            #generate reset token
            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()


            #create a password reset url
            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})
            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

            #email content
            email_body = f'Reset Password using the link below: \n \n\n{full_password_reset_url}'

            email_message = EmailMessage(

                'Reset Password using the link below:',
                email_body,
                settings.EMAIL_HOST_USER,
                [email]

                )

            email_message.fail_silently = True
            email_message.send()

            return redirect('password-reset-sent' , reset_id=new_password_reset.reset_id)


        except User.DoesNotExist:
            messages.error(request, f'User  {email} does not exist')
            return redirect('forgot-password')


    return render(request, './authentication/forgot-password.html')



def PasswordResetSent(request, reset_id):
    """
    This function handles the password reset sent page. It checks if a password reset request with the given reset_id exists.
    If it does, it renders the password_reset_sent.html template. If not, it redirects to the forgot password page and displays an error message.

    Parameters:
    request (HttpRequest): The request object containing information about the HTTP request.
    reset_id (str): The unique identifier for the password reset request.

    Returns:
    HttpResponse: The rendered password_reset_sent.html template if the reset_id exists, or a redirect to the forgot password page with an error message if it does not.
    """
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'password_reset_sent.html')
    else:
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('./authentication/forgot_password.html')

    
    
    



#reset Password
def ResetPassword(request, reset_id):
    """
    This function handles the password reset process. It retrieves the password reset request using the provided reset_id.
    If the request is a POST request, it validates the password and confirm password, checks for password length and expiration.
    If all validations pass, it updates the user's password and deletes the password reset request.
    If the reset_id does not exist, it redirects to the forgot password page with an error message.

    Parameters:
    request (HttpRequest): The request object containing information about the HTTP request.
    reset_id (str): The unique identifier for the password reset request.

    Returns:
    HttpResponse: The rendered reset_password.html template if the request is not a POST request or if there are validation errors.
    HttpResponseRedirect: A redirect to the login page if the password reset is successful.
    HttpResponseRedirect: A redirect to the forgot password page with an error message if the reset_id does not exist.
    """
    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            if len(password)  < 5:
                passwords_have_error = True
                messages.error(request, 'Password must be at least 5 characters Long ')

            # Check to make sure the link has not expired
            expiration_time = password_reset_id.created_when  + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                # Delete the reset id if expired
                reset_id.delete()
                passwords_have_error = True
                messages.error(request, 'Link has expired')

            if not passwords_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()
                # Delete the reset id
                reset_id.delete()
                messages.success(request, 'Password reset successfully. Proceed to Login')
                return redirect('login')
            else:
                return redirect('./authentication/reset_password.html', reset_id=reset_id)

    except PasswordReset.DoesNotExist:
        # Redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('./authentication/forgot)password.html')

    return render(request, './authentication/reset_password.html')
