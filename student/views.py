from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer
from django.shortcuts import render

class StudentApiView(APIView):
    def get(self, requset):
        students = Student.objects.all()[:5]
        serializers = StudentSerializer(students, many=True)
        return Response(serializers.data)
