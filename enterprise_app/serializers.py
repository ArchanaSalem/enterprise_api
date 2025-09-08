from rest_framework import serializers
from .models import Enterprise, Region, Circle, Cluster, Store,Role
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator
import re  
    # re nah eegular expression 

class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = ['id', 'name', 'is_active', 'created_on', 'updated_on']

    def validate_name(self, value):
        qs = Enterprise.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Enterprise with this name already exists.")
        return value


class RegionSerializer(serializers.ModelSerializer):
    enterprise_id = serializers.IntegerField(write_only=True, required=True)
    enterprise_name = serializers.CharField(source='enterprise.name', read_only=True)

    class Meta:
        model = Region
        fields = ['id', 'name', 'enterprise_id', 'enterprise_name', 'is_active', 'created_on', 'updated_on']

    def validate(self, data):
        enterprise_id = data.get('enterprise_id') if 'enterprise_id' in data else (self.instance.enterprise_id if self.instance else None)
        name = data.get('name', self.instance.name if self.instance else None)
        if not enterprise_id:
            raise serializers.ValidationError({"enterprise_id": "enterprise_id is required."})
        # check enterprise exists and active
        try:
            ent = Enterprise.objects.get(pk=enterprise_id)
        except Enterprise.DoesNotExist:
            raise serializers.ValidationError({"enterprise_id": "Enterprise does not exist."})

        qs = Region.objects.filter(enterprise_id=enterprise_id, name__iexact=name)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError({"name": "Region with this name already exists for this enterprise."})
        return data


class CircleSerializer(serializers.ModelSerializer):
    enterprise_id = serializers.IntegerField(write_only=True, required=True)
    region_id = serializers.IntegerField(write_only=True, required=True)
    enterprise_name = serializers.CharField(source='enterprise.name', read_only=True)
    region_name = serializers.CharField(source='region.name', read_only=True)

    class Meta:
        model = Circle
        fields = ['id', 'name', 'enterprise_id', 'region_id', 'enterprise_name', 'region_name',
                  'is_active', 'created_on', 'updated_on']

    def validate(self, data):
        enterprise_id = data.get('enterprise_id') if 'enterprise_id' in data else (self.instance.enterprise_id if self.instance else None)
        region_id = data.get('region_id') if 'region_id' in data else (self.instance.region_id if self.instance else None)
        name = data.get('name', self.instance.name if self.instance else None)

        if not enterprise_id or not region_id:
            raise serializers.ValidationError({"detail": "enterprise_id and region_id are required."})

        # validate parents exist
        try:
            Enterprise.objects.get(pk=enterprise_id)
        except Enterprise.DoesNotExist:
            raise serializers.ValidationError({"enterprise_id": "Enterprise does not exist."})
        try:
            Region.objects.get(pk=region_id, enterprise_id=enterprise_id)
        except Region.DoesNotExist:
            raise serializers.ValidationError({"region_id": "Region does not exist under given enterprise."})

        qs = Circle.objects.filter(enterprise_id=enterprise_id, region_id=region_id, name__iexact=name)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError({"name": "Circle with this name already exists in this enterprise+region."})

        return data


