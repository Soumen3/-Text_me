from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import User
from .models import ChatModel
from channels.db import database_sync_to_async
import json

class ChatConsumer(AsyncJsonWebsocketConsumer):
	async def connect(self):
		my_id = self.scope['user'].id
		friend_id = self.scope['url_route']['kwargs']['id']

		if my_id > friend_id:
			room_name = f"{friend_id}_{my_id}"
		else:
			room_name = f"{my_id}_{friend_id}"

		self.room_group_name = f"chat_{room_name}"

		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)

		await self.accept()

		print("Connected to the websocket")


	


	async def receive_json(self, content, **kwargs):
		print("Received content",content)
	
		message = content['message']
		sender_username = content['sender_username']
		timestamp = content['timestamp']
		print(content)
		friend_id = content['friend_id']

		await self.save_message(self.scope['user'],message,friend_id, self.room_group_name, timestamp)
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type':'chat_message',
				'message':message,
				'sender_username':sender_username,
				'timestamp':timestamp
			}
		)
		
	@database_sync_to_async
	def save_message(self, user,message,friend_id, thread, timestamp):
		receiver=User.objects.get(id=friend_id)
		ChatModel.objects.create(
			sender=user,
			receiver=receiver,
			thread=thread,
			message=message,
			timestamp=timestamp
		)


	async def chat_message(self,event):
		print("Received message",event)
		message = event['message']
		sender_username = event['sender_username']
		timestamp = event['timestamp']

		await self.send_json({
			'message':message,
			'sender_username':sender_username,
			'timestamp':timestamp
		})




	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)
		print("Disconnected to the websocket")
		