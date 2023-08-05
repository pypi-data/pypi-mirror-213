from py_scripts.src.Conv2D import Conv2D
import numpy as np
import pytest
import torch
from tqdm import tqdm

def valid_params(num_tests):
    ''' generates `num_tests` number of valid input and kernel parameters '''
    
    params_list = []
    sample_count = 0
    while sample_count < num_tests:
        in_channels = np.random.randint(20) + 1 # input channels
        out_channels = np.random.randint(20) + 1 # output channels
        
        kernel_h = np.random.randint(20) + 1
        kernel_w = np.random.randint(20) + 1
        kernel_size = (kernel_h, kernel_w) # kernel size
        
        padding_h = np.random.randint(10) + 1
        padding_w = np.random.randint(10) + 1
        padding = (padding_h, padding_w) # padding (optional)
        stride_h = np.random.randint(5) + 1
        stride_w = np.random.randint(5) + 1
        stride = (stride_h, stride_w) # stride (optional)
        dilation_h = np.random.randint(10) + 1
        dilation_w = np.random.randint(10) + 1
        dilation = (dilation_h, dilation_w) # dilation factor (optional)
        groups = np.random.randint(in_channels) + 1 # groups (optional)
        
        in_batches = np.random.randint(5) + 1 # input batches
        in_h = np.random.randint(30) + 5 # input height
        in_w = np.random.randint(30) + 5 # input weight
    
        ker_h_flag, ker_w_flag, out_h_flag, out_w_flag, in_group_flag, out_group_flag = True, True, True, True, True, True
        
        if in_h + 2 * padding_h < dilation_h * (kernel_h - 1) + 1: # check if (dilated) ker_h is valid
            ker_h_flag = False
        if in_w + 2 * padding_w < dilation_w * (kernel_w - 1) + 1: # check if (dilated) ker_w is valid
            ker_w_flag = False
        if ((in_h + 2 * padding_h - (dilation_h * (kernel_h - 1) + 1)) / stride_h) + 1 < 0: # check if out_h is valid
            out_h_flag = False
        if ((in_w + 2 * padding_w - (dilation_w * (kernel_w - 1) + 1)) / stride_w) + 1 < 0: # check if out_w is valid
            out_w_flag = False
        if  in_channels % groups != 0: # check if groups is valid
            in_group_flag = False
        if out_channels % groups != 0: # check if groups is valid
            out_group_flag = False
        
        if ker_h_flag and ker_w_flag and out_h_flag and out_w_flag and in_group_flag and out_group_flag:
            params_list.append({'in_channels': in_channels, 'out_channels': out_channels, 'kernel_size': kernel_size,
                          'padding': padding, 'stride': stride, 'dilation': dilation, 'groups': groups, 'in_batches': in_batches,
                          'in_h': in_h, 'in_w': in_w})
            sample_count += 1
    return params_list

@pytest.mark.sweep
def test_sweep():
    ''' sweep different input parameters and test by comparing outputs of Conv2D and PyTorch '''
    
    num_tests = 200
    num_passed = 0
    params_list = valid_params(num_tests)
    print('Number of tests: {}\n\n'.format(len(params_list)))

    for i, params in enumerate(tqdm(params_list)):
        print('Test: {}\nParams: {}'.format(i, params))
        in_channels = params['in_channels'] # input channels
        out_channels = params['out_channels'] # output channels
        kernel_size = params['kernel_size'] # kernel size

        padding = params['padding'] # padding (optional)
        stride = params['stride'] # stride (optional)
        dilation = params['dilation'] # dilation factor (optional)
        groups = params['groups'] # groups (optional)

        in_batches = params['in_batches'] # input batches
        in_h = params['in_h'] # input height
        in_w = params['in_w'] # input weight

        _input = np.random.rand(in_batches, in_channels, in_h, in_w) # define a random image based on the input parameters
        kernels = []
        for k in range(out_channels):
            kernel = np.random.rand(int(in_channels / groups), kernel_size[0], kernel_size[1]) # define a random kernel based on the kernel parameters
            kernels.append(kernel)

        try:
            # get Conv2D output with the random inputs
            conv2d = Conv2D(in_channels, out_channels, kernel_size, stride = stride, padding = padding, dilation = dilation, groups = groups) # call an instance of the class with the input parameters 
            _output = conv2d.forward(_input, kernels) # perform convolution

            # get PyTorch output with the same random inputs as above
            x = torch.DoubleTensor(_input)
            weights = torch.stack([torch.DoubleTensor(kernel) for kernel in kernels])
            output = torch.nn.functional.conv2d(x, weights, stride = stride, padding = padding, dilation = dilation, groups = groups)

        except Exception as e:
            print(e)
            print('Result: False\n\n') # treating exception as a failed test
            continue

        # compare outputs of Conv2D and PyTorch
        result = torch.equal(torch.round(torch.DoubleTensor(_output)), torch.round(output)) # need to round the output due to precision difference
        print('Result: {}\n\n'.format(result))
        if result:
            num_passed += 1

    print('{} out of {} ({}%) tests passed'.format(num_passed, num_tests, float(100 * num_passed / num_tests)))