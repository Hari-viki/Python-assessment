from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
import requests

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def delete(self, request):
        instance = self.get_object()
        instance.destinations.all().delete() 
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

    def delete(self, request):
        instance = self.get_object()
        instance.delete() 
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



@api_view(['POST'])
def incoming_data(request):

    token = request.headers.get('CL-X-TOKEN')
    if not token:
        return Response({"error": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        account = get_object_or_404(Account, app_secret_token=token)
        print(f"Token Account: {account}")  
    except Exception as e:
        print(f"Error finding account: {e}")  
        return Response({"error": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED)

    data = request.data
    print(f"Received data: {data}")  
    
    for destination in account.destinations.all():
        headers = destination.headers
        url = destination.url
        method = destination.http_method.lower()
        print(f"Database url is {url} with method {method}")  
        
        try:
            if method == 'get':
                response = requests.get(url, params=data, headers=headers)
            elif method == 'post':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'put':
                response = requests.put(url, json=data, headers=headers)
            else:
                continue
            
            print(f"Response from {url}: {response.status_code}")  

        except:        
            pass
    return Response({"status": "success", "Value send to postman for testing": data}, status=status.HTTP_200_OK)
