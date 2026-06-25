import ctypes
import config
import logic


def train(input_data, output_data, model_type):
    #setting global values
    config.INPUT_NO = len(input_data[0])
    config.TESTS_NO = len(input_data)
    if model_type == "r":
        config.OUTPUT_NO = len(output_data[0])
    else:
        logic.get_posib(output_data)
    config.EXAM_NO = int(0.8 * config.TESTS_NO)

    logic.normalize(input_data, output_data, model_type)

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
    logic.hardcode(presets, existing_adn) #first 4 well-know presets
    while len(presets) < config.TEMPLATE_NO:# the rest of them
        model = logic.preset()
        if model.height not in existing_adn and model.space < 1000000:
            existing_adn.append(model.height)
            presets.append(model)
    
    #first training - !10 epochs!
    for model in presets:
        point_height = (ctypes.c_int * model.depth)(*model.height)
        train_lib.train_and_test(config.INPUT_NO, config.OUTPUT_NO, model.depth, 10, model.ponders, flat_input, flat_output, config.TESTS_NO, point_height, model_type)
    


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