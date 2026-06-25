# AI-Framework---C-Python-Data-Structures
An AI Framework that trains AI models for general use an linear problems

This is a program that lets you train AI models for various use cases.

This directory should be imported into your python script.

The way it works:
calling:
variable.train(all_input_list, all_output_list, char)

char = "r" or "c"
"r" = regression(this code trains the model for calculating final numbers for an equation)
"c" = clasification(this code trains the model for choosing between n options)

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

The programs works by making 32 different templates of neural networks randomly generated, as well as for well known types of matrices : funnel, cillinder, barrell and wall.

It trains, tests and scores them by how well they've done. Then the least intelligent half gets destroyed and the rest get further more educated
This process repeats until just one remains on ground and a file is made in the directory of the program with the brute data of its model

If a model was already trained for an application, you SHOULD NOT use the train function, but the get function, that calculates using the nerual network that was just already formed.



