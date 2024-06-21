from rest_framework import serializers
from .models import Account, Destination
import uuid

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ('app_secret_token', 'account_id')

    def create(self, validated_data):
        validated_data['app_secret_token'] = str(uuid.uuid4())
        return super(AccountSerializer, self).create(validated_data)

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'
