#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

float alfa = 0.01;
float learning_rate;

float grade(const int OUTPUT_NO, float **values_chart, const float *current_out,
    const char type, const int Depth)
{
    int i;
    float sum = 0;
    if (type == 'c') {
        if (values_chart[Depth][(int)current_out[0]] >= 1e-7f) {
            sum += -logf(values_chart[Depth][(int)current_out[0]]);
        } else {
            sum += -logf(1e-7f);
        }
    } else {
        for (i = 0; i < OUTPUT_NO; ++i) {
            sum += fabsf(values_chart[Depth][i] - current_out[i]);
        }
        sum /= OUTPUT_NO;
    }
    return sum;
}

static inline void backprop(const int OUTPUT_NO, float **values_chart,float **err_chart,
    const char type, const int Depth, const float *current_out, const int *heights, const int *offset,
        float *pond_n_bias, const int INPUT_NO, const float *current_inp)
{
    int i,j,k;
    if (type == 'r') {
        for (i = 0; i < OUTPUT_NO; ++i) {
            float der;
            if (values_chart[Depth][i] > 0) {
                der = 1;
            } else {
                der = alfa;
            }
            err_chart[Depth][i] = (values_chart[Depth][i] - current_out[i]) * der;
        }
    } else {
        for (i = 0; i < OUTPUT_NO; ++i) {
            err_chart[Depth][i] = values_chart[Depth][i] - (float)(i == (int)current_out[0]);
        }
    }
    for (i = Depth; i > 0; --i) {
        //step1 : err propagation
        for (j = 0; j < heights[i - 1]; ++j) {
            float sum = 0;
            if (i == Depth) {//case of output Row
                int cont = 0;
                for (k = 0; k < OUTPUT_NO; ++k) {
                    sum += err_chart[Depth][k] * pond_n_bias[offset[Depth] + cont + j];
                    cont += heights[i - 1] + 1;
                }
                //*deriv
                if (values_chart[Depth - 1][j] <= 0) {
                    err_chart[Depth - 1][j] = sum * alfa;
                } else {
                    err_chart[Depth - 1][j] = sum;
                }
            } else { // middle case
                int cont = 0;
                for (k = 0; k < heights[i]; ++k) {
                    sum += err_chart[i][k] * pond_n_bias[offset[i] + cont + j];
                    cont += heights[i - 1] + 1;
                }
                //*deriv
                if (values_chart[i - 1][j] <= 0) {
                    err_chart[i - 1][j] = sum * alfa;
                } else {
                    err_chart[i - 1][j] = sum;
                }
            }
        }
        //step2 : new weight and bias
        int range;
        if (i == Depth) {
            range = OUTPUT_NO;
        } else {
            range = heights[i];
        }
        int cont = 0;
        for (j = 0; j < range; ++j) {
            for (k = 0; k < heights[i - 1]; ++k) {
                pond_n_bias[offset[i] + cont + k] -= values_chart[i - 1][k] * err_chart[i][j] * learning_rate;
            }
            pond_n_bias[offset[i] + cont + heights[i - 1]] -= err_chart[i][j] * learning_rate;
            cont += heights[i - 1] + 1;
        }
    }
    //modifying first weights
    int cont = 0;
    for (i = 0; i < heights[0]; ++i) {
        for (j = 0; j < INPUT_NO; ++j) {
            pond_n_bias[offset[0] + cont + j] -= current_inp[j] * err_chart[0][i] * learning_rate;
        }
        pond_n_bias[offset[0] + cont + INPUT_NO] -= err_chart[0][i] * learning_rate;
        cont += INPUT_NO + 1;
    }
}


