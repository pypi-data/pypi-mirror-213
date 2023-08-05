from py_scripts.src.CosineSimilarity import CosineSimilarity
import numpy as np
import pytest
import torch
from tqdm import tqdm

@pytest.mark.sweep
def test_sweep():
    ''' sweep different input parameters and test by comparing outputs of ReLU and PyTorch '''
    
    num_tests = 10000
    num_passed = 0
    print('Number of tests: {}\n\n'.format(num_tests))
    
    for i in tqdm(range(num_tests)):
        num_dim = np.random.randint(6) + 1 # number of input dimensions
        shape = tuple(np.random.randint(5) + 1 for _ in range(num_dim)) # shape of input
        _input1 = np.random.rand(*shape) # generate an input based on the dimensions and shape
        _input2 = np.random.rand(*shape) # generate another input based on the dimensions and shape
        _dim = np.random.randint(num_dim) # dimension along which CosineSimilarity is to be computed
        _eps = np.random.uniform(low = 1e-10, high = 1e-6)
        print('Test: {}\nInput shape: {}, Dimension: {}, eps: {}'.format(i, shape, _dim, _eps))
        
        try:
            # compute CosineSimilarity using the random input and target
            cosinesimilarity = CosineSimilarity(dim = _dim, eps = _eps) # call an instance of the class
            _output = cosinesimilarity.forward(_input1, _input2) # compute CosineSimilarity

            # get PyTorch output with the same random inputs as above
            x = torch.DoubleTensor(_input1)
            y = torch.DoubleTensor(_input2)
            loss = torch.nn.CosineSimilarity(dim = _dim, eps = _eps)
            output = loss(x, y)

            
        except Exception as e:
            print(e)
            print('Result: False\n\n') # treating exception as a failed test
            continue

        # compare outputs of CosineSimilarity and PyTorch
        if not isinstance(_output, np.ndarray): # if a singleton, convert PyTorch tensor to NumPy float, round, and compare
            output = output.numpy()
            result = np.equal(np.round(_output), np.round(output)) 
        else:
            result = torch.equal(torch.round(torch.DoubleTensor(_output)), torch.round(output)) # need to round the output due to precision difference
        print('Result: {}\n\n'.format(result))
        if result:
            num_passed += 1

    print('{} out of {} ({}%) tests passed'.format(num_passed, num_tests, float(100 * num_passed / num_tests)))
    assert num_passed == num_tests