import numpy as np
from rs4 import pathtool
from hashlib import md5
import os
import math
import rs4
import random

class DataSet:
    def __init__ (self, augment = 0, shuffle = False):
        self.data = []
        self.augment = augment
        self.shuffle = shuffle
        self.cache = {}
        self.xs, self.ys = None, None

    def __len__ (self):
        return len (self.data)

    def add (self, row):
        self.data.append (row)

    def get_cache_name (self, path):
        return md5 (path.encode ()).hexdigest () + '.{}.npy'.format (self.augment and 'b' or 'a')

    def get_abs_cache_name (self, path):
        return md5 (path.encode ()).hexdigest () + '.npy'

    def next_indexes (self, size):
        if self.ys is None:
            self.xs, self.ys = self.initiate_data ()
            if self.shuffle:
                self.indexes = np.random.permutation (len (self.data))
            else:
                 self.indexes = range (len (self.data))
            self.current_index = 0

        if not size:
            batch_indexes = self.indexes
        else:
            size = min (size, len (self.data))
            batch_indexes = list (self.indexes [self.current_index:self.current_index + size])
            if len (batch_indexes) < size:
                self.indexes = np.random.permutation (len (self.data))
                self.current_index = size - len (batch_indexes)
                batch_indexes += list (self.indexes [:self.current_index])
            else:
                self.current_index = self.current_index + size
        return batch_indexes

    # override --------------------------------------------
    def initiate_data (self):
        # reconstruct self.data and return xs, ys for iteration
        raise NotImplementedError

    def next_minibatch (self, size = 0):
        batch_indexes = self.next_indexes (size)



