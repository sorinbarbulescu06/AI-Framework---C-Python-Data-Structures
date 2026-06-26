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
        ctypes.c_char, #model_type
        ctypes.c_float #rate
    ]
    train_lib.train_and_test.restype = ctypes.c_float

    #initiating presets
    presets = [] #adn list
    existing_adn = []
    cnt = 0
    print("LOCK AND LOADED")
    logic.hardcode(presets, existing_adn) #first 4 well-know presets
    print("GOT THE FIRST 4 MODELS")
    while len(presets) < config.TEMPLATE_NO:# the rest of them
        model = logic.preset()
        print(model.space)
        if model.height not in existing_adn and model.space < 1000000:
            print("GOT ANOTHER MODEL", cnt)
            cnt += 1
            existing_adn.append(model.height)
            presets.append(model)
    
    #first training - !10 epochs!
    for i in range(config.COMP_LENGHT):
        print("TRAINING STAGE", i + 1)
        cnt = 0
        for model in presets:
            print("TRAINING MODEL", cnt)
            cnt += 1
            point_height = (ctypes.c_int * model.depth)(*model.height)
            model.err = train_lib.train_and_test(config.INPUT_NO, config.OUTPUT_NO, model.depth, config.EPOCHS[i], model.ponders, flat_input, flat_output, config.TESTS_NO, point_height, model_type.encode('utf-8'), config.LEARNING_RATE)
        presets.sort(key=lambda model: model.err) #sorted array
        presets = presets[:config.QUALIFY[i]]

    #verifying if its worth swaping theese 2 winners for memory consumption
    if presets[1].err < 1.5 * presets[0].err and presets[0].space > 1.5 * presets[1].space:
        presets[0], presets[1] = presets[1], presets[0]
        print("I SWITCHED")

    
    return presets[0]
