from rest_framework import serializers


class DashboardSummarySerializer(serializers.Serializer):
    total_properties = serializers.IntegerField()
    total_rooms = serializers.IntegerField()
    active_tenancies = serializers.IntegerField()
    vacant_rooms = serializers.IntegerField()
    expected_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    collected_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    pending_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    occupancy_rate = serializers.FloatField()
    dash_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    dash_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    dash_profit = serializers.DecimalField(max_digits=12, decimal_places=2)
    dash_due = serializers.DecimalField(max_digits=12, decimal_places=2)
