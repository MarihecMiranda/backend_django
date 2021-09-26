from django.shortcuts import render
from rest_framework import generics
from .models import Programa,Pensum
from .serializers import ProgramaSerializers, PensumSerializers

class ProgramaList(generics.ListCreateAPIView):
    queryset=Programa.objects.all()
    serializer_class= ProgramaSerializers

class ProgramaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Programa
    serializer_class= ProgramaSerializers

class PensumList(generics.ListCreateAPIView):
    queryset=Pensum.objects.all()
    serializer_class= PensumSerializers

class PensumDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Pensum
    serializer_class= PensumSerializers
