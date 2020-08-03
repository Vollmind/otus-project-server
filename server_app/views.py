from datetime import datetime

from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views import generic

from server_app.models import Address


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Token.objects.create(user=user)
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'server_app/register.html', {'form': form})


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        client_ip = get_client_ip(request)
        Address.objects.filter(user=user).delete()
        Address.objects.create(
            ip=client_ip,
            user=user,
            is_online=True
        )
        return Response({
            'token': token.key
        })


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def online_list(request):
    available_addresses = Address.objects.filter(is_online=True).all()
    return Response({
        'available': [{'user': x.user.username, 'address': x.ip} for x in available_addresses]
    })


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ping_me(request):
    if request.user:
        address = Address.objects.get(user=request.user)
        client_ip = get_client_ip(request)
        address.last_checked = datetime.now()
        address.is_online = True
        address.ip = client_ip
        address.save()
    return Response()


class OnlineView(generic.ListView):
    queryset = Address.objects.all()
    template_name = 'server_app/online.html'
