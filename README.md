# AI-Framework---C-Python-Data-Structures
An AI Framework that trains AI models for general use an linear problems

This is a program that lets you train AI models for various use cases.

This directory should be imported into your python script.

The way it works:
Variables:
in config.py you must put your own data in order to build a model that converges, play a bit with those numbers

calling:
variable.train(all_input_list, all_output_list, char)

char = "r" or "c"
"r" = regression(this code trains the model for calculating final numbers for an equation)
"c" = classification(this code trains the model for choosing between n options)

You have to make 2 lists used for this program to learn and test its abilities

all_input_list = [input0_list,
              input1_list,
              input2_list,
              ...
              inputJ_list,
              ...
              ]
inputJ_list = [inputJ0, inputJ1, inputJ2, ...] 

all_output_list = [output0_list,
                   output1_list,
                   output2_list,
                   ...
                   outputJ_list,
                   ...
                   ]
outputJ_list = [outputJ0, outputJ1, outputJ2, ...] 

Where each inputJ_list in all_input_list should be all the input data for the J-th test each outputJ_list in all_output_list should be all the outputs data for the same
J-th test

There is no need for normalization of data, this code does that in the background


!!!IMPORTANT!!!
-This program normalizes data using the input and output max and min / field
so if the training dataset does not contain all the possible cases then the final model cannot "predict" what it didn't saw(or at least it cant precisely predict it)
-If you want a classification method, the all_output_list should contain only lists of 1 element that resemble the "winning" case, you must also put all posibile scenarios in the output file so that the program can learn all the possible scenarios

Functionality:
The programs works by making 32 different templates of neural networks randomly generated, as well as for well known types of matrices : funnel, cillinder, barrell and wall.

It trains, tests and scores them by how well they've done. Then the least intelligent half gets destroyed and the rest get further more educated
This process repeats until just one remains on ground and a file is made in the directory of the program with the brute data of its model

If a model was already trained for an application, you SHOULD NOT use the train function, but the get function, that calculates using the neural network that was just already formed.

Memory usage:
all of the 32 templates have a float pointer that stores all the weights and biases that each neural network has.

Aproximation of maximum memory occupied for one weight matrix:

(8 * input_number(25 * input_number + 4 + output_number) + output_number) * 4 bytes

with the restriction that this equation cannot physically go over 3.8MB and in total(32 templates) cannot go over 123MB

So for an example of a problem that has 10 inputs and 10 outputs, all the weight and biases matrices only occupy nearly 3MB and the matrix for training that has 100.000 tests consisting 10 inputs & 10 outputs / tests occupy nearly 7.5MB
so in total python manages a maximum of 10.5MB

C on the other half only manages nearly 2.5 KB on the heap, only storing a matrix for the calculated values and error for every neuron

+- the rest of the data stored this code can succsessfuly run on 20MB of free data





