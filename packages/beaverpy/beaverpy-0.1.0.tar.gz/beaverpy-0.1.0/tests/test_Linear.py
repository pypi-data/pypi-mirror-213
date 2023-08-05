#!/usr/bin/env python
# coding: utf-8

from py_scripts.src.Linear import Linear
import numpy as np
import pytest
import torch
from tqdm import tqdm

def valid_params(num_tests):
    ''' generates `num_tests` number of valid input and kernel parameters '''
    
    params_list = []
    sample_count = 0
    while sample_count < num_tests:
        in_samples = np.random.randint(200)
        in_features = np.random.randint(100) + 1
        out_features = np.random.randint(100) + 1
        params_list.append({'in_samples': in_samples, 'in_features': in_features, 'out_features': out_features})
        sample_count += 1
    return params_list


@pytest.mark.sweep
def test_sweep():
    ''' sweep different input parameters and test by comparing outputs of ReLU and PyTorch '''
    
    num_tests = 1000
    num_passed = 0
    params_list = valid_params(num_tests)
    print('Number of tests: {}\n\n'.format(len(params_list)))

    for i, params in enumerate(tqdm(params_list)):
        print('Test: {}\nParams: {}'.format(i, params))
        in_samples = params['in_samples'] # input samples
        in_features = params['in_features'] # input features
        out_features = params['out_features'] # output features
        
        _input = np.random.rand(in_samples, in_features) # define a random input
        _weights = np.random.rand(out_features, in_features) # define random weights
        _bias = np.random.rand(out_features) # define random bias
        
        try:
            # get Linear output with the random input
            linear = Linear(in_features, out_features) # call an instance of the class with the input parameters
            _output = linear.forward(_input, weights = _weights, bias_weights = _bias) # apply linear transformation

            # get PyTorch output with the same random inputs as above
            x = torch.DoubleTensor(_input)
            A = torch.DoubleTensor(_weights)
            b = torch.DoubleTensor(_bias)
            output = torch.nn.functional.linear(x, A, bias = b)
            
        except Exception as e:
            print(e)
            print('Result: False\n\n') # treating exception as a failed test
            continue

        # compare outputs of Linear and PyTorch
        result = torch.equal(torch.round(torch.DoubleTensor(_output)), torch.round(output)) # need to round the output due to precision difference
        print('Result: {}\n\n'.format(result))
        if result:
            num_passed += 1

    print('{} out of {} ({}%) tests passed'.format(num_passed, num_tests, float(100 * num_passed / num_tests)))
    assert num_passed == num_tests