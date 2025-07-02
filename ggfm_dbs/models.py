from django.db import models
from django.contrib.auth.models import User # Import Django's built-in User model

class Programme(models.Model):
    """
    Model to represent a GGFM Programme or Event.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    host = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_time'] # Order by start time
        verbose_name = "Programme"
        verbose_name_plural = "Programmes"

    def __str__(self):
        return f"{self.title} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"

class FinancialTransaction(models.Model):
    """
    Model to represent a GGFM financial transaction (income or expense).
    """
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    # Common categories for GGFM finances
    INCOME_CATEGORIES = (
        ('donations', 'Donations'),
        ('grants', 'Grants'),
        ('sponsorships', 'Sponsorships'),
        ('event_revenue', 'Event Revenue'),
        ('other_income', 'Other Income'),
    )

    EXPENSE_CATEGORIES = (
        ('salaries', 'Salaries'),
        ('utilities', 'Utilities'),
        ('rent_facilities', 'Rent/Facilities'),
        ('program_costs', 'Program Costs'),
        ('marketing', 'Marketing'),
        ('equipment', 'Equipment'),
        ('admin_costs', 'Administrative Costs'),
        ('other_expense', 'Other Expense'),
    )

    date = models.DateField()
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=50,
                                choices=INCOME_CATEGORIES + EXPENSE_CATEGORIES,
                                help_text="Select a category for the transaction.")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at'] # Order by date descending, then creation time
        verbose_name = "Financial Transaction"
        verbose_name_plural = "Financial Transactions"

    def __str__(self):
        return f"{self.date} - {self.get_type_display()}: {self.category} - ${self.amount}"

class TodoItem(models.Model):
    """
    Model to represent a To-Do item.
    """
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    task = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    completed = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date', 'priority', '-created_at'] # Order by due date, then priority, then creation time
        verbose_name = "To-Do Item"
        verbose_name_plural = "To-Do Items"

    def __str__(self):
        return f"{self.task} (Due: {self.due_date if self.due_date else 'N/A'}, Priority: {self.get_priority_display()})"

class Commercial(models.Model): # New Commercial Model
    """
    Model to represent a commercial slot or advertisement.
    """
    title = models.CharField(max_length=200)
    advertiser = models.CharField(max_length=100)
    duration_seconds = models.IntegerField(help_text="Duration of the commercial in seconds")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_date', 'advertiser']
        verbose_name = "Commercial"
        verbose_name_plural = "Commercials"

    def __str__(self):
        return f"{self.title} by {self.advertiser} ({self.duration_seconds}s)"
