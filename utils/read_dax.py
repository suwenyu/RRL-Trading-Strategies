import scipy.io


def read_dax():
    data = []
    f = open('./data/DAX.txt')
    for line in f:
        data.append(line.strip())
    f.close()

    data_ret = []
    f = open('./data/retDax.txt')
    for line in f:
        data_ret.append(line.strip())
    f.close()
    return data, data_ret


def read_twse():
    mat = scipy.io.loadmat('./data/twse_ret.mat')
    data_ret = [i[0] for i in mat['twse_ret']]

    mat = scipy.io.loadmat('./data/twse.mat')
    data = [i[0] for i in mat['twse']]
    return data, data_ret
