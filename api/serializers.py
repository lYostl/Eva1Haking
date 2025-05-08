from rest_framework import serializers
import re

class DomainSerializer(serializers.Serializer):
    domain = serializers.CharField()

    def validate_domain(self, value):
        pattern = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.(?:[A-Za-z]{2,6})$"
        if not re.match(pattern, value):
            raise serializers.ValidationError("Dominio inválido")
        return value

class TargetSerializer(serializers.Serializer):
    target = serializers.CharField()
