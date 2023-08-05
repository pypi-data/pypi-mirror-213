from py_scripts.src.Sigmoid import Sigmoid
import numpy as np
import pytest
import torch
from tqdm import tqdm

@pytest.mark.sweep
def test_sweep():
    ''' sweep different input parameters and test by comparing outputs of Sigmoid and PyTorch '''
    
    num_tests = 1000
    num_passed = 0
    print('Number of tests: {}\n\n'.format(num_tests))
    
    for i in tqdm(range(num_tests)):
        num_dim = np.random.randint(6) + 1 # number of input dimensions
        dim = tuple(np.random.randint(5) + 1 for _ in range(num_dim)) # shape of input
        _input = np.random.rand(*dim) # generate an input based on the dimensions and shape
        print('Test: {}\nInput shape: {}'.format(i, dim))
        
        try:
            # get Sigmoid output with the random input
            sigmoid = Sigmoid(_input) # call an instance of the class with the input
            _output = sigmoid.forward(_input) # perform Sigmoid activation

            # get PyTorch output with the same random input as above
            x = torch.DoubleTensor(_input)
            m = torch.nn.Sigmoid()
            output = m(x)
            
        except Exception as e:
            print(e)
            print('Result: False\n\n') # treating exception as a failed test
            continue

        # compare outputs of Sigmoid and PyTorch
        result = torch.equal(torch.round(torch.DoubleTensor(_output)), torch.round(output)) # need to round the output due to precision difference
        print('Result: {}\n\n'.format(result))
        if result:
            num_passed += 1

    print('{} out of {} ({}%) tests passed'.format(num_passed, num_tests, float(100 * num_passed / num_tests)))
    assert num_passed == num_tests



