import torch

class LSTMLastHiddenState(torch.nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x):
        output = x[0] #모든 타임 스텝(토큰: 숫자, 문자, 단어)의 숨은 상태
        hidden_state, cell_state = x[1] #마지막 타임 스텝(토큰: 숫자, 문자, 단어)의 숨은 상태
        #print(output.shape) #torch.Size([8, 380, 32]) 
        #print(hidden_state.shape) #torch.Size([1, 8, 32]) #레이어 수, 타임 스텝, 숨은 상태
        x = output[:,-1]
        #print(x)
        x = hidden_state[-1]
        #print(x)
        #print(x.shape) #torch.Size([8, 32])
        return x
