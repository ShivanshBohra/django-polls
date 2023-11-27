import datetime
import logging
from django.contrib import admin
from django.db import models
from django.utils import timezone

# Get an instance of the logger
logger = logging.getLogger(__name__)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self) -> str:
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        recently_published = now - datetime.timedelta(days=1) <= self.pub_date <= now

        # Log whether the question was published recently or not
        logger.info("Question '%s' was_published_recently: %s", self.question_text, recently_published)

        return recently_published


class Choice(models.Model):
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.choice_text

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Log when a new choice is saved
        logger.info("New choice '%s' saved for question '%s'", self.choice_text, self.question.question_text)

    def delete(self, *args, **kwargs):
        # Log when a choice is deleted
        logger.info("Choice '%s' for question '%s' deleted", self.choice_text, self.question.question_text)

        super().delete(*args, **kwargs)
