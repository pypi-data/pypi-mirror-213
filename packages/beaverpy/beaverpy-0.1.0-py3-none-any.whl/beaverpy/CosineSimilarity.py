import numpy as np

class CosineSimilarity:
    ''' Computes CosineSimilarity Loss given the input1 and input2 '''
    
    ''' * The class implementation will be along the lines of torch.nn.CosineSimilarity in order to 
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
        dim = 1,
        eps = 1e-08,
        verbose = False
        ):
        super(CosineSimilarity, self).__init__()
        
        ''' mandatory parameters '''
        # None
        
        ''' optional parameters '''
        self.dim = dim
        self.eps = eps
        
        ''' optional parameters (dummy, yet to be implemented)'''
        # None
        
        ''' additional parameters (different from torch.nn.Conv2D)'''
        self.verbose = verbose
        self.verboseprint = print if self.verbose else lambda *a, **k: None
        self.verboseprint('*** parameters ***')
        self.verboseprint('dim: {}, eps: {}'.format(self.dim, self.eps))
        self.verboseprint('\n')
    
    def forward(self, _input1, _input2):
        ''' forward pass to compute CosineSimilarity'''
        
        ''' error checking '''
        if not (isinstance(_input1, int) or isinstance(_input1, float) or isinstance(_input1, np.ndarray)):
            raise Exception('invalid input: `input1` should either be an int, a float, or a NumPy ndarray')
        
        if not (isinstance(_input2, int) or isinstance(_input2, float) or isinstance(_input2, np.ndarray)):
            raise Exception('invalid input: `input2` should either be an int, a float, or a NumPy ndarray')
            
        if (isinstance(_input1, np.ndarray) and not isinstance(_input2, np.ndarray))  or (not isinstance(_input1, np.ndarray) and isinstance(_input2, np.ndarray)):
            raise Exception('invalid input: `input1` and `input2` should both be a NumPy ndarray, or can be a mix of `int` and `float`')
        
        if (len(_input1.shape) <= self.dim):
            self.dim = len(_input1.shape) - 1
        
        if (len(_input2.shape) <= self.dim):
            self.dim = len(_input2.shape) - 1
        
        ''' compute CosineSimilarity '''
        dot_product = np.sum(_input1 * _input2, axis = self.dim)
        norm1 = np.sqrt(np.sum(_input1 ** 2, axis = self.dim))
        norm2 = np.sqrt(np.sum(_input2 ** 2, axis = self.dim))
        output = dot_product / (norm1 * norm2)
        self.verboseprint("*** CosineSimilarity output ***")
        self.verboseprint(output)
        self.verboseprint('\n')
        return output