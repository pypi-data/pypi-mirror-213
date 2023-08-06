from django.urls import path
from machine_tracking import models, views
from netbox.views.generic import ObjectChangeLogView


urlpatterns = (

    path('event/', views.EventListView.as_view(), name='event_list'),
    path('event/add/', views.EventEditView.as_view(), name='event_add'),
    path('event/<int:pk>/', views.EventView.as_view(), name='event'),
    path('event/<int:pk>/edit/', views.EventEditView.as_view(), name='event_edit'),
    path('event/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    path('event/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='event_changelog', kwargs={
        'model': models.Event
    }),

    path('replacement/', views.ReplacementListView.as_view(), name='replacement_list'),
    path('replacement/add/', views.ReplacementEditView.as_view(), name='replacement_add'),
    path('replacement/<int:pk>/', views.ReplacementView.as_view(), name='replacement'),
    path('replacement/<int:pk>/edit/', views.ReplacementEditView.as_view(), name='replacement_edit'),
    path('replacement/<int:pk>/delete/', views.ReplacementDeleteView.as_view(), name='replacement_delete'),
    path('replacement/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='replacement_changelog', kwargs={
        'model': models.Replacement
    }),
)