from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone, dateformat
from .models import Participant, ExperimentSettingsSet, Question
from .utils import generate_points, propose, compare, generate_prop_placements, \
    generate_chain_order, assign_chains, generate_key, generate_prior_data, step_size

'''
Shows the information sheet/consent form page
'''
def index(request):
    if not request.session.session_key:
        return render(request, 'mcmcgraphs/no_session_id.html')
    else:
        return render(request, 'mcmcgraphs/index.html')


'''
Gets the Amazon mTurk id from the url
'''
def catch_amt(request):
    amt_id = request.GET.get('amt', '')
    if amt_id == '':
        return render(request, 'mcmcgraphs/no_session_id.html')
    elif Participant.objects.filter(amt_id=amt_id).exists():
        # If participant already exisits in the data base
        amt_worker = get_object_or_404(Participant, amt_id=amt_id)
        if amt_worker.unique_code == "" or amt_worker.unique_code == "debug":
            # If the user has not completed the experiment yet, or in case of debugging - create a new session
            request.session.create()
            request.session.save()
            previous_ssid = amt_worker.session_id
            amt_worker.session_id = request.session.session_key
            amt_worker.session_start = timezone.now()
            amt_worker.save()
            Participant.objects.filter(pk=previous_ssid).delete()
            return HttpResponseRedirect(reverse('mcmcgraphs:instructions'))
        else:
            # Return the repeated participation page
            return render(request, 'mcmcgraphs/repeated.html', {'participant': amt_worker})
    else:
        # Create a new entry
        request.session.create()
        request.session.save()
        ssid = request.session.session_key
        amt_worker = Participant(session_id=ssid,
                                 session_start=timezone.now(),
                                 amt_id=amt_id,
                                 time_start=timezone.now())
        amt_worker.save()
        return HttpResponseRedirect(reverse('mcmcgraphs:index'))


'''
Show the instructions
'''
def show_instructions(request):
    if not request.session.session_key:
        return render(request, 'mcmcgraphs/no_session_id.html')
    else:
        data_show = generate_prior_data()
        return render(request, 'mcmcgraphs/instructions.html', {'dataShow': data_show})


'''
Pre-processes the request before showing the instructions
'''
@ensure_csrf_cookie
def instructions(request):
    if request.method == 'POST':
        if request.session.session_key:
            amt_worker = get_object_or_404(Participant, pk=request.session.session_key)
            if not amt_worker.terms_accepted and request.POST['terms'] == 'True':
                # If terms are accepted
                amt_worker.terms_accepted = True
                chains = assign_chains()
                amt_worker.curr_state_place = generate_prop_placements()
                # Check if there are any settings pre-defined, if not - return the default (exponential with base 2.1)
                if ExperimentSettingsSet.objects.filter(should_be_used=True).exists():
                    exp_set = ExperimentSettingsSet.objects.get(should_be_used=True)
                    amt_worker.prior = exp_set.prior_type.lower() # linear, quadratic, exp 1.8, exp 2.1 (default)
                else:
                    amt_worker.prior = 'exp 2.1'
                amt_worker.chain_shown = generate_chain_order()
                amt_worker.chain_1 = chains[0]
                amt_worker.chain_1_all = chains[0]
                amt_worker.chain_2 = chains[1]
                amt_worker.chain_2_all += chains[1]
                amt_worker.chain_3 = chains[2]
                amt_worker.chain_3_all += chains[2]
                amt_worker.weights = str(chains[0])+', '+str(chains[1])+', '+str(chains[2])
                amt_worker.save()
    return HttpResponseRedirect(reverse('mcmcgraphs:show_instructions'))


'''
Shows the trials or the pre-trials quiz
'''
def show_trials(request):
    if not request.session.session_key:
        return render(request, 'mcmcgraphs/no_session_id.html')
    else:
        amt_worker = get_object_or_404(Participant, pk=request.session.session_key)
        if amt_worker.quiz_completed:
            # If the participant has completed the quiz successfully
            if amt_worker.trials_stage < step_size():
                # If the experiment is not finished yet
                data_left = generate_points(amt_worker.current_view_left)
                data_right = generate_points(amt_worker.current_view_right)
                data_prior = generate_prior_data()
                return render(request, 'mcmcgraphs/trials.html', {'participant': amt_worker,
                                                                  'dataPrior': data_prior,
                                                                  'dataLeft': data_left,
                                                                  'dataRight': data_right})
            else:
                # If the experiment has been finished
                return render(request, 'mcmcgraphs/trials_completed.html', {'participant': amt_worker})
        else:
            # Show the quiz or a quiz fail page
            if amt_worker.quiz_runs < 3:
                question1 = get_object_or_404(Question, pk=1)
                question2 = get_object_or_404(Question, pk=2)
                question3 = get_object_or_404(Question, pk=3)
                if amt_worker.quiz_runs == 0:
                    return render(request, 'mcmcgraphs/trials_pre_quiz.html', {'questions': [question1,
                                                                                                question2,
                                                                                                question3]})
                else:
                    return render(request, 'mcmcgraphs/trials_pre_quiz.html', {
                                    'questions': [question1, question2, question3],
                                    'error_message': "You have answered at least one question incorrectly. Please re-read the instructions and try again. You have "+str(3-amt_worker.quiz_runs)+" out of 3 attempts left.",
                                })
            else:
                return render(request, 'mcmcgraphs/trials_pre_quiz_fail.html')


