from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Lunch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                             blank=True)  # If user deletes his/her account, his/her tasks also be deleted. We can also
    # use models.SET_NULL and items remain, not deleted.
    name = models.CharField(max_length=255, default='Default Lunch Name')
    calories = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Breakfast(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                             blank=True)  # If user deletes his/her account, his/her tasks also be deleted. We can also
    # use models.SET_NULL and items remain, not deleted.
    name = models.CharField(max_length=255)
    calories = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Dinner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                             blank=True)  # If user deletes his/her account, his/her tasks also be deleted. We can also
    # use models.SET_NULL and items remain, not deleted.
    name = models.CharField(max_length=255)
    calories = models.FloatField(null=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)


# So cause of we don't want to have error:UserProfile matching query does not exist, which occurs when we are trying
# to retrieve a UserProfile object for a user who does not have an associated UserProfile(This happens if the
# UserProfile object has not been created for a specific user).To resolve this issue, we should ensure that a
# UserProfle is created for each user when they register, so we use Django signals to automatically crate a
# UserProfile object whenever a new user is created. We add a signal handler that creates UserProfile for each new
# user. This signal handlers will ensure that a UserProfile is created when a new user is registered and that it is
# associated with the user.

# Original signal handler
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def populate_personal_info(sender, instance, created, **kwargs):
    if created:
        instance.first_name = "Default First Name"
        instance.last_name = "Default Last Name"
        instance.email = "default@example.com"
        instance.save()

# It listens for the post_save signal, which is triggered when a User model instance (representing a user) is saved,
# typically after a new user is created. When the signal is triggered, it checks if a new user is being created (
# created is True), and if so, it: Sets the user's first name to "Default First Name."Sets the user's last name to
# "Default Last Name."Sets the user's email address to "default@example.com."Finally, it saves these default values
# to the user instance, ensuring that new users are created with these default personal information values.In
# essence, this code sets default first name, last name, and email address values for newly created users when they
# are added to the database.
