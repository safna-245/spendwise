from django.shortcuts import render,get_object_or_404
from django.db.models import Sum
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,permissions

from spending.serializers import UserSerializer,ExpenseSerializer

from spending.models import Expense
from spending.permissions import IsOwner

from datetime import datetime


# Create your views here.
class SignUpView(APIView):

    def post(self,request):

        form_data = request.data

        serializer_instance = UserSerializer(data=form_data)

        if serializer_instance.is_valid():

            cleaned_data = serializer_instance.validated_data

            instance = User.objects.create_user(**cleaned_data)

            serializer_instance = UserSerializer(instance)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)

class GetMeView(APIView): 

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        auth_user = request.user

        instance = User.objects.get(username=auth_user)

        serializer_instance = UserSerializer(instance)

        return Response(data=serializer_instance.data)

class ExpenseListCreateView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        instance = Expense.objects.filter(owner=request.user)

        serializer_instance = ExpenseSerializer(instance,many=True)

        return Response(data=serializer_instance.data)

    def post(self,request):

        form_data = request.data

        serializer_instance = ExpenseSerializer(data=form_data)

        if serializer_instance.is_valid():

            serializer_instance.save(owner=request.user)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)
        
class ExpenseRetrieveUpdateDeleteView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    
    # permission_classes = [permissions.IsAuthenticated]

    permission_classes = [IsOwner]

    def get(self,request,pk=None):

        instance = get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,instance)

        serializer_instance = ExpenseSerializer(instance)

        return Response(data=serializer_instance.data)

    def put(self,request,pk=None):

        instance = get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,instance)

        form_data =  request.data

        serializer_instance = ExpenseSerializer(data=form_data,instance=instance)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(serializer_instance.data)

        else:

            return Response(serializer_instance.errors)

    def delete(self,request,pk=None):

        instance = get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,instance)

        instance.delete()

        return Response({"message":"deleted..."})

class ExpenseSummaryView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        response_data = {
            "today_total":0
        }

        cur_date = datetime.now().date()

        cur_month = datetime.now().month

        cur_year = datetime.now().year
        #monthly summary

        monthly_transaction = Expense.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)

        if monthly_transaction:

            monthly_total = monthly_transaction.values("amount").aggregate(total=Sum("amount")).get("total")

            response_data["monthly_total"] = monthly_total

        #today summary
        today_transaction = Expense.objects.filter(owner=request.user,created_at__date=cur_date)

        if today_transaction:

            today_total = today_transaction.values("amount").aggregate(total=Sum("amount")).get("total")

            #todays category summary
            category_summary = today_transaction.values("category").annotate(total=Sum("amount"))

            response_data["category_summary"] = category_summary

            response_data["today_total"] = today_total

        return Response(data=response_data)



        










        
    


