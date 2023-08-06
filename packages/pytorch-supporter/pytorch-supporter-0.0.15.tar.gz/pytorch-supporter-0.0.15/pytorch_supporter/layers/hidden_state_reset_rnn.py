import torch

#이전 시퀀스의 숨은 상태가 다음 시퀀스의 영행을 주기 않게 하기위해 새로운 시퀀스 입력시 이전 숨은 상태 초기화하는 RNN
class HiddenStateResetRNN(torch.nn.Module):
    def __init__(self, input_size, hidden_size, num_layers=1, **kwargs):
        super().__init__()
        self.layer = torch.nn.RNN(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, **kwargs)
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers

    def forward(self, x, **kwargs):
        batch_length = len(x)
        hidden_state = torch.zeros(self.num_layers, batch_length, self.hidden_size)
        print(hidden_state)
        x = self.layer(x, hx=hidden_state, **kwargs)
        return x
