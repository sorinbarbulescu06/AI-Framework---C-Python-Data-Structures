import random
import ctypes

TEMPLATE_NO = 32
INPUT_NO = 0
OUTPUT_NO = 0
TESTS_NO = 0
MULTIP_LIST = [0.5, 1, 2, 4, 8]
EXAM_NO = 0
MAX_HIDLAYERS = 4
INPUT_MIN = []
INPUT_MAX = []
OUTPUT_MIN = []
OUTPUT_MAX = []


class preset:
    def __init__(self):
        self.depth = random.randint(1, MAX_HIDLAYERS) #no layers
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
            num = random.uniform(-1.0, 1.0)
            initial_values.append(num)
        type_arr_c = ctypes.c_float * self.space
        self.ponders = type_arr_c(*initial_values)

    def init_adn(self):
        self.height = []
        for i in range(self.depth):
            num = random.randint(0, 4)
            num = int(INPUT_NO * MULTIP_LIST[num])
            num = max(2, num)
            self.height.append(num)

    def set_space(self):
        self.space = 0
        for i in range(self.depth):
            self.space += self.height[i]
            if i == 0:
                self.space += self.height[0] * INPUT_NO
            else:    
                self.space += self.height[i] * self.height[i - 1]   
        self.space += OUTPUT_NO           
        self.space += OUTPUT_NO * self.height[self.depth - 1]
    
def hardcode(presets, existing_adn):
    #hardcode general neural templates
    #funnel
    model = preset()
    model.depth = 3
    if int(INPUT_NO / 2)<= 1:
        num = 2
    else:
        num= int(INPUT_NO / 2)
    model.height = [INPUT_NO * 2, INPUT_NO, num]
    model.set_space()
    model.init_ponders()
    existing_adn.append(model.height)
    presets.append(model)

    #cilinder   
    model = preset()
    model.depth = 3
    model.height = [INPUT_NO * 2, INPUT_NO * 2, INPUT_NO * 2]
    model.set_space()
    model.init_ponders()
    existing_adn.append(model.height)
    presets.append(model)

    #barrell
    model = preset()
    model.depth = 3
    model.height = [INPUT_NO, INPUT_NO * 4, INPUT_NO]
    model.set_space()
    model.init_ponders()
    existing_adn.append(model.height)
    presets.append(model)
    
    #wall
    model = preset()
    model.depth = 1
    model.height = [INPUT_NO * 8]
    model.set_space()
    model.init_ponders()
    existing_adn.append(model.height)
    presets.append(model)

def normalize(input_data, output_data):
    global INPUT_MAX, INPUT_MIN, OUTPUT_MAX, OUTPUT_MIN, INPUT_NO, OUTPUT_NO, TESTS_NO
    for i in range(INPUT_NO):
        minimum = input_data[0][i]
        maximum = input_data[0][i]
        for j in range(TESTS_NO):
            if minimum > input_data[j][i]:
                minimum = input_data[j][i]
            if maximum < input_data[j][i]:
                maximum = input_data[j][i]
        #saving mininum and maximum from the i-th input field
        INPUT_MAX.append(maximum)
        INPUT_MIN.append(minimum)
        #calculating the values normalised
        delta = maximum - minimum
        for j in range(TESTS_NO):
            if delta == 0:
                input_data[j][i] = 0
            else:
                input_data[j][i] = (input_data[j][i] - minimum) / delta

    for i in range(OUTPUT_NO):
        minimum = output_data[0][i]
        maximum = output_data[0][i]
        for j in range(TESTS_NO):
            if minimum > output_data[j][i]:
                minimum = output_data[j][i]
            if maximum < output_data[j][i]:
                maximum = output_data[j][i]
        OUTPUT_MAX.append(maximum)
        OUTPUT_MIN.append(minimum)
        delta = maximum - minimum
        for j in range(TESTS_NO):
            if delta == 0:
                output_data[j][i] = 0
            else:
                output_data[j][i] = (output_data[j][i] - minimum) / delta
            
    


def train(input_data, output_data, model_type):
    global INPUT_NO, OUTPUT_NO, TESTS_NO, EXAM_NO, INPUT_MAX, INPUT_MIN, OUTPUT_MAX, OUTPUT_MIN #global data
   
    #setting global values
    INPUT_NO = len(input_data[0])
    OUTPUT_NO = len(output_data[0])
    TESTS_NO = len(input_data)
    EXAM_NO = int(0.8 * TESTS_NO)

    normalize(input_data, output_data)

    #transform from objects into pointers input and output data
    flat_input = [valoare for rand in input_data for valoare in rand]
    flat_output = [valoare for rand in output_data for valoare in rand]
    flat_input = (ctypes.c_float * len(flat_input))(*flat_input)
    flat_output = (ctypes.c_float * len(flat_output))(*flat_output)

    train_lib = ctypes.CDLL("./brain.so")
    train_lib.train_and_test.argtypes = [
        ctypes.c_int, #INPUT_NO
        ctypes.c_int, #OUTPUT_NO
        ctypes.c_int, #model.depth
        ctypes.c_int, #Epoch
        ctypes.POINTER(ctypes.c_float), #model.ponders
        ctypes.POINTER(ctypes.c_float), #flat_input
        ctypes.POINTER(ctypes.c_float), #flat_output
        ctypes.c_int, #TESTS_NO
        ctypes.POINTER(ctypes.c_int), #model.height
        ctypes.c_char #model_type
    ]
    train_lib.train_and_test.restype = ctypes.c_float

    #initiating presets
    presets = [] #adn list
    existing_adn = []
    hardcode(presets, existing_adn) #first 4 well-know presets
    while len(presets) < TEMPLATE_NO:# the rest of them
        model = preset()
        if model.height not in existing_adn and model.space < 1000000:
            existing_adn.append(model.height)
            presets.append(model)
    
    #first half out - !10 epochs!
    for model in presets:
        point_height = (ctypes.c_int * model.depth)(*model.height)
        train_lib.train_and_test(INPUT_NO, OUTPUT_NO, model.depth, 10, model.ponders, flat_input, flat_output, TESTS_NO, point_height, model_type)
    

    


            


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