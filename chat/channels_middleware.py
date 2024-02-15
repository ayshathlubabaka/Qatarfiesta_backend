from channels.middleware import BaseMiddleware
from rest_framework.exceptions import AuthenticationFailed
from django.db import close_old_connections
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser
import logging
from accounts.models import User

logger = logging.getLogger(__name__)


class JWTWebsocketMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        close_old_connections()
        query_string = scope.get("query_string", b"").decode("utf-8")
        query_parameter = dict(qp.split("=") for qp in query_string.split("&"))
        token = query_parameter.get("token", None)

        if token is None:
            await send({"type": "websocket.close", "code": 4000})
        user = await self.get_user_from_token(token)
        if user:
            scope["user"] = user
        else:
            await send({"type": "websocket.close", "code": 4000})
        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user_from_token(self, access_token):
        try:
            token = AccessToken(access_token)
            payload = token.payload
            user_id = payload.get("user_id")

            if user_id is not None:
                user = User.objects.get(id=user_id)
                return user
        except Exception as e:
            print(f"Error decoding token: {e}")

        return AnonymousUser()
