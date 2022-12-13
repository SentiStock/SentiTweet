"""
ASGI config for sentitweet project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sentitweet.settings')

# application = get_asgi_application()
application = ProtocolTypeRouter()



# from django.core.asgi import get_asgi_application

# from .middleware import TokenAuthMiddleware
# from channels.routing import ProtocolTypeRouter, URLRouter
# from .urls import websocket_urlpatterns

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": TokenAuthMiddleware(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ),
# })
