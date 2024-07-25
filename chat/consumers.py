from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
import json

class ChatConsumer(AsyncJsonWebsocketConsumer):
	async def connect(self):
		await self.accept()
		print("Connected to the websocket")
		await self.send_json({"message":"Connected to the websocket"})

	async def receive_json(self, content, **kwargs):
		print("Received content",content)
		await self.send_json(content)
		

	async def disconnect(self, close_code):
		print("Disconnected to the websocket")
		