static inline void forward_pass(const int INPUT_NO, const int OUTPUT_NO, const int Depth,
    const float *pond_n_bias, const float *current_inp, float **values_chart,
        const int *heights, const char type)
{
    int cursor = 0;
    int i,j,k;
    for (i = 0; i < Depth; ++i) {
        for (j = 0; j < heights[i]; ++j) {
            float sum = 0;
            if (i == 0) {
                for (k = 0; k < INPUT_NO; ++k) {
                    sum += current_inp[k] * pond_n_bias[cursor];
                    cursor++;
                }
                sum += pond_n_bias[cursor];
                cursor++;
            } else {
                for(k = 0; k < heights[i - 1]; ++k) {
                    sum += values_chart[i - 1][k] * pond_n_bias[cursor];//ading wieght * prev_val
                    cursor++;
                }
                sum += pond_n_bias[cursor]; //adding bias
                cursor++;
            }
            if (sum > 0) {
                values_chart[i][j] = sum;
            } else {
                values_chart[i][j] = alfa * sum;
            }
        }
    }
    if (type == 'r') { //regression so Leaky ReLU
        for(i = 0; i < OUTPUT_NO; ++i) {
            float sum = 0;
            for (j = 0; j < heights[Depth - 1]; ++j) {
                sum += values_chart[Depth - 1][j] * pond_n_bias[cursor];
                cursor++;
            }
            sum += pond_n_bias[cursor];
            cursor++;
            if (sum > 0) {
                values_chart[Depth][i] = sum;
            } else {
                values_chart[Depth][i] = alfa * sum;
            }
        }
    } else { //clasification so Softmax
        float exp_sum = 0;
        for (i = 0; i < OUTPUT_NO; ++i) {
            float sum = 0;
            for (j = 0; j < heights[Depth - 1]; ++j) {
                sum += values_chart[Depth - 1][j] * pond_n_bias[cursor];
                cursor++;
            }
            sum +=pond_n_bias[cursor];
            cursor++;
            values_chart[Depth][i] = exp(sum);
            exp_sum += values_chart[Depth][i];
        }
        for (i = 0; i < OUTPUT_NO; ++i) {
            values_chart[Depth][i] = values_chart[Depth][i] / exp_sum;
        }
    }
}

float train_and_test(int INPUT_NO, int OUTPUT_NO, int Depth, int Epoch,
    float *pond_n_bias, float *inp_data, float *out_data, int Tests,
        int *heights, char type, float rate)
{
    learning_rate = rate;
    srand(time(NULL));
    int i,j,k,l;
    int *offset = malloc((Depth + 1) * sizeof(int));
    for (i = 0; i < Depth + 1; ++i) {
        if (i == 0) {
            offset[i] = 0;
        } else if (i == 1) {
            offset[i] = offset[i - 1] + heights[i - 1] * INPUT_NO + heights[i - 1];
        } else {
            offset[i] = offset[i - 1] + heights[i - 1] * heights[i - 2] + heights[i - 1];
        }
    }
    int exam = (int)Tests * 0.8;
    int neura_num = 0;
    int step = OUTPUT_NO;
    if (type == 'c') {
        step = 1;
    }

    for (i = 0; i < Depth; ++i) {
        neura_num += heights[i];
    }
    neura_num += OUTPUT_NO;

    float *values_pool = malloc(neura_num * sizeof(float));
    if (values_pool == NULL) {
        return 999999;
    }
    float **values_chart = malloc((Depth + 1) * sizeof(float *));
    if (values_chart == NULL) {
        return 999999;
    }

    float *curs = values_pool;
    for (i = 0; i < Depth; ++i) {
        values_chart[i] = curs;
        curs += heights[i];
    }
    values_chart[Depth] = curs;

    float *err_pool = malloc(neura_num * sizeof(float));
    if (err_pool == NULL) {
        return 999999;
    }
    float **err_chart = malloc((Depth + 1) * sizeof(float *));
    if (err_chart == NULL) {
        return 999999;
    }

    curs = err_pool;
    for (i = 0; i < Depth; ++i) {
        err_chart[i] = curs;
        curs += heights[i];
    }
    err_chart[Depth] = curs;

    //values_chart[i][j] = neural value matrix
    //err_chart[i][j] = error matrix
    
    //LEARNING PHASE:

    int *indices = malloc(exam * sizeof(int));
    for (l = 0; l < exam; ++l) {
        indices[l] = l;
    }
    for(int t = 0; t < Epoch; ++t) {
        for (l = exam - 1; l > 0; --l) {
            int j = rand() % (l + 1);
            int temp = indices[l];
            indices[l] = indices[j];
            indices[j] = temp;
        }
        for (int step_idx = 0; step_idx < exam; ++step_idx) {
            int current_img = indices[step_idx];
            //modifying the values throughout forward_pass
            forward_pass(INPUT_NO, OUTPUT_NO, Depth, pond_n_bias,
                &inp_data[current_img * INPUT_NO], values_chart, heights, type);
            backprop(OUTPUT_NO, values_chart, err_chart, type, Depth,
                &out_data[current_img * step], heights, offset, pond_n_bias, INPUT_NO, &inp_data[current_img * INPUT_NO]);
        }
    }
    //TESTING PHASE:
    float score = 0;
    for (l = exam; l < Tests; ++l) {
        forward_pass(INPUT_NO, OUTPUT_NO, Depth, pond_n_bias, &inp_data[l * INPUT_NO],
            values_chart, heights, type);
        score += grade(OUTPUT_NO, values_chart, &out_data[l * step], type, Depth);
    }
    score /= Tests - exam;

    free(values_chart);
    free(values_pool);
    free(err_pool);
    free(err_chart);
    free(offset);
    free(indices);
    return score;
}