import numpy as np
import random
import binascii
import os
from .models import ExperimentSettingsSet

'''
You can define the number of overall trials here (steps by chains). Note, that models.py has to be updated manually, 
whereas views.py can import step_size correctly.
'''
def step_size(steps=4, chains=3):
    return steps*chains


'''
Functions fun1, fun2 and fun3 define the linear, quadratic and exponential functions that will be weighted to show the proposals.
'''
def fun1(x, b0=-5.41905, b1=5.68953):
    if ExperimentSettingsSet.objects.filter(should_be_used=True).exists():
        exp_set = ExperimentSettingsSet.objects.get(should_be_used=True)
        if exp_set.prior_type.lower() == 'exp 1.8':
            b0 = -1.8288
            b1 = 2.86848
        elif exp_set.prior_type.lower() == 'linear':
            b0 = 5
            b1 = 15
        elif exp_set.prior_type.lower() == 'quadratic':
            b0 = -5
            b1 = 5.5
    return b1*x+b0


def fun2(x, b0=0.07713838, b1=1.16368488):
    if ExperimentSettingsSet.objects.filter(should_be_used=True).exists():
        exp_set = ExperimentSettingsSet.objects.get(should_be_used=True)
        if exp_set.prior_type.lower() == 'exp 1.8':
            b0 = 0.58091163
            b1 = 0.98556279
        elif exp_set.prior_type.lower() == 'linear':
            b0 = 2.90697675
            b1 = 20.6976744
        elif exp_set.prior_type.lower() == 'quadratic':
            b0 = 0.5
            b1 = 1.1
    return b1*x**2+b0


def fun3(x, base=2.1, b0=0):
    if ExperimentSettingsSet.objects.filter(should_be_used=True).exists():
        exp_set = ExperimentSettingsSet.objects.get(should_be_used=True)
        if exp_set.prior_type.lower() == 'exp 1.8':
            b0 = 0
            base = 1.8
        elif exp_set.prior_type.lower() == 'linear':
            b0 = 26
            base = 2.1
        elif exp_set.prior_type.lower() == 'quadratic':
            b0 = 0.47057739
            base = 2.06121332
    return b0+base**x


'''
Extracts an array of float parameters from a string
'''
def get_params(params):
    return list(map(float, params.split(' ')))


'''
Generates the data (y-values) for the prior region (for x in [1, 4]), rounded.
'''
def generate_prior_data(x_start=1, x_end=4):
    x_axis = list(range(x_start, x_end + 1))
    data = list()
    if ExperimentSettingsSet.objects.filter(should_be_used=True).exists():
        exp_set = ExperimentSettingsSet.objects.get(should_be_used=True)
        if exp_set.prior_type.lower() == 'linear':
            for x in x_axis:
                data.append([x, round(fun1(x), 6)])
        elif exp_set.prior_type.lower() == 'quadratic':
            for x in x_axis:
                data.append([x, round(fun2(x), 6)])
        else:
            for x in x_axis:
                data.append([x, round(fun3(x), 6)])
    else:
        for x in x_axis:
            data.append([x, round(fun3(x), 6)])
    return data


'''
Generates the data (y-values) for the prior region (for x in [5, 7]), rounded.
'''
def generate_points(params, x_start=5, x_end=7):
    x_axis = list(range(x_start, x_end+1))
    coefs = get_params(params)
    data = list()
    for x in x_axis:
        data.append([x, round(coefs[0]*fun1(x) + coefs[1]*fun2(x) + coefs[2]*fun3(x), 6)])
    return data



'''
Proposes new weights (here: Uniform, but I've left an option for Normal dist).
'''
def propose(params, max_u = 1.03): #, variances=[0.35, 0.2, 0.08]):
    if ExperimentSettingsSet.objects.filter(should_be_used=True).exists():
        exp_set = ExperimentSettingsSet.objects.get(should_be_used=True)
        if exp_set.prior_type.lower() == 'exp 1.8':
            max_u = 1.5
        elif exp_set.prior_type.lower() == 'linear':
            max_u = 0.15
        elif exp_set.prior_type.lower() == 'quadratic':
            max_u = 1.1
    coefs = get_params(params)
    n_params = np.random.uniform(0, max_u, len(coefs))
    # n_params = n_params / sum(n_params)
    new_params = ""
    for i in range(len(coefs)):
        # new_params += str(np.random.normal(coefs[i], variances[i])) + " "
        new_params += str(round(n_params[i], 6)) + " "
    return new_params[:-1]


