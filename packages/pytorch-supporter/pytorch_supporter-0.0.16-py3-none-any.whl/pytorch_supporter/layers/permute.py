import torch

class Permute(torch.nn.Module):
    def __init__(self, shape):
        super().__init__()
        self.shape = shape
        

    def forward(self, x):
        x = torch.permute(x, self.shape)
        return x
