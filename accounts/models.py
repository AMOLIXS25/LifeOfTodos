from django.db import models

from django.conf import settings

from django.contrib.auth.models import User, AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

class Profile(models.Model):
    class Rank(models.TextChoices):
        NOVICE = 'NOV', 'Novice 🌱'
        APPRENTICE = 'APPR', 'Apprentis 🔰' 
        DISCIPLINED = 'DISC', 'Discipliné ⏳'
        LEGEND = 'LEG', 'Légende de la displine 🔥'
        MONK = 'MONK', 'Moine de la Productivité 🧘'

    class DisplayMode(models.TextChoices):
        DARK = 'DK', 'dark'
        LIGHT = 'LG', 'light'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profil')
    profil_pic = models.URLField(default='https://i.imgur.com/KiiziZ1.png',blank=True)
    number_of_completed_task = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    rank = models.CharField(max_length=5, choices=Rank.choices, default=Rank.NOVICE)
    display_mode = models.CharField(max_length=2, choices=DisplayMode.choices, default=DisplayMode.DARK)

    def update_display_mode(self, display_mode):
        if display_mode == 'dark':
            self.display_mode = Profile.DisplayMode.DARK
        else:
            self.display_mode = Profile.DisplayMode.LIGHT
        self.save()

    def get_rank(self):
        if self.points < 35 and self.number_of_completed_task < 5:
            return Profile.Rank.NOVICE
        elif self.points < 140 and self.number_of_completed_task < 20:
            return Profile.Rank.APPRENTICE
        elif self.points < 350 and self.number_of_completed_task < 50:
            return Profile.Rank.DISCIPLINED
        elif self.points < 1750 and self.number_of_completed_task < 250:
            return Profile.Rank.LEGEND
        else:
            return Profile.Rank.MONK

    def complete_task(self):
        self.points += 7
        self.number_of_completed_task += 1
        self.rank = self.get_rank()

        self.save()

    def reset_stats(self):
        self.number_of_completed_task = 0
        self.points = 0
        self.rank = Profile.Rank.NOVICE
        self.save()

    def __str__(self):
        return f'Profile : {self.user}'