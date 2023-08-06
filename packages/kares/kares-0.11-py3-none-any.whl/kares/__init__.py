import os

def keras(val):
    pracs = {
        1:"Practical_1.txt",
        2:"Practical_2.txt",
        3:"Practical_3.txt",
        4:"Practical_4.txt",
        5:"Practical_5.txt",
        6:"Practical_6.txt",
        7:"Practical_7.txt",
        8:"Practical_8.txt",
        9:"Practical_9.txt"
    }

    filename = pracs.get(val)
    if filename is not None:
        module_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(module_path, filename)
        with open(file_path, "r") as file:
            data = file.read()
        return data
    else:
        return "Invalid value"

def numpy():
    pracs = {
        1:"Feed Forward",
        2:"Regularization for Overfitting",
        3:"Recognition of classes for CIFAR10",
        4:"Autoencoder",
        5:"CNN for digit recog on MNIST dataset",
        6:"Transfer learning",
        7:"GAN",
        8:"a. RNN b. LSTM",
        9:"Obj Detection"
    }

    for i in pracs:
        print(i,pracs[i])