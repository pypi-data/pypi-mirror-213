import django_filters
from netbox.filtersets import ChangeLoggedModelFilterSet, NetBoxModelFilterSet
from utilities.filters import ContentTypeFilter
from .models import *
from django.db.models import Q


class PTUEventAssignmentFilterSet(ChangeLoggedModelFilterSet):
    content_type = ContentTypeFilter()
    ptuevent_id = django_filters.ModelMultipleChoiceFilter(
        queryset=PTUEvent.objects.all(),
        label='PTUEvent (ID)',
    )
    relation_id = django_filters.ModelMultipleChoiceFilter(
        queryset=PTUEventRelation.objects.all(),
        label='PTUEvent relation (ID)',
    )
    relation = django_filters.ModelMultipleChoiceFilter(
        field_name='relation__name',
        queryset=PTUEventRelation.objects.all(),
        to_field_name='name',
        label='PTUEvent relation (name)',
    )

    class Meta:
        model = PTUEventAssignment
        fields = ['id', 'content_type_id', 'object_id']


class PTAppSystemFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = PTAppSystem
        fields = ['id', 'name', 'slug', 'tenant', 'description', 'comments']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(tenant__icontains=value) |
            Q(slug__icontains=value) |
            Q(description__icontains=value) |
            Q(comments__icontains=value)
        )


class PTAppSystemAssignmentFilterSet(ChangeLoggedModelFilterSet):
    content_type = ContentTypeFilter()
    app_system_id = django_filters.ModelMultipleChoiceFilter(
        queryset=PTAppSystem.objects.all(),
        label='PTAppSystem (ID)',
    )

    class Meta:
        model = PTAppSystemAssignment
        fields = ['id', 'content_type_id', 'object_id']


class PTWorkstationsFilterSet(NetBoxModelFilterSet):
    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value) |
            Q(ad_description__icontains=value) |
            Q(CN__icontains=value) |
            Q(DistinguishedName__icontains=value) |
            Q(ad_guid__icontains=value) |
            Q(ad_description__icontains=value)
        )

    class Meta:
        model = PTWorkstations
        fields = ['id', 'name', 'description', 'ad_description',
                  'CN', 'DistinguishedName', 'ad_guid', 'ad_description']


class PTWorkstationsAssignmentFilterSet(ChangeLoggedModelFilterSet):
    content_type = ContentTypeFilter()
    pt_workstations_id = django_filters.ModelMultipleChoiceFilter(
        queryset=PTWorkstations.objects.all(),
        label='Workstation (ID)',
    )

    class Meta:
        model = PTWorkstationsAssignment
        fields = ['id', 'content_type_id', 'object_id']
