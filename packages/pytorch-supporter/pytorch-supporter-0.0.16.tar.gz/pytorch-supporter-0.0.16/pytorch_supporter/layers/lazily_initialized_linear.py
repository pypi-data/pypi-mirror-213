import torch

class LazilyInitializedLinear(torch.nn.Module):
    def __init__(self, out_features):
        super().__init__()
        self.layer = None
        self.out_features = out_features

    def forward(self, x):
        if not self.layer:
            in_features = x.shape[1]
            self.layer = torch.nn.Linear(in_features=in_features, out_features=self.out_features)
            device = "cpu"
            if torch.cuda.is_available():
                device = "cuda"
            elif torch.backends.mps.is_available():
                device = "mps"
            self.layer = self.layer.to(device)
        x = self.layer(x)
        return x