'''
Pre-processes the request before showing trials/quiz
'''
@ensure_csrf_cookie
def trials(request):
    if not request.session.session_key:
        return render(request, 'mcmcgraphs/no_session_id.html')
    else:
        amt_worker = get_object_or_404(Participant, pk=request.session.session_key)
        if request.method == 'POST':
            if request.POST['submit'] == 'Next':
                # Record participant's response
                stage = amt_worker.trials_stage
                cur_chain = amt_worker.chain_shown[stage + stage * 2]  # i.e. 1, 2 or 3
                choice = request.POST['chosenGraph']
                if choice == 'L':
                    update_chain = amt_worker.current_view_left
                else:
                    update_chain = amt_worker.current_view_right
                if cur_chain == '1':
                    amt_worker.chain_1 = update_chain
                    amt_worker.chain_1_all += ', ' + update_chain
                if cur_chain == '2':
                    amt_worker.chain_2 = update_chain
                    amt_worker.chain_2_all += ', ' + update_chain
                if cur_chain == '3':
                    amt_worker.chain_3 = update_chain
                    amt_worker.chain_3_all += ', ' + update_chain
                amt_worker.current_choice = choice
                amt_worker.choices += choice + ', '
                amt_worker.choice_datetime += dateformat.format(timezone.now(), "Y-m-d H:i:s") + ', '
                correct_choice = compare(amt_worker.current_view_left, amt_worker.current_view_right)
                if choice == correct_choice:
                    amt_worker.trials_correct += 1
                amt_worker.trials_stage += 1
                amt_worker.save()
        stage = amt_worker.trials_stage
        if stage < step_size():
            cur_position = amt_worker.curr_state_place[stage + stage * 2]  # i.e. L or R
            cur_chain = amt_worker.chain_shown[stage + stage * 2]  # i.e. 1, 2 or 3
            if cur_chain == '1':
                cur_state = amt_worker.chain_1
            if cur_chain == '2':
                cur_state = amt_worker.chain_2
            if cur_chain == '3':
                cur_state = amt_worker.chain_3
            cur_proposal = propose(cur_state)
            if cur_position == 'L':
                params_l = cur_state
                params_r = cur_proposal
            else:
                params_r = cur_state
                params_l = cur_proposal
            amt_worker.curr_states += cur_state + ', '
            amt_worker.proposals += cur_proposal + ', '
            amt_worker.current_view_left = params_l
            amt_worker.current_view_right = params_r
            amt_worker.save()
        else:
            if request.method == 'POST':
                if request.POST['submit'] == 'Next':
                    amt_worker.time_end = timezone.now()
                    amt_worker.unique_code = generate_key()
                    amt_worker.save()
        return HttpResponseRedirect(reverse('mcmcgraphs:show_trials'))


'''
Defines the page to show for 404 error
'''
def error404(request):
    return HttpResponse(render(request, 'mcmcgraphs/no_session_id.html'), status=404)


'''
Defines the page to show for 500 error
'''
def error500(request):
    return HttpResponse(render(request, 'mcmcgraphs/no_session_id.html'), status=500)


'''
Submits the quiz response and redirects the user
'''
@ensure_csrf_cookie
def vote(request):
    question1 = get_object_or_404(Question, pk=1)
    question2 = get_object_or_404(Question, pk=2)
    question3 = get_object_or_404(Question, pk=3)
    amt_worker = get_object_or_404(Participant, pk=request.session.session_key)

    if request.method == "POST":
        amt_worker.quiz_runs += 1
        amt_worker.save()
        choices_str = request.POST['choices']
        choice_ids = choices_str.split(',')
        selected_choice1 = question1.choice_set.get(pk=int(choice_ids[0]))
        selected_choice2 = question2.choice_set.get(pk=int(choice_ids[1]))
        selected_choice3 = question3.choice_set.get(pk=int(choice_ids[2]))

    if selected_choice1.correct and selected_choice2.correct and selected_choice3.correct:
        amt_worker.quiz_completed = True
        amt_worker.save()
        return HttpResponseRedirect(reverse('mcmcgraphs:show_trials'))
    else:
        if amt_worker.quiz_runs >= 3:
            amt_worker.time_end = timezone.now()
            amt_worker.unique_code = 'Quiz failed'
            amt_worker.save()
        return HttpResponseRedirect(reverse('mcmcgraphs:show_trials'))
