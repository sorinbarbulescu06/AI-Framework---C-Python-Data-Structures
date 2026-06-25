#include <stdio.h>
#include <stdlib.h>
#include <math.h>

float alfa = 0.01;

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
        int *heights, char type)
{
    int exam = (int)Tests * 0.8;
    int neura_num = 0;
    int i,j,k,l;
    
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
    //values_chart[i][j] = matricea de valori aferenta
    
    for(int t = 0; t < Epoch; ++t) {
        for (l = 0; l < exam; ++l) {
            //modifying the values throughout forward_pass
            forward_pass(INPUT_NO, OUTPUT_NO, Depth, pond_n_bias,
                &inp_data[l * INPUT_NO], values_chart, heights, type);
            
        }
    }
    
    free(values_chart);
    free(values_pool);
}