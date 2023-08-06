import torch

#Reshape((1, 28, 28))
#Reshape((28 * 28,))
#Reshape((28 * 28))
class Reshape(torch.nn.Module):
    def __init__(self, shape):
        super().__init__()
        self.shape = shape
        if type(self.shape) == int:
            self.shape = [self.shape]

    def forward(self, x):
        return x.view((-1, *self.shape))
