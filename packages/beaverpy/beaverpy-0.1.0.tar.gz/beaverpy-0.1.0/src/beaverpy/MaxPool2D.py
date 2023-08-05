#!/usr/bin/env python
# coding: utf-8

import numpy as np

class MaxPool2D:
    ''' Computes maxpool given the input parameters '''
    
    ''' The class implementation will be along the lines of torch.nn.MaxPool2d in order to 
        enable comparison of this NumPy only implementation and seamless testing
    '''
    '''
        TODO:
        * Implement `ceil_mode`
        * Optimizing code
    '''
    
    def __init__(
        self, 
        kernel_size, 
        padding = (0, 0), 
        stride = (1, 1), 
        dilation = (1, 1), 
        return_indices = False,
        ceil_mode = False,
        verbose = False
        ):
        super(MaxPool2D, self).__init__()
        
        ''' mandatory parameters '''
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
        self.return_indices = return_indices
        
        ''' optional parameters (dummy, yet to be implemented)'''
        self.ceil_mode = ceil_mode
        
        ''' additional parameters (different from torch.nn.Conv2D)'''
        self.verbose = verbose
        self.verboseprint = print if self.verbose else lambda *a, **k: None
        self.verboseprint('*** parameters ***')
        self.verboseprint('kernel_size: {}'.format(self.kernel_size))
        self.verboseprint('padding: {}, stride: {}, dilation factor: {}'.format(self.padding, self.stride, self.dilation))
        self.verboseprint('\n')
    
    def forward(self, _input):
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
        if self.padding[0] > self.kernel_size[0] // 2: # as PyTorch mandates this
            raise Exception('invalid input parameters: padding height is larger than half of kernel height')
        if self.padding[1] > self.kernel_size[1] // 2: # as PyTorch mandates this
            raise Exception('invalid input parameters: padding width is larger than half of kernel width')
        
        ''' add zero padding based on the input parameters '''
        if self.padding != (0, 0):
            _input = np.array([[np.pad(channel, ((self.padding[0], self.padding[0]), (self.padding[1], self.padding[1])), 'constant', constant_values = -np.inf) for channel in batch] for batch in _input])    
            self.verboseprint('*** padded input image ***')
            self.verboseprint('input batches: {}, input channels: {}, input height: {}, input weight: {}'.format(_input.shape[0], _input.shape[1], _input.shape[2], _input.shape[3]))
            self.verboseprint(_input)
            self.verboseprint('\n')
        
        ''' use the provided kernels or create random kernels based on the input kernel parameters '''
        kernels = []
        self.verboseprint('*** kernels ***')
        self.verboseprint('kernels: {}, kernel channels: {}, kernel height: {}, kernel weight: {}'.format(_input_c, 1, self.kernel_size[0], self.kernel_size[1]))
        for k in range(_input_c):
            kernel = np.ones((self.kernel_size[0], self.kernel_size[1])) # define a kernel of 1s based on the kernel parameters
            kernels.append(kernel)
            self.verboseprint('kernel {}'.format(k))
            self.verboseprint(kernel)
        self.verboseprint('\n')
            
        ''' dilate a kernel '''
        dil_ker_h = self.dilation[0] * (self.kernel_size[0] - 1) + 1
        dil_ker_w = self.dilation[1] * (self.kernel_size[1] - 1) + 1
        dil_kernels = []
        for kernel in kernels:
            dil_kernel = -np.inf * np.ones((dil_ker_h, dil_ker_w)) # instantiate a dilated kernel of all -np.inf (holes)
            for row in range(len(kernel)):
                for col in range(len(kernel[0])):
                    dil_kernel[self.dilation[0] * row][self.dilation[1] * col] = kernel[row][col]
            dil_kernels.append(dil_kernel.tolist())
        kernels, self.kernel_size = dil_kernels, (dil_ker_h, dil_ker_w)
        self.verboseprint('*** dilated kernels ***')
        self.verboseprint('dilation factor: {}, kernel channels: {}, kernel height: {}, kernel weight: {}'.format(self.dilation, _input_c, self.kernel_size[0], self.kernel_size[1]))
        for k in range(_input_c):
            self.verboseprint('kernel {}'.format(k))
            self.verboseprint(kernels[k])
        self.verboseprint('\n')
        
        ''' compute output volume from the input and kernel parameters '''
        _input_n, _input_c, _input_h, _input_w = _input.shape
        out_n = int(_input_n)
        out_c = int(_input_c)
        out_h = int((_input_h - self.kernel_size[0]) / self.stride[0]) + 1
        out_w = int((_input_w - self.kernel_size[1]) / self.stride[1]) + 1
        output = np.zeros([out_n, out_c, out_h, out_w])
        max_indices = np.zeros([out_n, out_c, out_h, out_w], dtype = int)
        
        ''' parse through every element of the output and compute the convolution value for that element '''
        for b_out in range(out_n):
            for c_out in range(out_c):
                for h_out in range(out_h):
                    for w_out in range(out_w):
                        # convolve kernel over the input slices
                        self.verboseprint('kernel indices, image indices')
                        self.verboseprint('[n, c, h, w]', '[n, c, h, w]')
                        convol_sum = -np.inf
                        max_index = 0
                        ker_h = self.kernel_size[0]
                        ker_w = self.kernel_size[1]
                        for h_ker in range(ker_h):
                            for w_ker in range(ker_w):
                                self.verboseprint([c_out, h_ker, w_ker], [b_out, c_out, h_ker + self.stride[0] * h_out, w_ker + self.stride[1] * w_out])
                                # consider only those input values where there is no 'hole' in the corresponding value of kernel
                                if kernels[c_out][h_ker][w_ker] != -np.inf:
                                    val = kernels[c_out][h_ker][w_ker] * _input[b_out][c_out][h_ker + self.stride[0] * h_out][w_ker + self.stride[1] * w_out]
                                    if val > convol_sum:
                                        convol_sum = val
                                        max_index = (h_ker + self.stride[0] * h_out) * _input_h + (w_ker + self.stride[1] * w_out)
                        self.verboseprint('\n')
                        output[b_out, c_out, h_out, w_out] += convol_sum
                        max_indices[b_out, c_out, h_out, w_out] += max_index
        self.verboseprint('*** MaxPool2D output ***')
        output_shape = output.shape
        self.verboseprint('output batches: {}, ouput channels: {}, output height: {}, output weight: {}'.format(output_shape[0], output_shape[1], output_shape[2], output_shape[3]))
        assert((out_n, out_c, out_h, out_w) == output_shape)
        self.verboseprint(output)
        self.verboseprint('\n')
        if self.return_indices:
            return (output, max_indices)
        return output