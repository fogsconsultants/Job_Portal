from django import forms
from jobs.models import Jobs


class ApplicationStatusForm(forms.Form):
    status = forms.ChoiceField(choices=[
        ("Submitted", "Submitted"),
        ("In review", "In review"),
        ("Shortlisted", "Shortlisted"),
        ("Interview", "Interview"),
        ("Not selected", "Not selected"),
    ])

class JobForm(forms.ModelForm):
    class Meta: 
        model=Jobs
        fields = ["title", "sector", "location", "employment_type", "description", "salary", "is_active"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. Senior Product Designer"}),
            "location": forms.TextInput(attrs={"placeholder": "e.g. Bengaluru or Remote"}),
            "description": forms.Textarea(attrs={"rows": 7, "placeholder": "Describe the role, responsibilities, and requirements."}),
            "salary": forms.TextInput(attrs={"placeholder": "e.g. ₹12–18 LPA"}),
        }

