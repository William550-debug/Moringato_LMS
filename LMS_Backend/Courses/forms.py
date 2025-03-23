from django import forms
from .models import *

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = [ 'title', 'description', 'file', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'placeholder':'YYYY-MM-DD', 'class': 'form-control'}),
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [ 'topic', 'file']


class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['file']



class GradeSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['grade']

class TutorialForm(forms.ModelForm):
    class Meta:
        model = Tutorial
        fields = ['title', 'description', 'file', ]


class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = ['question_text', 'choices', 'correct_answer']
        widgets = {
            'choices': forms.TextInput(attrs={'placeholder': 'Enter choices as a JSON list, e.g., ["Choice 1", "Choice 2"]'}),
            'correct_answer': forms.TextInput(attrs={'placeholder': 'Enter the correct choice exactly as it appears in the choices list'}),
        }