import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from django.http import Http404

from core.models import Message, ChatGroup
from base_user.models import MyUser


class ChatConsumer(WebsocketConsumer):
    def __init__(self, room_name=None, room_group_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = room_name
        self.room_group_name = room_group_name
        self.commands = {
            'fetch_messages': self.fetch_messages,
            'new_message': self.new_message
        }

    @staticmethod
    def __message_to_json(message):
        return {
            'user': message.user.email,
            'group': message.group.slug,
            'message': message.message,
            'timestamp': message.timestamp.strftime('%a %H:%M  %d/%m/%y')
        }

    def __messages_to_json(self, messages):
        return [self.__message_to_json(message) for message in messages]

    def fetch_messages(self, data):
        messages = Message.last_10_messages(data['group_name'])

        context = {
            'messages': self.__messages_to_json(messages),
            'command': 'fetch_messages',
        }

        self.send_message(context)

    def new_message(self, data):
        user_email = data['from']
        group_name = data['group_name']

        user = MyUser.objects.filter(email=user_email)[0]
        group = ChatGroup.objects.filter(slug=group_name)[0]

        if user is not None and group is not None:
            message = Message.objects.create(
                user=user,
                group=group,
                message=data['message']
            )

            context = {
                'command': 'new_message',
                'message': self.__message_to_json(message)
            }

            return self.send_chat_message(context)

        raise Http404()

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)

        self.commands[data['command']](data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
