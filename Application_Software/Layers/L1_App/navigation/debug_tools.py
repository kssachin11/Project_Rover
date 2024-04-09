from math import ceil, log10

import numpy as np


def print_array(a: np.ndarray):    
    l = max(ceil(log10(a.max())), 1)
    
    for aa in a:
        for aaa in aa:
            print(f'{aaa:{l+1}.0f}', end='')
        print()
    print()