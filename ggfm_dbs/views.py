from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.messages import success, error, info
from django.db.models import Sum
from .models import Programme, FinancialTransaction, TodoItem, Commercial # Import Commercial
from .forms import CustomUserCreationForm, ProgrammeForm, FinancialTransactionForm, TodoItemForm, CommercialForm # Import CommercialForm
from django.contrib.auth.forms import AuthenticationForm # For login form
from django.utils import timezone

def register_view(request):
    """
    Handles user registration.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log the user in immediately after registration
            success(request, 'Registration successful! You are now logged in.')
            return redirect('dashboard')
        else:
            for field, errors_list in form.errors.items():
                for err in errors_list:
                    error(request, f"{field}: {err}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'ggfm_dbs/register.html', {'form': form})

def user_login_view(request):
    """
    Handles user login.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'ggfm_dbs/login.html', {'form': form})

@login_required
def user_logout_view(request):
    """
    Handles user logout.
    """
    logout(request)
    info(request, 'You have been logged out.')
    return redirect('home')

@login_required
def dashboard_view(request):
    """
    Displays a combined dashboard for financial summary, upcoming programmes, recent to-do items, and recent commercials.
    """
    total_income = FinancialTransaction.objects.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = FinancialTransaction.objects.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    net_balance = total_income - total_expense

    # Get upcoming programmes (starting from now)
    upcoming_programmes = Programme.objects.filter(start_time__gte=timezone.now()).order_by('start_time')[:5]

    recent_transactions = FinancialTransaction.objects.all()[:5] # Display last 5 transactions

    # Get recent incomplete to-do items for the current user
    recent_todo_items = TodoItem.objects.filter(completed=False, created_by=request.user).order_by('due_date', 'priority')[:5]

    # Get recent commercials
    recent_commercials = Commercial.objects.filter(end_date__gte=timezone.now()).order_by('start_date')[:5] # Commercials that are active or upcoming

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'net_balance': net_balance,
        'upcoming_programmes': upcoming_programmes,
        'recent_transactions': recent_transactions,
        'recent_todo_items': recent_todo_items,
        'recent_commercials': recent_commercials, # Add to context
    }
    return render(request, 'ggfm_dbs/dashboard.html', context)

# --- Programme Views ---
@login_required
def programme_list_view(request):
    """
    Displays a list of all programmes.
    """
    programmes = Programme.objects.all()
    context = {'programmes': programmes}
    return render(request, 'ggfm_dbs/programme_list.html', context)

@login_required
def programme_create_view(request):
    """
    Handles creation of new programmes.
    """
    if request.method == 'POST':
        form = ProgrammeForm(request.POST)
        if form.is_valid():
            programme = form.save(commit=False)
            programme.created_by = request.user
            programme.save()
            success(request, 'Programme added successfully!')
            return redirect('programme_list')
        else:
            for field, errors_list in form.errors.items():
                for err in errors_list:
                    error(request, f"{field}: {err}")
    else:
        form = ProgrammeForm()
    return render(request, 'ggfm_dbs/programme_form.html', {'form': form, 'title': 'Add New Programme'})

@login_required
def programme_detail_view(request, pk):
    """
    Displays details of a single programme.
    """
    programme = get_object_or_404(Programme, pk=pk)
    context = {'programme': programme}
    return render(request, 'ggfm_dbs/programme_detail.html', context)

@login_required
def programme_update_view(request, pk):
    """
    Handles updating an existing programme.
    """
    programme = get_object_or_404(Programme, pk=pk)
    if request.method == 'POST':
        form = ProgrammeForm(request.POST, instance=programme)
        if form.is_valid():
            form.save()
            success(request, 'Programme updated successfully!')
            return redirect('programme_detail', pk=pk)
        else:
            for field, errors_list in form.errors.items():
                for err in errors_list:
                    error(request, f"{field}: {err}")
    else:
        form = ProgrammeForm(instance=programme)
    return render(request, 'ggfm_dbs/programme_form.html', {'form': form, 'title': 'Update Programme'})

@login_required
def programme_delete_view(request, pk):
    """
    Handles deletion of a programme.
    """
    programme = get_object_or_404(Programme, pk=pk)
    if request.method == 'POST':
        programme.delete()
        success(request, 'Programme deleted successfully!')
        return redirect('programme_list')
    return render(request, 'ggfm_dbs/confirm_delete_programme.html', {'programme': programme})

# --- Financial Transaction Views ---
@login_required
def financial_transaction_list_view(request):
    """
    Displays a list of all financial transactions.
    """
    transactions = FinancialTransaction.objects.all()
    context = {'transactions': transactions}
    return render(request, 'ggfm_dbs/financial_transaction_list.html', context)

@login_required
def financial_transaction_create_view(request):
    """
    Handles creation of new financial transactions.
    """
    if request.method == 'POST':
        form = FinancialTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.recorded_by = request.user # Assign the current user as recorder
            transaction.save()
            success(request, 'Financial transaction added successfully!')
            return redirect('financial_transaction_list')
        else:
            for field, errors_list in form.errors.items():
                for err in errors_list:
                    error(request, f"{field}: {err}")
    else:
        form = FinancialTransactionForm()
    return render(request, 'ggfm_dbs/financial_transaction_form.html', {'form': form, 'title': 'Add New Financial Transaction'})

@login_required
def financial_transaction_detail_view(request, pk):
    """
    Displays details of a single financial transaction.
    """
    transaction = get_object_or_404(FinancialTransaction, pk=pk)
    context = {'transaction': transaction}
    return render(request, 'ggfm_dbs/financial_transaction_detail.html', context)

