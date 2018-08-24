from django.contrib import admin
from .models import Participant, ExperimentSettingsSet, Choice, Question
from django.http import HttpResponse
import csv
from django.utils.encoding import smart_str
from django.utils import timezone, dateformat


'''
Defines what is exported in the csv file
'''
def export_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=participants_report'+dateformat.format(timezone.now(), "Y-m-d H:i:s")+'.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u'session_id'),
        smart_str(u'session_start'),
        smart_str(u'amt_id'),
        smart_str(u'terms_accepted'),
        smart_str(u'time_start'),
        smart_str(u'time_end'),
        smart_str(u'unique_code'),
        smart_str(u'quiz_completed'),
        smart_str(u'quiz_runs'),
        smart_str(u'prior'),
        smart_str(u'weights'),
        smart_str(u'chain_1'),
        smart_str(u'chain_2'),
        smart_str(u'chain_3'),
        smart_str(u'trials_stage'),
        smart_str(u'trials_correct'),
        smart_str(u'chain_1_all'),
        smart_str(u'chain_2_all'),
        smart_str(u'chain_3_all'),
        smart_str(u'curr_states'),
        smart_str(u'curr_state_place'),
        smart_str(u'proposals'),
        smart_str(u'choices'),
        smart_str(u'choice_datetime'),
        smart_str(u'chain_shown')
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.session_start),
            smart_str(obj.amt_id),
            smart_str(obj.terms_accepted),
            smart_str(obj.time_start),
            smart_str(obj.time_end),
            smart_str(obj.unique_code),
            smart_str(obj.quiz_completed),
            smart_str(obj.quiz_runs),
            smart_str(obj.prior),
            smart_str(obj.weights),
            smart_str(obj.chain_1),
            smart_str(obj.chain_2),
            smart_str(obj.chain_3),
            smart_str(obj.trials_stage),
            smart_str(obj.trials_correct),
            smart_str(obj.chain_1_all),
            smart_str(obj.chain_2_all),
            smart_str(obj.chain_3_all),
            smart_str(obj.curr_states),
            smart_str(obj.curr_state_place),
            smart_str(obj.proposals),
            smart_str(obj.choices),
            smart_str(obj.choice_datetime),
            smart_str(obj.chain_shown)
        ])
    return response
export_csv.short_description = u"Export CSV"


'''
Models that will be shown in the admi interface (under MCMCGRAPHS)
'''
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('session_id',
                    'session_start',
                    'amt_id',
                    'terms_accepted',
                    'time_start',
                    'time_end',
                    'unique_code',
                    'quiz_completed',
                    'quiz_runs',
                    'prior',
                    'weights',
                    'chain_1',
                    'chain_2',
                    'chain_3',
                    'trials_stage',
                    'trials_correct')
    actions = [export_csv]


class ExperimentSettingsSetAdmin(admin.ModelAdmin):
    list_display = ('version',
                    'should_be_used',
                    'prior_type',
                    'chain_1',
                    'chain_2',
                    'chain_3')



class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


'''
Registering the models
'''
admin.site.register(Question, QuestionAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(ExperimentSettingsSet, ExperimentSettingsSetAdmin)
