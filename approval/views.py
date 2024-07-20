from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render, redirect
from django.views import generic
from django.db.models import Q

from .models import Workflow
from .forms import WorkflowForm

class IndexView(generic.ListView):
    template_name = "approval/index.html"
    context_object_name = "workflow_list"

    def get_queryset(self):
        """Return the approval requsts by myself."""
        return Workflow.objects.filter(originator=self.request.user, status='run')
    
    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['tab_selection'] = 'index'
        return ctx
    
class RequestedView(generic.ListView):
    template_name = "approval/index.html"
    context_object_name = "workflow_list"

    def get_queryset(self):
        """Return the approval requsts by myself."""
        return Workflow.objects.filter(owner=self.request.user, status='run')

    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['tab_selection'] = 'requested'
        return ctx
    
class WithdrawnView(generic.ListView):
    template_name = "approval/index.html"
    context_object_name = "workflow_list"

    def get_queryset(self):
        """Return the approval requsts by myself."""
        return Workflow.objects.filter(originator=self.request.user, status='withdrawn')
    
    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['tab_selection'] = 'withdrawn'
        return ctx
    
class ClosedView(generic.ListView):
    template_name = "approval/index.html"
    context_object_name = "workflow_list"

    def get_queryset(self):
        """Return closed approval requsts."""
        return Workflow.objects.filter(Q(originator=self.request.user), Q(status='approved') | Q(status='rejected') | Q(status='disposed'))
    
    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['tab_selection'] = 'closed'
        return ctx
    
class DetailView(generic.DetailView):
    model = Workflow
    template_name = "approval/detail.html"

def newWorkflow(request):
    if request.method == 'POST':
        form = WorkflowForm(request.POST)
        if form.is_valid():
            wf = Workflow()
            wf.title = form.cleaned_data['title']
            wf.originator = request.user
            wf.flow_type = form.cleaned_data['flow_type']
            wf.approvers = form.cleaned_data['approvers']
            wf.observers = form.cleaned_data['observers']
            wf.save()
            return redirect('index')
    else:
        form = WorkflowForm()

    return render(request, 'approval/form.html', {'form': form})

def withdraw(request, workflow_id):
    try:
        wf = Workflow.objects.get(pk=workflow_id)
    except Workflow.DoesNotExist:
        raise Http404("Workflow does not exist")
    wf.status = 'withdrawn'
    wf.save()
    return render(request, "approval/detail.html", {"workflow": wf})

def dispose(request, workflow_id):
    try:
        wf = Workflow.objects.get(pk=workflow_id)
    except Workflow.DoesNotExist:
        raise Http404("Workflow does not exist")
    wf.status = 'disposed'
    wf.save()
    return render(request, "approval/detail.html", {"workflow": wf})
