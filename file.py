import random
import ctypes

TEMPLATE_NO = 30
INPUT_NO = 0
OUTPUT_NO = 0
TESTS_NO = 0
MULTIP_LIST = [0.5, 1, 2, 4, 8]

class preset:
    def __init__(self):
        self.depth = random.randint(1, 4) #no layers
        self.height = [] # self.[12, 23, 23]
        self.ponders = []
        self.space = 0
        self.err = 9999

        self.init_adn()
        self.init_ponders()
        self.set_space()

    def init_ponders(self):
        initial_values = []
        for i in range(self.space):
            num = random.uniform(-1.0, 1.0)
            initial_values.append(num)
        type_arr_c = ctypes.c_float * self.space
        self.ponders = type_arr_c(*initial_values)

    def init_adn(self):
        self.height = []
        for i in range(self.depth):
            num = random.randint(0, 4)
            num = int(INPUT_NO * MULTIP_LIST[num])
            if num < 1:
                num = 1
            self.height.append(num)
        print(self.height)

    def set_space(self):
        self.space = 0
        for i in range(self.depth):
            if i == 0:
                self.space += self.height[0] * INPUT_NO
            else:
                self.space += self.height[i] * self.height[i - 1]
        self.space += OUTPUT_NO * self.height[self.depth - 1]
    



def train(input_data, output_data, model_type):
    global INPUT_NO, OUTPUT_NO, TESTS_NO #global data

    INPUT_NO = len(input_data[0])
    OUTPUT_NO = len(output_data[0])
    TESTS_NO = len(input_data)
    presets = [] #adn list
    for i in range(TEMPLATE_NO):
        model = preset()
        presets.append(model)
    


            


def main():
    inpt = []
    outpt = []
    date = []
    date.append(1)
    date.append(3.5)
    date.append(14)
    inpt.append(date)
    date = []
    date.append(3)
    date.append(2)
    date.append(1)
    inpt.append(date)
    date = []
    date.append(1)
    outpt.append(date)
    train(inpt, outpt, "c")

if __name__ == "__main__":
    main()