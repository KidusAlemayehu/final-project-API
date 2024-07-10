from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from apps.staff_auth import permission_handler as AuthPermissions
from apps.staff_user.models import OfficeChoices, RoleChoices
from .serializers import MessageSerializer, MessageAttachmentSerializer
from .models import Message

# Create your views here.
class MessageSendAPIView(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [AuthPermissions.IsAuthenticated]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['sender'] = self.request.user
        context['receiver'] = self.request.GET.get('receiver', None)
        return context
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class MessageListView(ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [AuthPermissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Message.objects.all()
        type = self.request.GET.get('type', None)
        if type is None:
            if self.request.user.roles.filter(office__name=OfficeChoices.HOD, role=RoleChoices.ADMINISTRATOR).exists():
                queryset = Message.objects.all().order_by('-created_at')
            else:
                queryset1 = Message.objects.filter(sender=self.request.user.id).order_by('-created_at')
                queryset2 = Message.objects.filter(receiver=self.request.user.id).order_by('-created_at')
                queryset = queryset1.union(queryset2)
        elif type == 'sent':
            queryset = Message.objects.filter(sender=self.request.user.id).order_by('-created_at')
        elif type == 'received':
            queryset = Message.objects.filter(receiver=self.request.user.id).order_by('-created_at')
        else:
            pass
        return queryset.order_by('-created_at')
        
    
