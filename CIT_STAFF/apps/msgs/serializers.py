from rest_framework import serializers
from.models import Message, MessageAttachment


class MessageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageAttachment
        fields = "__all__"
        
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ['sender', 'receiver', 'created_at', 'updated_at']
        
    def validate(self, attrs):
        attrs['sender'] = self.context.get('sender')
        attrs['receiver'] = self.context.get('receiver')
        print('Sender: ', attrs['sender'])
        return attrs
    
