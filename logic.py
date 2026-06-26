import config
import random
import ctypes

#classes

class preset:
    def __init__(self):
        self.depth = random.randint(1, config.MAX_HIDLAYERS) #no layers
        self.height = [] # self.[12, 23, 23]
        self.ponders = []
        self.space = 0
        self.err = 9999

        self.init_adn()
        self.set_space()
        self.init_ponders()

    def init_ponders(self):
        initial_values = []
        for i in range(self.space):
            num = random.uniform(config.W_INIT[0], config.W_INIT[1])
            initial_values.append(num)
        type_arr_c = ctypes.c_float * self.space
        self.ponders = type_arr_c(*initial_values)

    def init_adn(self):
        self.height = []
        for i in range(self.depth):
            num = random.randint(0, 4)
            num = int(config.INPUT_NO * config.MULTIP_LIST[num])
            num = max(2, num)
            self.height.append(num)

    def set_space(self):
        self.space = 0
        for i in range(self.depth):
            self.space += self.height[i]
            if i == 0:
                self.space += self.height[0] * config.INPUT_NO
            else:    
                self.space += self.height[i] * self.height[i - 1]   
        self.space += config.OUTPUT_NO           
        self.space += config.OUTPUT_NO * self.height[self.depth - 1]

#FUNCTIONS

def hardcode(presets, existing_adn):
    #hardcode general neural templates
    #funnel
    model = preset()
    model.depth = 3
    if int(config.INPUT_NO / 2)<= 1:
        num = 2
    else:
        num= int(config.INPUT_NO / 2)
    model.height = [int(config.INPUT_NO * config.MULTIP_LIST[len(config.MULTIP_LIST) - 3]), config.INPUT_NO, num]
    model.set_space()
    model.init_ponders()
    existing_adn.append(model.height)
    presets.append(model)

    #cilinder   
    model = preset()
    model.depth = 3
    model.height = [int(config.INPUT_NO * config.MULTIP_LIST[len(config.MULTIP_LIST) - 3]), int(config.INPUT_NO * config.MULTIP_LIST[len(config.MULTIP_LIST) - 3]), int(config.INPUT_NO * config.MULTIP_LIST[len(config.MULTIP_LIST) - 3])]
    model.set_space()
    model.init_ponders()
    existing_adn.append(model.height)
    presets.append(model)

    #barrell
    model = preset()
    model.depth = 3
    model.height = [config.INPUT_NO, int(config.INPUT_NO * config.MULTIP_LIST[len(config.MULTIP_LIST) - 2]), config.INPUT_NO]
    model.set_space()
    model.init_ponders()
    existing_adn.append(model.height)
    presets.append(model)
    
    #wall
    model = preset()
    model.depth = 1
    model.height = [int(config.INPUT_NO * config.MULTIP_LIST[len(config.MULTIP_LIST) - 1])]
    model.set_space()
    model.init_ponders()
    existing_adn.append(model.height)
    presets.append(model)

def normalize(input_data, output_data, model_type):
    for i in range(config.INPUT_NO):
        minimum = input_data[0][i]
        maximum = input_data[0][i]
        for j in range(config.TESTS_NO):
            if minimum > input_data[j][i]:
                minimum = input_data[j][i]
            if maximum < input_data[j][i]:
                maximum = input_data[j][i]
        #saving mininum and maximum from the i-th input field
        config.INPUT_MAX.append(maximum)
        config.INPUT_MIN.append(minimum)
        #calculating the values normalised
        delta = maximum - minimum
        for j in range(config.TESTS_NO):
            if delta == 0:
                input_data[j][i] = 0
            else:
                input_data[j][i] = (input_data[j][i] - minimum) / delta

    if model_type == "r":
        for i in range(config.OUTPUT_NO):
            minimum = output_data[0][i]
            maximum = output_data[0][i]
            for j in range(config.TESTS_NO):
                if minimum > output_data[j][i]:
                    minimum = output_data[j][i]
                if maximum < output_data[j][i]:
                    maximum = output_data[j][i]
            config.OUTPUT_MAX.append(maximum)
            config.OUTPUT_MIN.append(minimum)
            delta = maximum - minimum
            for j in range(config.TESTS_NO):
                if delta == 0:
                    output_data[j][i] = 0
                else:
                    output_data[j][i] = (output_data[j][i] - minimum) / delta
            
def get_posib(output_data):
    maxim = output_data[0][0]
    for i in range(config.TESTS_NO):
        if maxim < output_data[i][0]:
            maxim = output_data[i][0]
    config.OUTPUT_NO = int(maxim) + 1