#!/usr/bin/env python
# coding: utf-8

import numpy as np

class Conv2D:
    ''' Computes convolution given the input parameters '''
    
    ''' The class implementation will be along the lines of torch.nn.Conv2d in order to 
        enable comparison of this NumPy only implementation and seamless testing
    '''
    '''
        TODO:
        * Replace `torch.round()` with `np.allclose()` for tests
        * Add `padding = 'same'` mode
        * Optimizing code
    '''
    
    def __init__(
        self, 
        in_channels, 
        out_channels, 
        kernel_size, 
        padding = (0, 0), 
        stride = (1, 1), 
        dilation = (1, 1), 
        groups = 1, 
        bias = True, 
        padding_mode = 'zeros', 
        device = None, 
        dtype = None, 
        verbose = False
        ):
        super(Conv2D, self).__init__()
        
        ''' mandatory parameters '''
        self.in_channels = in_channels
        self.out_channels = out_channels
        if isinstance(kernel_size, tuple):
            self.kernel_size = kernel_size
        elif isinstance(kernel_size, int):
            self.kernel_size = (kernel_size, kernel_size)
        else:
            raise Exception('invalid input parameters: kernel_size should either be an int or a tuple')
        
        ''' optional parameters '''
        if isinstance(padding, str):
            if padding == 'valid':
                self.padding = (0, 0)
            elif padding == 'same':
                raise Exception("invalid input parameters: padding = 'same' not yet supported")
            else:
                raise Exception('invalid input parameters: padding is not valid')
        elif isinstance(padding, tuple):
            if padding[0] >= 0 and padding[1] >= 0:
                self.padding = padding
            else:
                raise Exception('invalid input parameters: padding is not valid')
        elif isinstance(padding, int):
            if padding >= 0:
                self.padding = (padding, padding)
            else:
                raise Exception('invalid input parameters: padding is not valid')
        else:
            raise Exception('invalid input parametersL padding should be either an int or a tuple')
        if isinstance(stride, tuple):
            if stride[0] >= 1 and stride[1] >= 1:
                self.stride = stride
            else:
                raise Exception('invalid input parameters: stride is not valid')
        elif isinstance(stride, int):
            if stride >= 1:
                self.stride = (stride, stride)
            else:
                raise Exception('invalid input parameters: stride is not valid')
        else:
            raise Exception('invalid input parameters: stride should be either an int or a tuple')
        if isinstance(dilation, tuple):
            if dilation[0] >= 1 and dilation[1] >= 1:
                self.dilation = dilation
            else:
                raise Exception('invalid input parameters: dilation is not valid')
        elif isinstance(dilation, int):
            if dilation >= 1:
                self.dilation = (dilation, dilation)
            else:
                raise Exception('invalid input parameters: dilation is not valid')
        else:
            raise Exception('invalid input parameters: dilation should be either an int or a tuple')
        self.groups = groups
        
        ''' optional parameters (dummy, yet to be implemented)'''
        self.bias = bias
        self.padding_mode = padding_mode
        self.device = device
        self.dtype = dtype
        
        ''' additional parameters (different from torch.nn.Conv2D)'''
        self.verbose = verbose
        self.verboseprint = print if self.verbose else lambda *a, **k: None
        self.verboseprint('*** parameters ***')
        self.verboseprint('in_channels: {}, out_channels: {}, kernel_size: {}'.format(self.in_channels, self.out_channels, self.kernel_size))
        self.verboseprint('padding: {}, stride: {}, dilation factor: {}'.format(self.padding, self.stride, self.dilation))
        self.verboseprint('groups: {}, bias: {}, padding_mode: {}, device: {}, dtype: {}'.format(self.groups, self.bias, self.padding_mode, self.device, self.dtype))
        self.verboseprint('\n')
    
    def forward(self, _input, kernels = None):
        ''' forward pass to perform convolution '''
        
        ''' do error checking '''
        _input_n, _input_c, _input_h, _input_w = _input.shape
        if _input_h + 2 * self.padding[0] < self.dilation[0] * (self.kernel_size[0] - 1) + 1: # check if (dilated) ker_h is valid
            raise Exception('invalid input parameters: kernel height is larger than input height')
        if _input_w + 2 * self.padding[1] < self.dilation[1] * (self.kernel_size[1] - 1) + 1: # check if (dilated) ker_w is valid
            raise Exception('invalid input parameters: kernel width is larger than input width')
        if ((_input_h + 2 * self.padding[0] - (self.dilation[0] * (self.kernel_size[0] - 1) + 1)) / self.stride[0]) + 1 < 0: # check if out_h is valid
            raise Exception('invalid input parameters: output height is negative')
        if ((_input_w + 2 * self.padding[1] - (self.dilation[1] * (self.kernel_size[1] - 1) + 1)) / self.stride[1]) + 1 < 0: # check if out_w is valid
            raise Exception('invalid input parameters: output width is negative')
        if  self.in_channels % self.groups != 0: # check if groups is valid
            raise Exception('invalid input parameters: input channels is not divisible by groups')
        if self.out_channels % self.groups != 0: # check if groups is valid
            raise Exception('invalid input parametes: output channels is not divisible by groups')
         
        ''' add zero padding based on the input parameters '''
        if self.padding != (0, 0):
            _input = np.array([[np.pad(channel, ((self.padding[0], self.padding[0]), (self.padding[1], self.padding[1])), 'constant', constant_values = 0) for channel in batch] for batch in _input])    
            self.verboseprint('*** padded input image ***')
            self.verboseprint('input batches: {}, input channels: {}, input height: {}, input weight: {}'.format(_input.shape[0], _input.shape[1], _input.shape[2], _input.shape[3]))
            self.verboseprint(_input)
            self.verboseprint('\n')
        
        ''' use the provided kernels or create random kernels based on the input kernel parameters '''
        if kernels is not None:
            self.verboseprint('*** kernels ***')
            self.verboseprint('kernels: {}, kernel channels: {}, kernel height: {}, kernel weight: {}'.format(self.out_channels, int(self.in_channels / self.groups), self.kernel_size[0], self.kernel_size[1]))
        else:
            kernels = []
            self.verboseprint('*** kernels ***')
            self.verboseprint('kernels: {}, kernel channels: {}, kernel height: {}, kernel weight: {}'.format(self.out_channels, int(self.in_channels / self.groups), self.kernel_size[0], self.kernel_size[1]))
            for k in range(self.out_channels):
                kernel = np.random.rand(int(self.in_channels / self.groups), self.kernel_size[0], self.kernel_size[1]) # define a random kernel based on the kernel parameters
                kernels.append(kernel)
                self.verboseprint('kernel {}'.format(k))
                self.verboseprint(kernel)
            self.verboseprint('\n')
        
        ''' dilate a kernel '''
        dil_ker_h = self.dilation[0] * (self.kernel_size[0] - 1) + 1
        dil_ker_w = self.dilation[1] * (self.kernel_size[1] - 1) + 1
        dil_kernels = []
        for kernel in kernels:
            dil_kernel = []
            for channel in kernel:
                dil_channel = np.zeros((dil_ker_h, dil_ker_w))
                for row in range(len(channel)):
                    for col in range(len(channel[0])):
                        dil_channel[self.dilation[0] * row][self.dilation[1] * col] = channel[row][col] # check if the indices 0 and 1 need to be swapped
                dil_kernel.append(dil_channel.tolist())
            dil_kernels.append(dil_kernel)
        kernels, self.kernel_size = dil_kernels, (dil_ker_h, dil_ker_w)
        self.verboseprint('*** dilated kernels ***')
        self.verboseprint('kernels: {}, dilation factor: {}, kernel channels: {}, kernel height: {}, kernel weight: {}'.format(self.out_channels, self.dilation, int(self.in_channels / self.groups), self.kernel_size[0], self.kernel_size[1]))
        for k in range(self.out_channels):
            self.verboseprint('kernel {}'.format(k))
            self.verboseprint(kernels[k])
        self.verboseprint('\n')
        
        ''' compute output volume from the input and kernel parameters '''
        _input_n, _, _input_h, _input_w = _input.shape
        out_n = int(_input_n)
        out_c = int(self.out_channels)
        out_h = int((_input_h - self.kernel_size[0]) / self.stride[0]) + 1
        out_w = int((_input_w - self.kernel_size[1]) / self.stride[1]) + 1
        output = np.zeros([out_n, out_c, out_h, out_w])
        
        ''' parse through every element of the output and compute the convolution value for that element '''
        for b_out in range(out_n):
            for c_out in range(out_c):
                for h_out in range(out_h):
                    for w_out in range(out_w):
                        # convolve kernel over the input slices
                        self.verboseprint('kernel indices, image indices')
                        self.verboseprint('[n, c, h, w]', '[n, c, h, w]')
                        convol_sum = 0
                        ker_c = int(self.in_channels / self.groups)
                        ker_h = self.kernel_size[0]
                        ker_w = self.kernel_size[1]
                        for c_ker in range(ker_c):
                            for h_ker in range(ker_h):
                                for w_ker in range(ker_w):
                                    self.verboseprint([c_out, c_ker, h_ker, w_ker], [b_out, c_ker + (ker_c * int(np.floor(c_out / (self.out_channels / self.groups)))), h_ker + self.stride[0] * h_out, w_ker + self.stride[1] * w_out])
                                    convol_sum += kernels[c_out][c_ker][h_ker][w_ker] * _input[b_out][c_ker + (ker_c * int(np.floor(c_out / (self.out_channels / self.groups))))][h_ker + self.stride[0] * h_out][w_ker + self.stride[1] * w_out] # works for all 1 <= `groups` <= in_channels
                        self.verboseprint('\n')
                        output[b_out, c_out, h_out, w_out] += convol_sum
        self.verboseprint('*** Conv2D output ***')
        output_shape = output.shape
        self.verboseprint('output batches: {}, ouput channels: {}, output height: {}, output weight: {}'.format(output_shape[0], output_shape[1], output_shape[2], output_shape[3]))
        assert((out_n, out_c, out_h, out_w) == output_shape)
        self.verboseprint(output)
        self.verboseprint('\n')
        return output