class ClusterSerializer(serializers.ModelSerializer):
    enterprise_id = serializers.IntegerField(write_only=True, required=True)
    region_id = serializers.IntegerField(write_only=True, required=True)
    circle_id = serializers.IntegerField(write_only=True, required=True)
    enterprise_name = serializers.CharField(source='enterprise.name', read_only=True)
    region_name = serializers.CharField(source='region.name', read_only=True)
    circle_name = serializers.CharField(source='circle.name', read_only=True)

    class Meta:
        model = Cluster
        fields = ['id', 'name', 'enterprise_id', 'region_id', 'circle_id',
                  'enterprise_name', 'region_name', 'circle_name',
                  'is_active', 'created_on', 'updated_on']

    def validate(self, data):
        enterprise_id = data.get('enterprise_id') if 'enterprise_id' in data else (self.instance.enterprise_id if self.instance else None)
        region_id = data.get('region_id') if 'region_id' in data else (self.instance.region_id if self.instance else None)
        circle_id = data.get('circle_id') if 'circle_id' in data else (self.instance.circle_id if self.instance else None)
        name = data.get('name', self.instance.name if self.instance else None)

        if not (enterprise_id and region_id and circle_id):
            raise serializers.ValidationError({"detail": "enterprise_id, region_id and circle_id are required."})

        # validate parents
        try:
            Enterprise.objects.get(pk=enterprise_id)
        except Enterprise.DoesNotExist:
            raise serializers.ValidationError({"enterprise_id": "Enterprise does not exist."})
        try:
            Region.objects.get(pk=region_id, enterprise_id=enterprise_id)
        except Region.DoesNotExist:
            raise serializers.ValidationError({"region_id": "Region does not exist under given enterprise."})
        try:
            Circle.objects.get(pk=circle_id, enterprise_id=enterprise_id, region_id=region_id)
        except Circle.DoesNotExist:
            raise serializers.ValidationError({"circle_id": "Circle does not exist under given enterprise+region."})

        qs = Cluster.objects.filter(enterprise_id=enterprise_id, region_id=region_id, circle_id=circle_id, name__iexact=name)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError({"name": "Cluster with this name already exists in this enterprise+region+circle."})
        return data


class StoreSerializer(serializers.ModelSerializer):
    enterprise_id = serializers.IntegerField(write_only=True, required=True)
    region_id = serializers.IntegerField(write_only=True, required=True)
    circle_id = serializers.IntegerField(write_only=True, required=True)
    cluster_id = serializers.IntegerField(write_only=True, required=True)

    enterprise_name = serializers.CharField(source='enterprise.name', read_only=True)
    region_name = serializers.CharField(source='region.name', read_only=True)
    circle_name = serializers.CharField(source='circle.name', read_only=True)
    cluster_name = serializers.CharField(source='cluster.name', read_only=True)

    class Meta:
        model = Store
        fields = [
            'id', 'name',
            'enterprise_id', 'region_id', 'circle_id', 'cluster_id',
            'enterprise_name', 'region_name', 'circle_name', 'cluster_name',
            'industry', 'location',
            'is_active', 'created_on', 'updated_on'
        ]

    def validate(self, data):
        enterprise_id = data.get('enterprise_id') if 'enterprise_id' in data else (self.instance.enterprise_id if self.instance else None)
        region_id = data.get('region_id') if 'region_id' in data else (self.instance.region_id if self.instance else None)
        circle_id = data.get('circle_id') if 'circle_id' in data else (self.instance.circle_id if self.instance else None)
        cluster_id = data.get('cluster_id') if 'cluster_id' in data else (self.instance.cluster_id if self.instance else None)
        name = data.get('name', self.instance.name if self.instance else None)

        if not (enterprise_id and region_id and circle_id and cluster_id):
            raise serializers.ValidationError({"detail": "enterprise_id, region_id, circle_id and cluster_id are required."})

        # validate parent chain
        try:
            Enterprise.objects.get(pk=enterprise_id)
        except Enterprise.DoesNotExist:
            raise serializers.ValidationError({"enterprise_id": "Enterprise does not exist."})
        try:
            Region.objects.get(pk=region_id, enterprise_id=enterprise_id)
        except Region.DoesNotExist:
            raise serializers.ValidationError({"region_id": "Region does not exist under given enterprise."})
        try:
            Circle.objects.get(pk=circle_id, enterprise_id=enterprise_id, region_id=region_id)
        except Circle.DoesNotExist:
            raise serializers.ValidationError({"circle_id": "Circle does not exist under given enterprise+region."})
        try:
            Cluster.objects.get(pk=cluster_id, enterprise_id=enterprise_id, region_id=region_id, circle_id=circle_id)
        except Cluster.DoesNotExist:
            raise serializers.ValidationError({"cluster_id": "Cluster does not exist under given enterprise+region+circle."})

        qs = Store.objects.filter(
            enterprise_id=enterprise_id, region_id=region_id,
            circle_id=circle_id, cluster_id=cluster_id, name__iexact=name
        )
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError({"name": "Store with this name already exists in this enterprise+region+circle+cluster"})
#-------Role Serialiser
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description','is_active', 'created_on', 'updated_on']
        read_only_fields = ['id','is_active', 'created_on', 'updated_on']


