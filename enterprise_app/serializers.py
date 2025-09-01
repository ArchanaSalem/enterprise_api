from rest_framework import serializers
from .models import Enterprise, Region, Circle, Cluster, Store

# ------------------- Enterprise Serializer -------------------
class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = ['id', 'name', 'is_active']
        read_only_fields = ['id']

    def validate_name(self, value):
        if Enterprise.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Enterprise with this name already exists.")
        return value


# ------------------- Region Serializer -------------------
class RegionSerializer(serializers.ModelSerializer):
    enterprise_id = serializers.PrimaryKeyRelatedField(
        queryset=Enterprise.objects.all(),
        source='enterprise',
        write_only=True
    )

    class Meta:
        model = Region
        fields = ['id', 'name', 'enterprise_id', 'is_active']
        read_only_fields = ['id']

    def validate(self, attrs):
        enterprise = attrs['enterprise']
        name = attrs['name']
        if Region.objects.filter(name__iexact=name, enterprise=enterprise).exists():
            raise serializers.ValidationError("Region with this name already exists for this enterprise.")
        return attrs


# ------------------- Circle Serializer -------------------
class CircleSerializer(serializers.ModelSerializer):
    enterprise_id = serializers.PrimaryKeyRelatedField(
        queryset=Enterprise.objects.all(),
        source='enterprise',
        write_only=True
    )
    region_id = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(),
        source='region',
        write_only=True
    )

    class Meta:
        model = Circle
        fields = ['id', 'name', 'enterprise_id', 'region_id', 'is_active']
        read_only_fields = ['id']

    def validate(self, attrs):
        enterprise = attrs['enterprise']
        region = attrs['region']
        name = attrs['name']
        if Circle.objects.filter(name__iexact=name, enterprise=enterprise, region=region).exists():
            raise serializers.ValidationError("Circle with this name already exists in this region for this enterprise.")
        return attrs


# ------------------- Cluster Serializer -------------------
class ClusterSerializer(serializers.ModelSerializer):
    enterprise_id = serializers.PrimaryKeyRelatedField(
        queryset=Enterprise.objects.all(),
        source='enterprise',
        write_only=True
    )
    region_id = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(),
        source='region',
        write_only=True
    )
    circle_id = serializers.PrimaryKeyRelatedField(
        queryset=Circle.objects.all(),
        source='circle',
        write_only=True
    )

    class Meta:
        model = Cluster
        fields = ['id', 'name', 'enterprise_id', 'region_id', 'circle_id', 'is_active']
        read_only_fields = ['id']

    def validate(self, attrs):
        enterprise = attrs['enterprise']
        region = attrs['region']
        circle = attrs['circle']
        name = attrs['name']
        if Cluster.objects.filter(name__iexact=name, enterprise=enterprise, region=region, circle=circle).exists():
            raise serializers.ValidationError("Cluster with this name already exists in this circle for this enterprise.")
        return attrs


# ------------------- Store Serializer -------------------
class StoreSerializer(serializers.ModelSerializer):
    enterprise_id = serializers.PrimaryKeyRelatedField(
        queryset=Enterprise.objects.all(),
        source='enterprise',
        write_only=True
    )
    region_id = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(),
        source='region',
        write_only=True
    )
    circle_id = serializers.PrimaryKeyRelatedField(
        queryset=Circle.objects.all(),
        source='circle',
        write_only=True
    )
    cluster_id = serializers.PrimaryKeyRelatedField(
        queryset=Cluster.objects.all(),
        source='cluster',
        write_only=True
    )

    class Meta:
        model = Store
        fields = [
            'id', 'name', 'enterprise_id', 'region_id', 'circle_id', 'cluster_id',
            'is_active', 'location', 'industry', 'updated_on', 'deleted_on'
        ]
        read_only_fields = ['id', 'updated_on', 'deleted_on']

    def validate(self, attrs):
        enterprise = attrs['enterprise']
        region = attrs['region']
        circle = attrs['circle']
        cluster = attrs['cluster']
        name = attrs['name']
        if Store.objects.filter(
            name__iexact=name,
            enterprise=enterprise,
            region=region,
            circle=circle,
            cluster=cluster
        ).exists():
            raise serializers.ValidationError("Store with this name already exists in this cluster for this enterprise.")
        return attrs
