from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path('new/', views.newWorkflow, name = 'new'),
    path("requested/", views.RequestedView.as_view(), name="requested"),
    path('withdraw/<int:workflow_id>/', views.withdraw, name = 'withdraw'),
    path("withdrawn/", views.WithdrawnView.as_view(), name="withdrawn"),
    path('dispose/<int:workflow_id>/', views.dispose, name = 'dispose'),
    path("closed/", views.ClosedView.as_view(), name="closed"),
]
