from django.db import models
from django.db.models import fields
from rest_framework import serializers
from pensum.models import Programa, Pensum

class ProgramaSerializers(serializers.ModelSerializer):
    class Meta:
        model=Programa
        fields='__all__'

class PensumSerializers(serializers.ModelSerializer):
    class Meta:
        model=Pensum
        fields='__all__'
    
    def validate(self, data):
        if data["expiration_date"] < data["date_issue"]:
            raise serializers.ValidationError(_("la fecha de expiracion no puede ser menor a la fecha de emision"))
        return data
