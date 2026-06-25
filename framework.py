import ctypes
import config
import logic
import random

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
        model.err = train_lib.train_and_test(config.INPUT_NO, config.OUTPUT_NO, model.depth, 10, model.ponders, flat_input, flat_output, config.TESTS_NO, point_height, model_type.encode('utf-8'))
    presets.sort(key=lambda model: model.err) #sorted array
    presets = presets[:16]

    #second training - !30 epochs!
    for model in presets:
        point_height = (ctypes.c_int * model.depth)(*model.height)
        model.err = train_lib.train_and_test(config.INPUT_NO, config.OUTPUT_NO, model.depth, 30, model.ponders, flat_input, flat_output, config.TESTS_NO, point_height, model_type.encode('utf-8'))
    presets.sort(key=lambda model: model.err) #sorted array
    presets = presets[:8]

    #third training - !50 epochs!
    for model in presets:
        point_height = (ctypes.c_int * model.depth)(*model.height)
        model.err = train_lib.train_and_test(config.INPUT_NO, config.OUTPUT_NO, model.depth, 50, model.ponders, flat_input, flat_output, config.TESTS_NO, point_height, model_type.encode('utf-8'))
    presets.sort(key=lambda model: model.err) #sorted array
    presets = presets[:4]

    #fourth training - !100 epochs!
    for model in presets:
        point_height = (ctypes.c_int * model.depth)(*model.height)
        model.err = train_lib.train_and_test(config.INPUT_NO, config.OUTPUT_NO, model.depth, 100, model.ponders, flat_input, flat_output, config.TESTS_NO, point_height, model_type.encode('utf-8'))
    presets.sort(key=lambda model: model.err) #sorted array
    presets = presets[:2]

    #verifying if its worth swaping theese 2 winners for memory consumption
    if presets[1].err < 1.5 * presets[0].err and presets[0].space > 1.5 * presets[1].space:
        presets[0], presets[1] = presets[1], presets[0]
    return presets[0]


def main():
    inpt = []
    outpt = []

    # Generam 300 de puncte random pe un grafic 2D
    for _ in range(300):
        # Generam coordonate X si Y intre -10 si 10
        x = random.uniform(-10.0, 10.0)
        y = random.uniform(-10.0, 10.0)
        
        inpt.append([x, y]) # Astea sunt datele de intrare (INPUT_NO = 2)
        
        # Etichetam (clasificam) punctele.
        # ATENTIE: La clasificare, output-ul tau cere doar un INDEX!
        if x > 0 and y > 0:
            outpt.append([0.0]) # Clasa 0
        elif x <= 0 and y > 0:
            outpt.append([1.0]) # Clasa 1
        else:
            outpt.append([2.0]) # Clasa 2

    print("Incepem turneul de antrenament pentru CLASIFICARE...")
    
    # Rulam cu flag-ul "c"
    campion = train(inpt, outpt, "c")
    
    print("\n=== REZULTAT FINAL CLASIFICARE ===")
    # Aici scorul afisat va fi media Cross-Entropy (logaritmii negativi)
    print(f"Eroarea campionului (Cross-Entropy): {campion.err:.6f}")
    print(f"Adancime (straturi ascunse): {campion.depth}")
    print(f"Arhitectura (neuroni/strat): {campion.height}")
    print(f"Parametri totali in memorie: {campion.space}")

if __name__ == "__main__":
    main()