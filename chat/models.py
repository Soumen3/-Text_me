from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Friend(models.Model):
	user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_set_1', default=None)
	user_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_set_2', default=None)
	status = models.CharField(max_length=10, choices=[
		('unknown', 'Unknown'),
		('pending', 'Pending'),
		('accepted', 'Accepted'),
		('rejected', 'Rejected'),
		('blocked', 'Blocked'),
	], default='unknown')
    
	def __str__(self):
		return f'{self.user_1.username} - {self.user_2.username}'

	class Meta:
		indexes = [
			models.Index(fields=['user_1']),
			models.Index(fields=['user_2']),
		]
		unique_together = ('user_1', 'user_2')
		
	def get_status(self):
		return self.status
	