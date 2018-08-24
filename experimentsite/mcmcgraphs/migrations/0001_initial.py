# Generated by Django 2.0.2 on 2018-08-22 15:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('correct', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ExperimentSettings',
            fields=[
                ('version', models.PositiveSmallIntegerField(default=0, primary_key=True, serialize=False)),
                ('should_be_used', models.BooleanField(default=False)),
                ('prior_type', models.CharField(default='', max_length=1000)),
                ('chain_1', models.CharField(default='', max_length=1000)),
                ('chain_2', models.CharField(default='', max_length=1000)),
                ('chain_3', models.CharField(default='', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('session_id', models.CharField(max_length=1000, primary_key=True, serialize=False)),
                ('session_start', models.DateTimeField(default=django.utils.timezone.now)),
                ('amt_id', models.CharField(default='', max_length=1000)),
                ('terms_accepted', models.BooleanField(default=False)),
                ('time_start', models.DateTimeField(default=django.utils.timezone.now)),
                ('time_end', models.DateTimeField(default=django.utils.timezone.now)),
                ('unique_code', models.CharField(default='', max_length=1000)),
                ('prior', models.CharField(default='', max_length=1000)),
                ('weights', models.CharField(default='', max_length=1000)),
                ('quiz_completed', models.BooleanField(default=False)),
                ('quiz_runs', models.PositiveSmallIntegerField(default=0)),
                ('trials_stage', models.PositiveSmallIntegerField(default=0)),
                ('trials_correct', models.PositiveSmallIntegerField(default=0)),
                ('choices', models.CharField(default='', max_length=1000)),
                ('choice_datetime', models.CharField(default='', max_length=20000)),
                ('curr_state_place', models.CharField(default='', max_length=1000)),
                ('chain_shown', models.CharField(default='', max_length=1000)),
                ('chain_1', models.CharField(default='', max_length=1000)),
                ('chain_1_all', models.CharField(default='', max_length=10000)),
                ('chain_2', models.CharField(default='', max_length=1000)),
                ('chain_2_all', models.CharField(default='', max_length=10000)),
                ('chain_3', models.CharField(default='', max_length=1000)),
                ('chain_3_all', models.CharField(default='', max_length=10000)),
                ('curr_states', models.CharField(default='', max_length=10000)),
                ('proposals', models.CharField(default='', max_length=10000)),
                ('current_view_left', models.CharField(default='', max_length=1000)),
                ('current_view_right', models.CharField(default='', max_length=1000)),
                ('current_choice', models.CharField(default='', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcmcgraphs.Question'),
        ),
    ]
