from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

class BaseConsumer(JsonWebsocketConsumer):
    """Wrapper for the default websocket consumer cause it's confusing."""
    def group_add(self, group, channel):
        async_to_sync(self.channel_layer.group_add)(group, channel)

    def group_discard(self, group, channel):
        async_to_sync(self.channel_layer.group_discard)(group, channel)

    def group_send(self, group, obj):
        async_to_sync(self.channel_layer.group_send)(group, obj)
