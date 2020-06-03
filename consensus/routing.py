from channels.routing import ProtocolTypeRouter, URLRouter

import confusion.routing

application = ProtocolTypeRouter({
    'websocket': URLRouter(confusion.routing.websocket_urlpatterns),
})
