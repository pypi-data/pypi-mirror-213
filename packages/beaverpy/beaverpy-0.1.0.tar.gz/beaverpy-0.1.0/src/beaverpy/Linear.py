#!/usr/bin/env python
# coding: utf-8

import numpy as np

class Linear:
    ''' Applies a linear transformation given the input '''
    
    ''' * The class implementation will be along the lines of torch.nn.Linear in order to 
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
        in_features,
        out_features,
        bias = True,
        device = None,
        dtype = None,
        verbose = False
        ):
        super(Linear, self).__init__()
        
        ''' mandatory parameters '''
        self.in_features = in_features
        self.out_features = out_features
        
        ''' optional parameters '''
        # None
        
        ''' optional parameters (dummy, yet to be implemented)'''
        self.bias = bias
        self.device = device
        self.dtype = dtype
        
        ''' additional parameters (different from torch.nn.Conv2D)'''
        self.verbose = verbose
        self.verboseprint = print if self.verbose else lambda *a, **k: None
        self.verboseprint('*** parameters ***')
        self.verboseprint('in_features: {}, out_features: {}, bias: {}'.format(self.in_features, self.out_features, self.bias))
        self.verboseprint('device: {}, dtype: {}'.format(self.device, self.dtype))
        self.verboseprint('\n')
    
    def forward(self, _input, weights = None, bias_weights = None):
        ''' forward pass to perform a linear transformation '''
        
        ''' error checking '''
        if not (isinstance(_input, int) or isinstance(_input, float) or isinstance(_input, np.ndarray)):
            raise Exception('invalid input: input should either be an int, a float, or a NumPy ndarray')
        
        ''' use the provided weights or create random weights based on the input parameters '''
        if weights is not None:
            self.verboseprint('*** weights ***')
            self.verboseprint('weights shape: {}'.format(weights.shape))
        else:
            weights = np.random.rand(self.out_features, self.in_features)
        self.verboseprint(weights)
        self.verboseprint('\n')                      
                              
        if self.bias:
            if bias_weights is not None:
                self.verboseprint('*** bias ***')
                self.verboseprint('bias shape: {}'.format(bias_weights.shape))
            else:
                bias_weights = np.random.rand(self.out_features)
                self.verboseprint('*** bias ***')
                self.verboseprint('bias shape: {}'.format(bias_weights.shape))
        else:
            bias_weights = np.zeroes(self.out_features)
        self.verboseprint(bias_weights)
        self.verboseprint('\n')
                              
        ''' apply linear transformation '''
        output = _input @ weights.T + bias_weights
        self.verboseprint(output)
        self.verboseprint('\n')
        return output