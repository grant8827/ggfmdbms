from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Programme, FinancialTransaction, TodoItem, Commercial # Import Commercial

class CustomUserCreationForm(UserCreationForm):
    """
    A custom user creation form to extend Django's default.
    Adds email field to registration.
    """
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)

class ProgrammeForm(forms.ModelForm):
    """
    Form for creating and updating Programme entries.
    """
    class Meta:
        model = Programme
        fields = ['title', 'description', 'start_time', 'end_time', 'location', 'host']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input rounded-md shadow-sm'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input rounded-md shadow-sm'}),
            'title': forms.TextInput(attrs={'class': 'form-input rounded-md shadow-sm'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-textarea rounded-md shadow-sm'}),
            'location': forms.TextInput(attrs={'class': 'form-input rounded-md shadow-sm'}),
            'host': forms.TextInput(attrs={'class': 'form-input rounded-md shadow-sm'}),
        }
        labels = {
            'title': 'Programme Title',
            'description': 'Description',
            'start_time': 'Start Time',
            'end_time': 'End Time (Optional)',
            'location': 'Location (Optional)',
            'host': 'Host/Presenter (Optional)',
        }

class FinancialTransactionForm(forms.ModelForm):
    """
    Form for creating and updating financial transactions.
    """
    class Meta:
        model = FinancialTransaction
        fields = ['date', 'type', 'category', 'amount', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input rounded-md shadow-sm'}),
            'type': forms.Select(attrs={'class': 'form-select rounded-md shadow-sm'}),
            'category': forms.Select(attrs={'class': 'form-select rounded-md shadow-sm'}),
            'amount': forms.NumberInput(attrs={'class': 'form-input rounded-md shadow-sm', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-textarea rounded-md shadow-sm'}),
        }
        labels = {
            'date': 'Date',
            'type': 'Transaction Type',
            'category': 'Category',
            'amount': 'Amount ($)',
            'description': 'Description (Optional)',
        }

class TodoItemForm(forms.ModelForm): # New TodoItemForm
    """
    Form for creating and updating To-Do items.
    """
    class Meta:
        model = TodoItem
        fields = ['task', 'description', 'due_date', 'priority', 'completed']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input rounded-md shadow-sm'}),
            'priority': forms.Select(attrs={'class': 'form-select rounded-md shadow-sm'}),
            'task': forms.TextInput(attrs={'class': 'form-input rounded-md shadow-sm'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-textarea rounded-md shadow-sm'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5 text-purple-600 rounded-md'}),
        }
        labels = {
            'task': 'Task',
            'description': 'Description (Optional)',
            'due_date': 'Due Date (Optional)',
            'priority': 'Priority',
            'completed': 'Completed',
        }

class CommercialForm(forms.ModelForm): # New CommercialForm
    """
    Form for creating and updating Commercial entries.
    """
    class Meta:
        model = Commercial
        fields = ['title', 'advertiser', 'duration_seconds', 'start_date', 'end_date', 'cost', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input rounded-md shadow-sm'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input rounded-md shadow-sm'}),
            'title': forms.TextInput(attrs={'class': 'form-input rounded-md shadow-sm'}),
            'advertiser': forms.TextInput(attrs={'class': 'form-input rounded-md shadow-sm'}),
            'duration_seconds': forms.NumberInput(attrs={'class': 'form-input rounded-md shadow-sm'}),
            'cost': forms.NumberInput(attrs={'class': 'form-input rounded-md shadow-sm', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-textarea rounded-md shadow-sm'}),
        }
        labels = {
            'title': 'Commercial Title',
            'advertiser': 'Advertiser',
            'duration_seconds': 'Duration (seconds)',
            'start_date': 'Start Date (Optional)',
            'end_date': 'End Date (Optional)',
            'cost': 'Cost (Optional)',
            'notes': 'Notes (Optional)',
        }
