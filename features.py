import mdp
import numpy as np


class squared_full(object):
    def __init__(self, normalization=None):
        self.normalization = normalization

    def __call__(self, state):
        a = np.outer(state, state)
        r= np.concatenate((a.flatten(), [1])) 
        if self.normalization is not None:
            assert self.normalization.shape == r.shape
            r /= self.normalization
        return r
    def param_back(self, theta):
        """ transform theta back to P,b """
        if self.normalization is not None:
            theta = theta / self.normalization
        x = theta
        return (x[:-1].reshape(int(np.sqrt(len(x[:-1]))), int(np.sqrt(len(x[:-1])))), x[-1])

    def param_forward(self, P, b):
        """ transform P,b to theta """
        r = np.concatenate((np.array(P).ravel(), [b]))
        if self.normalization is not None:
            r *= self.normalization
        return r

class squared_tri(object):
    def __init__(self, normalization=None):
        self.normalization = normalization

    def __call__(self, state):
        iu1 = np.triu_indices(len(state))
        a = np.outer(state, state)
        a = a* (2-np.eye(len(state)))
        r = np.concatenate((a[iu1], [1]))
        if self.normalization is not None:
            assert self.normalization.shape == r.shape
            r /= self.normalization
        return r
    def param_back(self, theta):
        """ transform theta back to P,b """
        if self.normalization is not None:
            theta = theta / self.normalization
        b = theta[-1]
        p = theta	[:-1]
        l = 1 if len(p) == 1 else (-1 + np.sqrt(1 + 8*len(p)))/2
        iu = np.triu_indices(l)
        il = np.tril_indices(l)
        a = np.empty((l,l))
        a[iu] = p
        a[il] = a.T[il]
        return a, b

    def param_forward(self, P, b):
        """ transform P,b to theta """
        iu1 = np.triu_indices(P.shape[0])
        r = np.concatenate((np.array(P[iu1]).ravel(), [b]))
        if self.normalization is not None:
            r *= self.normalization
        return r
class squared_diag(object):
    def __init__(self, normalization=None):
        self.normalization = normalization

    def __call__(self, state):
        r = state * state
        if self.normalization is not None:
            assert self.normalization.shape == r.shape
            r /= self.normalization
        return r
    def param_back(self, theta):
        """ transform theta back to P,b """
        if self.normalization is not None:
            theta = theta / self.normalization
        return np.diag(theta), 0

    def param_forward(self, P, b):
        """ transform P,b to theta """
        r = np.diag(P)
        if self.normalization is not None:
            r *= self.normalization
        return r