from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Avatar(models.Model):
    file_path = models.CharField(max_length=200)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.file_path

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ForeignKey(Avatar, on_delete=models.SET_NULL, null=True, blank=True)
	about = models.TextField(max_length=500, blank=True)
	phone = models.CharField(max_length=15, blank=True)
	country = models.CharField(max_length=50, blank=True)
	birth_date = models.DateField(null=True, blank=True)

	def __str__(self):
		return self.user.username



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
	

	