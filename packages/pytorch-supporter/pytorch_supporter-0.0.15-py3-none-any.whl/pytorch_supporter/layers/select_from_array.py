import torch

class SelectFromArray(torch.nn.Module):
    def __init__(self, index=0):
        super().__init__()
        self.index = index

    def forward(self, x):
        return x[self.index]
