from django.urls import path
from . import models, views
from netbox.views.generic import ObjectChangeLogView

urlpatterns = (
    # PTUEvents
    path('ptuevents/', views.PTUEventListView.as_view(), name='ptuevent_list'),
    path('ptuevents/add/', views.PTUEventEditView.as_view(), name='ptuevent_add'),
    path('ptuevents/<int:pk>/', views.PTUEventView.as_view(), name='ptuevent'),
    path('ptuevents/<int:pk>/edit/', views.PTUEventEditView.as_view(),
         name='ptuevent_edit'),
    path('ptuevents/<int:pk>/delete/', views.PTUEventDeleteView.as_view(),
         name='ptuevent_delete'),
    path('ptuevents/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='ptuevent_changelog', kwargs={
        'model': models.PTUEvent
    }),
    #  PTUEvent relation
    path('ptueventrelation/', views.PTUEventRelationListView.as_view(),
         name='ptueventrelation_list'),
    path('ptueventrelation/add/', views.PTUEventRelationEditView.as_view(),
         name='ptueventrelation_add'),
    path('ptueventrelation/<int:pk>/',
         views.PTUEventRelationView.as_view(), name='ptueventrelation'),
    path('ptueventrelation/<int:pk>/edit/',
         views.PTUEventRelationEditView.as_view(), name='ptueventrelation_edit'),
    path('ptueventrelation/<int:pk>/delete/',
         views.PTUEventRelationDeleteView.as_view(), name='ptueventrelation_delete'),
    path('ptueventrelation/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='ptueventrelation_changelog', kwargs={
        'model': models.PTUEventRelation
    }),
    # PTUEvent assignment
    path('ptueventassignment/add/', views.PTUEventAssignmentEditView.as_view(),
         name='ptueventassignment_add'),
    path('ptueventassignment/<int:pk>/edit/', views.PTUEventAssignmentEditView.as_view(),
         name='ptueventassignment_edit'),
    path('ptueventassignment/<int:pk>/delete/', views.PTUEventAssignmentDeleteView.as_view(),
         name='ptueventassignment_delete'),

    path('app-systems/', views.PTAppSystemListView.as_view(),
         name="ptappsystem_list"),
    path('app-systems/add', views.PTAppSystemEditView.as_view(),
         name="ptappsystem_add"),
    path('app-systems/<int:pk>/',
         views.PTAppSystemView.as_view(), name="ptappsystem"),
    path('app-systems/<int:pk>/edit',
         views.PTAppSystemEditView.as_view(), name="ptappsystem_edit"),
    path('app-systems/<int:pk>/delete',
         views.PTAppSystemDeleteView.as_view(), name="ptappsystem_delete"),
    path('app-systems/<int:pk>/changelog', ObjectChangeLogView.as_view(),
         name="ptappsystem_changelog", kwargs={'model': models.PTAppSystem}),

    # app system assignment
    path('app-system-assignment/add/', views.PTAppSystemAssignmentEditView.as_view(),
         name='ptappsystemassignment_add'),
    path('app-system-assignment/<int:pk>/edit/', views.PTAppSystemAssignmentEditView.as_view(),
         name='ptappsystemassignment_edit'),
    path('app-system-assignment/<int:pk>/delete/', views.PTAppSystemAssignmentDeleteView.as_view(),
         name='ptappsystemassignment_delete'),

    # PTUsers
    path('ptusers/', views.PTUsersListView.as_view(), name='ptusers_list'),
    path('ptusers/add/', views.PTUsersEditView.as_view(), name='ptusers_add'),
    path('ptusers/<int:pk>/', views.PTUsersView.as_view(), name='ptusers'),
    path('ptusers/<int:pk>/edit/', views.PTUsersEditView.as_view(), name='ptusers_edit'),
    path('ptusers/<int:pk>/delete/', views.PTUsersDeleteView.as_view(), name='ptusers_delete'),
    path('ptusers/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='ptusers_changelog', kwargs={ 'model': models.PTUsers}),

    # PTWorkstations
    path('ptworkstations/', views.PTWorkstationsListView.as_view(), name='ptworkstations_list'),
    path('ptworkstations/add/', views.PTWorkstationsEditView.as_view(), name='ptworkstations_add'),
    path('ptworkstations/<int:pk>/', views.PTWorkstationsView.as_view(), name='ptworkstations'),
    path('ptworkstations/<int:pk>/edit/', views.PTWorkstationsEditView.as_view(), name='ptworkstations_edit'),
    path('ptworkstations/<int:pk>/delete/', views.PTWorkstationsDeleteView.as_view(), name='ptworkstations_delete'),
    path('ptworkstations/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='ptworkstations_changelog', kwargs={ 'model': models.PTWorkstations}),

    # PTWorkstations assignment
    path('ptworkstationsassignment/add/', views.PTWorkstationsAssignmentEditView.as_view(),
         name='ptworkstationsassignment_add'),
    path('ptworkstationsassignment/<int:pk>/edit/', views.PTWorkstationsAssignmentEditView.as_view(),
         name='ptworkstationsassignment_edit'),
    path('ptworkstationsassignment/<int:pk>/delete/', views.PTWorkstationsAssignmentDeleteView.as_view(),
         name='ptworkstationsassignment_delete'),

)
