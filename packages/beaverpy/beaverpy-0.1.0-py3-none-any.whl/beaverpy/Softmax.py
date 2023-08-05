#!/usr/bin/env python
# coding: utf-8

import numpy as np

class Softmax:
    ''' Computes Softmax activation given the input '''
    
    ''' * The class implementation will be along the lines of torch.nn.Softmax in order to 
          enable comparison of this NumPy only implementation and seamless testing
        * Can expect extensive refactoring of the existing code in the days to come
        * As part of refactoring, some code will be de-modularized
        * Old code will be retained at the end of the notebook for reference
    '''
    '''
        TODO:
        * Replace `torch.round()` with `np.allclose()` for tests
        * Optimizing code
    '''
    
    def __init__(
        self,
        dim = None,
        verbose = False
        ):
        super(Softmax, self).__init__()
        
        ''' mandatory parameters '''
        # None
        
        ''' optional parameters '''
        self.dim = dim
        
        ''' optional parameters (dummy, yet to be implemented)'''
        # None
        
        ''' additional parameters (different from torch.nn.Conv2D)'''
        self.verbose = verbose
        self.verboseprint = print if self.verbose else lambda *a, **k: None
        self.verboseprint('*** parameters ***')
        self.verboseprint('dim: {},'.format(self.dim))
        self.verboseprint('\n')
    
    def forward(self, _input):
        ''' forward pass to perform Softmax activation '''
        
        ''' error checking '''
        if not (isinstance(_input, int) or isinstance(_input, float) or isinstance(_input, np.ndarray)):
            raise Exception('invalid input: input should either be an int, a float, or a NumPy ndarray')
        
        if self.dim is None:
            self.dim = -1
            
        ''' compute Softmax activation '''
        output = np.exp(_input) / np.sum(np.exp(_input), axis = self.dim, keepdims = True)
        self.verboseprint(output)
        self.verboseprint('\n')
        return output