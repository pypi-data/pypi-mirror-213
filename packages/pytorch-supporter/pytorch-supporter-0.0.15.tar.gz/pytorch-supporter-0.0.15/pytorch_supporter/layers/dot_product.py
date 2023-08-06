import torch

#https://en.wikipedia.org/wiki/Dot_product
class DotProduct(torch.nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, user_id, item_id):
        #print(user_id.shape) #torch.Size([1, 1, 100])
        #print(user_id.shape) #torch.Size([1, 1, 100])
        dot_product = (user_id * item_id).sum(2)
        #print(dot_product.shape) #torch.Size([1, 1])
        return dot_product
