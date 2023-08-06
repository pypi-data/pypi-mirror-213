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
        with open(filename, "r") as file:
            data = file.read()
        return data
    else:
        return "Invalid value"
        
practical_data = keras(3)
print(practical_data)