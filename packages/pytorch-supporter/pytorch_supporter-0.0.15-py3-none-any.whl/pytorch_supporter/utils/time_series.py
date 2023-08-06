import numpy as np

#window_length = sequence_length + 1
def slice_time_series_data_from_np_array(np_array, x_column_indexes=None, label_column_indexes=None, sequence_length=7):
    #print(np_array.shape) #(980, 1)
    window_length = sequence_length + 1
    x = []
    labels = []
    for i in range(0, len(np_array) - window_length + 1): #0 ~ (980 - 4 - 1) 
        window = np_array[i:i + window_length, :]
        if x_column_indexes:
            x.append(window[:-1, x_column_indexes])
        else:
            labels.append(window[:-1, :])
        if label_column_indexes:
            labels.append(window[-1, label_column_indexes])
        else:
            labels.append(window[-1, :])
    x = np.array(x)
    labels = np.array(labels)
    #print(x.shape) #(977, 3, 1)
    #print(labels.shape) #(977, 1)
    return x, labels 
