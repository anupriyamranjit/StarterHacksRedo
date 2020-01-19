from django.db import models

# Create your models here.
class IDtoUser(models.Model):
	name = models.CharField(max_length = 25)
	ID_Device = models.CharField(max_length = 50)
	def __str__(self):
		return self.name
	class Meta:
		verbose_name_plural = 'IDtoUsers'