# pytorch-supporter

https://pypi.org/project/pytorch-supporter
<pre>
pip install pytorch-supporter
</pre>

Supported layers

<pre>
import pytorch_supporter

pytorch_supporter.layers.DictToParameters
pytorch_supporter.layers.DotProduct
pytorch_supporter.layers.GRULastHiddenState
pytorch_supporter.layers.HiddenStateResetGRU
pytorch_supporter.layers.HiddenStateResetLSTM
pytorch_supporter.layers.HiddenStateResetRNN
pytorch_supporter.layers.LazilyInitializedLinear
pytorch_supporter.layers.LSTMLastHiddenState
pytorch_supporter.layers.Reshape
pytorch_supporter.layers.RNNLastHiddenState
pytorch_supporter.layers.SelectFromArray
</pre>

Supported utils

<pre>
import pytorch_supporter

text = ''
pytorch_supporter.utils.clean_english(text)
pytorch_supporter.utils.clean_korean(text)
</pre>

Simple time series regression
<pre>
import pytorch_supporter

from sklearn.preprocessing import MinMaxScaler
transformer = MinMaxScaler()
transformer.fit(train_df[['Close']].to_numpy())
train_np_array = transformer.transform(validation_df[['Close']].to_numpy())
#window_length = sequence_length + 1
train_x, train_label = pytorch_supporter.utils.slice_time_series_data_from_np_array(train_np_array, x_column_indexes=[0], label_column_indexes=[0], sequence_length=7)
#print(train_x.shape) #(973, 7, 1)
#print(train_labels.shape) #(973, 1)
#print(validation_x.shape) #(238, 7, 1)
#print(validation_labels.shape) #(238, 1)
</pre>

Multiple time series regression
<pre>
import pytorch_supporter

from sklearn.preprocessing import MinMaxScaler
transformer = MinMaxScaler()
transformer.fit(train_df[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']].to_numpy())
train_np_array = transformer.transform(validation_df[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']].to_numpy())
#window_length = sequence_length + 1
train_x, train_label = pytorch_supporter.utils.slice_time_series_data_from_np_array(train_np_array, x_column_indexes=[0, 1, 2, 3, 4, 5], label_column_indexes=[3], sequence_length=7)
#print(train_x.shape) #(973, 7, 6)
#print(train_labels.shape) #(973, 1)
#print(validation_x.shape) #(238, 7, 6)
#print(validation_labels.shape) #(238, 1)
</pre>
