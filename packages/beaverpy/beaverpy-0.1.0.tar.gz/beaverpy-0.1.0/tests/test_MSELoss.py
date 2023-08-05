from py_scripts.src.MSELoss import MSELoss
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
        _reduction = np.random.choice(['mean', 'sum', 'none'])
        dimension = np.random.randint(500) + 1 # dimension of the input and target
        _input = np.random.rand(dimension) # define a random input of the above dimension
        _target= np.random.rand(dimension) # define a random target of the above dimension
        print('Test: {}\nDimension : {}, `reduction`: {}'.format(i, dimension, _reduction))
        
        try:
            # compute MSE loss using the random input and target
            mseloss = MSELoss(reduction = _reduction) # call an instance of the class
            _output = mseloss.forward(_input, _target) # compute MSE loss


            # get PyTorch output with the same random inputs as above
            x = torch.DoubleTensor(_input)
            y = torch.DoubleTensor(_target)
            loss = torch.nn.MSELoss(reduction = _reduction)
            output = loss(x, y)

            
        except Exception as e:
            print(e)
            print('Result: False\n\n') # treating exception as a failed test
            continue

        # compare outputs of MSELoss and PyTorch
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