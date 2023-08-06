import numpy
import numpy as np
import pandas as pd
from tqdm import tqdm


def Call_Payoff(trajektoria,K):
    return (np.maximum(trajektoria-K,0))

def Put_Payoff(trajektoria,K):
    return (np.maximum(K-trajektoria,0))

def Double_Call_Payoff(sims_list, K1, K2):
    return (np.maximum(sims_list[0] - K1, 0) + np.maximum(sims_list[1] - K2, 0))

def double_max_put(sims_list, K):
    return np.maximum(np.maximum(K - sims_list[0], K - sims_list[1]), 0)


def payoff_creator_1d(paths, payoff_func, path_dependent=False, pd_type='asian', barrier=False, barrier_level=0,
                      barrier_type='up-and-out', *args, **kwargs):

    '''
    Creates various payoffs for one dimensional derivatives, depending on specified type of option and payoff function.

    :param paths: Generated trajectories for which we want to create a payoff in each timestep,
                    each row of n array is a new trajectory
    :type paths: array
    :param payoff_func: Function we want to use as payoff, taking paths as an argument and possibly other arguments
    :type payoff_func: function
    :param path_dependent: If option is path dependent, it means that payoff depends on the whole (or some part)
    of the underlying price process
    :type path_dependent: bool
    :param pd_type: What kind of path dependency, possible choices: 'asian'(asian_geom): (geometric) mean of underlying,
    'asian_strike'('asian_strike_geom'): strike is a (geometric) mean value of underlying,
    'lookback_min': min value of underlying, 'lookback_max': max value of underlying,
    :type pd_type: str
    :param barrier: If option has a barrier
    :type barrier: bool
    :param barrier_level: Level of a barrier
    :type barrier_level: float
    :param barrier_type: Type of barrier, possible choices: 'up-and-out', 'down-and-out', 'up-and-in', 'down-and-in'
    :type barrier_type: str
    :return: Payoffs for an option type
    :rtype: numpy array
    '''

    if type(paths) != numpy.ndarray:
        paths = paths.to_numpy()

    if barrier:
        if barrier_level == 0:
            raise Exception('Please specify barrier level')

        if barrier_type[:2] == 'up':
            arr = paths >= barrier_level
        elif barrier_type[:4] == 'down':
            arr = paths <= barrier_level

        # if there is no true value(path wont touch the barrier) argmax will return first false index -->0
        # as we cannot start being out of barrier I will take zeros as paths when we havent touched the barrier

        indexes = np.argmax(arr, axis=1)
        affected = np.where(indexes != 0)

    if path_dependent:
        if pd_type == 'asian':
            paths = np.cumsum(paths, axis=1) / np.arange(1, len(paths[0]) + 1)
        elif pd_type == 'asian_geom':
            paths = np.cumprod(paths, axis=1) ** (1 / np.arange(1, len(paths[0]) + 1))
        elif pd_type == 'asian_strike':
            K = np.cumsum(paths, axis=1) / np.arange(1, len(paths[0]) + 1)
        elif pd_type == 'asian_strike_geom':
            K = np.cumprod(paths, axis=1) ** (1 / np.arange(1, len(paths[0]) + 1))
        # look-back options - min/max of path
        elif pd_type == 'lookback_max':
            paths = np.maximum.accumulate(paths, axis=1)
        elif pd_type == 'lookback_min':
            paths = np.minimum.accumulate(paths, axis=1)

    payoffs = payoff_func(paths, *args, **kwargs)

    if barrier:
        if barrier_type[-3:] == 'out':
            for i in affected[0]:
                # print(i)
                # print(indexes[i])
                payoffs[i, indexes[i]:] = 0
            # payoffs[affected[0], indexes[affected[0]]:] = 0
            # print(affected[0][0])

        elif barrier_type[-2:] == 'in':
            payoffs_c = np.zeros(payoffs.shape)
            for i in affected[0]:
                # print(i)
                # print(indexes[i])
                payoffs_c[i, indexes[i]:] = payoffs[i, indexes[i]:]
            # payoffs[affected, :indexes[affected]] = 0
            # payoffs[-affected, :] = 0
            payoffs = payoffs_c

    return payoffs