'''
Generates the data (y-values) for the prior region (for x in [1, 4]), rounded.
'''
def compare(params_l, params_r, x_start=5, x_end=7):
    coefs_l = get_params(params_l)
    coefs_r = get_params(params_r)
    x = list(range(x_start, x_end + 1))
    dist_l = 0
    dist_r = 0
    if ExperimentSettingsSet.objects.filter(should_be_used=True).exists():
        exp_set = ExperimentSettingsSet.objects.get(should_be_used=True)
        if exp_set.prior_type.lower() == 'linear':
            for i in range(len(x)):
                dist_l += abs(fun1(x[i]) - (coefs_l[0] * fun1(x[i]) + coefs_l[1] * fun2(x[i]) + coefs_l[2] * fun3(x[i])))
                dist_r += abs(fun1(x[i]) - (coefs_r[0] * fun1(x[i]) + coefs_r[1] * fun2(x[i]) + coefs_r[2] * fun3(x[i])))
        elif exp_set.prior_type.lower() == 'quadratic':
            for i in range(len(x)):
                dist_l += abs(fun2(x[i]) - (coefs_l[0] * fun1(x[i]) + coefs_l[1] * fun2(x[i]) + coefs_l[2] * fun3(x[i])))
                dist_r += abs(fun2(x[i]) - (coefs_r[0] * fun1(x[i]) + coefs_r[1] * fun2(x[i]) + coefs_r[2] * fun3(x[i])))
        else:
            for i in range(len(x)):
                dist_l += abs(fun3(x[i]) - (coefs_l[0] * fun1(x[i]) + coefs_l[1] * fun2(x[i]) + coefs_l[2] * fun3(x[i])))
                dist_r += abs(fun3(x[i]) - (coefs_r[0] * fun1(x[i]) + coefs_r[1] * fun2(x[i]) + coefs_r[2] * fun3(x[i])))
    else:
        for i in range(len(x)):
            dist_l += abs(fun3(x[i]) - (coefs_l[0]*fun1(x[i]) + coefs_l[1]*fun2(x[i]) + coefs_l[2]*fun3(x[i])))
            dist_r += abs(fun3(x[i]) - (coefs_r[0]*fun1(x[i]) + coefs_r[1]*fun2(x[i]) + coefs_r[2]*fun3(x[i])))
    if dist_l < dist_r:
        return 'L'
    else:
        return 'R'


'''
Randomly assigns the current state fo the chain to either left graph or right
'''
def generate_prop_placements(steps=step_size()):
    sample = ""
    for s in range(steps):
        sample += random.sample(['L', 'R'], 1)[0] + ", "
    return sample[:-2]


'''
Array to string: for storage in the database
'''
def arr_to_str(array, sep=', '):
    s = ''
    for a in array:
        s += str(a) + sep
    return s[:-2]


'''
Generates a list that states which chain will be shown at each step; makes sure each chain has the same amount of trials 
assigned to it and no chain is shown twice in a row.
'''
def generate_chain_order(steps=step_size()):
    pairs = int(steps/3) - 1
    c = [1, 2, 3]
    sample = arr_to_str(c)
    for p in range(pairs):
        c_old = [c[0], c[1], c[2]]
        np.random.shuffle(c)
        while c[0] == c_old[-1]:
            np.random.shuffle(c)
        sample += ', ' + arr_to_str(c)
    return sample


'''
Generates the unique key for mTurk
'''
def generate_key(length=14):
    length += 3
    key = str(binascii.hexlify(os.urandom(length)))
    return key[2:-1]


'''
Assigns initial chain weights
'''
def assign_chains():
    if ExperimentSettingsSet.objects.filter(should_be_used=True).exists():
        exp_set = ExperimentSettingsSet.objects.get(should_be_used=True)
        return [exp_set.chain_1, exp_set.chain_2, exp_set.chain_3]
    else:
        return ["1 0 0", "0 1 0", "0 0 1"]
