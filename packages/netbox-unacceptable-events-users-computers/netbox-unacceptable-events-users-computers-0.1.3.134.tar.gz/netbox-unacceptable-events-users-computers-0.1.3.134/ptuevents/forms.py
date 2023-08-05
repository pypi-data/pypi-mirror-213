from netbox.forms import NetBoxModelForm
from tenancy.models import Tenant
from pyrsistent import v
from .models import PTUEvent, PTUEventRelation, PTUEventAssignment, PTAppSystem, PTAppSystemAssignment, PTUsers, PTWorkstations, PTWorkstationsAssignment
from utilities.forms.fields import CommentField
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms import BootstrapMixin
from django import forms


class PTUEventForm(NetBoxModelForm):
    class Meta:
        model = PTUEvent
        fields = ('name', 'description', 'comments')


class PTUEventRelationForm(NetBoxModelForm):
    class Meta:
        model = PTUEventRelation
        fields = ('name', 'description')


class PTUEventAssignmentForm(BootstrapMixin, forms.ModelForm):
    ptuevent = DynamicModelChoiceField(
        queryset=PTUEvent.objects.all()
    )
    relation = DynamicModelChoiceField(
        queryset=PTUEventRelation.objects.all()
    )

    class Meta:
        model = PTUEventAssignment
        fields = (
            'ptuevent', 'relation',
        )


class PTAppSystemForm(NetBoxModelForm):
    comments = CommentField()

    class Meta:
        model = PTAppSystem
        fields = ('name', 'slug', 'tenant', 'description', 'comments', 'tags')


class PTAppSystemAssignmentForm(BootstrapMixin, forms.ModelForm):
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(), required=True)
    app_system = DynamicModelChoiceField(queryset=PTAppSystem.objects.all(), query_params={
        'tenant': '$tenant',
    })

    class Meta:
        model = PTAppSystemAssignment
        fields = ('app_system',)


class PTUsersForm(NetBoxModelForm):
    class Meta:
        model = PTUsers
        fields = ('name',
                  'sAMAccountName',
                  'status',
                  'firstname',
                  'lastname', 'ad_guid', 'ad_description', 'position', 'department', 'comment',
                  'vpnIPaddress',
                  'description',
                  'comments')


class PTWorkstationsForm(NetBoxModelForm):
    class Meta:
        model = PTWorkstations
        fields = ('name', 'CN', 'DistinguishedName', 'ad_guid', 'ad_description', 'description')


class PTWorkstationsAssignmentForm(BootstrapMixin, forms.ModelForm):
    # tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=True)
    pt_workstations = DynamicModelChoiceField(queryset=PTWorkstations.objects.all()) # , query_params={'tenant': '$tenant',}

    class Meta:
        model = PTWorkstationsAssignment
        fields = ('pt_workstations',)