@login_required
def financial_transaction_update_view(request, pk):
    """
    Handles updating an existing financial transaction.
    """
    transaction = get_object_or_404(FinancialTransaction, pk=pk)
    if request.method == 'POST':
        form = FinancialTransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            success(request, 'Financial transaction updated successfully!')
            return redirect('financial_transaction_detail', pk=pk)
        else:
            for field, errors_list in form.errors.items():
                for err in errors_list:
                    error(request, f"{field}: {err}")
    else:
        form = FinancialTransactionForm(instance=transaction)
    return render(request, 'ggfm_dbs/financial_transaction_form.html', {'form': form, 'title': 'Update Financial Transaction'})

@login_required
def financial_transaction_delete_view(request, pk):
    """
    Handles deletion of a financial transaction.
    """
    transaction = get_object_or_404(FinancialTransaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        success(request, 'Financial transaction deleted successfully!')
        return redirect('financial_transaction_list')
    return render(request, 'ggfm_dbs/confirm_delete_financial_transaction.html', {'transaction': transaction})

# --- To-Do List Views ---
@login_required
def todo_list_view(request):
    """
    Displays a list of all to-do items for the current user.
    """
    todo_items = TodoItem.objects.filter(created_by=request.user).order_by('completed', 'due_date', '-priority')
    context = {'todo_items': todo_items}
    return render(request, 'ggfm_dbs/todo_list.html', context)

@login_required
def todo_create_view(request):
    """
    Handles creation of new to-do items.
    """
    if request.method == 'POST':
        form = TodoItemForm(request.POST)
        if form.is_valid():
            todo_item = form.save(commit=False)
            todo_item.created_by = request.user
            todo_item.save()
            success(request, 'To-Do item added successfully!')
            return redirect('todo_list')
        else:
            for field, errors_list in form.errors.items():
                for err in errors_list:
                    error(request, f"{field}: {err}")
    else:
        form = TodoItemForm()
    return render(request, 'ggfm_dbs/todo_form.html', {'form': form, 'title': 'Add New To-Do Item'})

@login_required
def todo_detail_view(request, pk):
    """
    Displays details of a single to-do item.
    """
    todo_item = get_object_or_404(TodoItem, pk=pk, created_by=request.user) # Ensure user owns item
    context = {'todo_item': todo_item}
    return render(request, 'ggfm_dbs/todo_detail.html', context)

@login_required
def todo_update_view(request, pk):
    """
    Handles updating an existing to-do item.
    """
    todo_item = get_object_or_404(TodoItem, pk=pk, created_by=request.user) # Ensure user owns item
    if request.method == 'POST':
        form = TodoItemForm(request.POST, instance=todo_item)
        if form.is_valid():
            form.save()
            success(request, 'To-Do item updated successfully!')
            return redirect('todo_detail', pk=pk)
        else:
            for field, errors_list in form.errors.items():
                for err in errors_list:
                    error(request, f"{field}: {err}")
    else:
        form = TodoItemForm(instance=todo_item)
    return render(request, 'ggfm_dbs/todo_form.html', {'form': form, 'title': 'Update To-Do Item'})

@login_required
def todo_delete_view(request, pk):
    """
    Handles deletion of a to-do item.
    """
    todo_item = get_object_or_404(TodoItem, pk=pk, created_by=request.user) # Ensure user owns item
    if request.method == 'POST':
        todo_item.delete()
        success(request, 'To-Do item deleted successfully!')
        return redirect('todo_list')
    return render(request, 'ggfm_dbs/confirm_delete_todo.html', {'todo_item': todo_item})

# --- Commercial Views (New) ---
@login_required
def commercial_list_view(request):
    """
    Displays a list of all commercials.
    """
    commercials = Commercial.objects.all().order_by('start_date')
    context = {'commercials': commercials}
    return render(request, 'ggfm_dbs/commercial_list.html', context)

@login_required
def commercial_create_view(request):
    """
    Handles creation of new commercial entries.
    """
    if request.method == 'POST':
        form = CommercialForm(request.POST)
        if form.is_valid():
            commercial = form.save(commit=False)
            commercial.created_by = request.user
            commercial.save()
            success(request, 'Commercial added successfully!')
            return redirect('commercial_list')
        else:
            for field, errors_list in form.errors.items():
                for err in errors_list:
                    error(request, f"{field}: {err}")
    else:
        form = CommercialForm()
    return render(request, 'ggfm_dbs/commercial_form.html', {'form': form, 'title': 'Add New Commercial'})

@login_required
def commercial_detail_view(request, pk):
    """
    Displays details of a single commercial.
    """
    commercial = get_object_or_404(Commercial, pk=pk)
    context = {'commercial': commercial}
    return render(request, 'ggfm_dbs/commercial_detail.html', context)

@login_required
def commercial_update_view(request, pk):
    """
    Handles updating an existing commercial.
    """
    commercial = get_object_or_404(Commercial, pk=pk)
    if request.method == 'POST':
        form = CommercialForm(request.POST, instance=commercial)
        if form.is_valid():
            form.save()
            success(request, 'Commercial updated successfully!')
            return redirect('commercial_detail', pk=pk)
        else:
            for field, errors_list in form.errors.items():
                for err in errors_list:
                    error(request, f"{field}: {err}")
    else:
        form = CommercialForm(instance=commercial)
    return render(request, 'ggfm_dbs/commercial_form.html', {'form': form, 'title': 'Update Commercial'})

@login_required
def commercial_delete_view(request, pk):
    """
    Handles deletion of a commercial.
    """
    commercial = get_object_or_404(Commercial, pk=pk)
    if request.method == 'POST':
        commercial.delete()
        success(request, 'Commercial deleted successfully!')
        return redirect('commercial_list')
    return render(request, 'ggfm_dbs/confirm_delete_commercial.html', {'commercial': commercial})
