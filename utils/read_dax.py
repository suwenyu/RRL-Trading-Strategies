import scipy.io

def read_dax():
    data = []
    f = open('/Users/wenyu/Desktop/reinforment_learning_trading_system/data/Dax.txt')
    for line in f:
        data.append(line.strip())
    f.close()
    return data

def read_twse():
    mat = scipy.io.loadmat('/Users/wenyu/Desktop/reinforment_learning_trading_system/data/twse_ret.mat')
    data = [i[0] for i in mat['twse_ret']]
    return data