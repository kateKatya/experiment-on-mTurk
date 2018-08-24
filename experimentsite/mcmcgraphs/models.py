from django.db import models
from django.utils import timezone
import datetime
#from .utils import step_size

# Create your models here.


class Participant(models.Model):
    session_id = models.CharField(max_length=1000, primary_key=True)
    session_start = models.DateTimeField(default=timezone.now)
    amt_id = models.CharField(max_length=1000, default="")
    terms_accepted = models.BooleanField(default=False)
    time_start = models.DateTimeField(default=timezone.now)
    time_end = models.DateTimeField(default=timezone.now)
    unique_code = models.CharField(max_length=1000, default="")
    prior = models.CharField(max_length=1000, default="") # e.g. expo 2.1, linear etc
    weights = models.CharField(max_length=1000, default="") # weights that were assigned to the chains

    # Quiz fields
    quiz_completed = models.BooleanField(default=False)
    quiz_runs = models.PositiveSmallIntegerField(default=0)

    # Trials fields
    trials_stage = models.PositiveSmallIntegerField(default=0)
    trials_correct = models.PositiveSmallIntegerField(default=0)
    choices = models.CharField(max_length=1000, default="")
    choice_datetime = models.CharField(max_length=20000, default="")
    curr_state_place = models.CharField(max_length=1000, default="")
    chain_shown = models.CharField(max_length=1000, default="")
    chain_1 = models.CharField(max_length=1000, default="") # Current state of Chain 1
    chain_1_all = models.CharField(max_length=10000, default="") # All current states of Chain 1
    chain_2 = models.CharField(max_length=1000, default="")
    chain_2_all = models.CharField(max_length=10000, default="")
    chain_3 = models.CharField(max_length=1000, default="")
    chain_3_all = models.CharField(max_length=10000, default="")
    curr_states = models.CharField(max_length=10000, default="") # All current states shown
    proposals = models.CharField(max_length=10000, default="") # All proposals shown

    # Current state fields
    # Experiment Trials
    current_view_left = models.CharField(max_length=1000, default="")
    current_view_right = models.CharField(max_length=1000, default="")
    current_choice = models.CharField(max_length=1, default="")

    # Functions

    def trials_progress(self, steps=12):
        return round(self.trials_stage/steps*100)

    def trials_precision(self, steps=12):
        return round(self.trials_correct/steps*100)


class ExperimentSettingsSet(models.Model):
    version = models.PositiveSmallIntegerField(primary_key=True, default=0) # Just used as a primary key (can be any small integer)
    should_be_used = models.BooleanField(default=False) # Boolean to indicate if the setting should be used during the experiment
    prior_type = models.CharField(max_length=1000, default="") # e.g. expo 2.1, linear, quadratic, expo 1.8
    chain_1 = models.CharField(max_length=1000, default="") # weights for Chain 1, e.g. 1, 0, 0
    chain_2 = models.CharField(max_length=1000, default="")
    chain_3 = models.CharField(max_length=1000, default="")


'''
Quiz classes: questions and choices
'''
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    def __str__(self):
        return self.choice_text