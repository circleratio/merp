from django.forms import ModelForm
from .models import Workflow

class WorkflowForm(ModelForm):
    class Meta:
        model = Workflow
        ch = ['出張精算', '経費精算', '支払']
        fields = ['title', 'flow_type', 'approvers', 'observers']
