#include <stdio.h>
#include <stdlib.h>
#include <math.h>

float alfa = 0.01;

float* train_and_test(int INPUT_NO, int OUTPUT_NO, int Depth, int Epoch,
    float *pond_n_bias, float *inp_data, float *out_data, int Tests,
        int *heights)
{
    int neura_num = 0;
    int i,j,k,l;
    float *p = malloc()
    for (i = 0; i < Depth; ++i) {
        neura_num += heights[i];
    }
    neura_num += OUTPUT_NO;
    float *values_pool = malloc(neura_num * sizeof(float));
    if (values_pool == NULL) {
        return NULL;
    }
    float **values_chart = malloc((Depth + 1) * sizeof(float *));
    if (values_chart == NULL) {
        return NULL;
    }
    float *curs = values_pool;
    for (i = 0; i < Depth; ++i) {
        values_chart[i] = curs;
        curs += heights[i];
    }
    values_chart[Depth] = curs;
    
    for(int t = 0; t < Epoch; ++t) {
        int dataset = 0;
        int cursor = 0;

        for (l = 0; l < Tests; ++l) {
            for (i = 0; i < Depth; ++i) {
                for (j = 0; j < heights[i]; ++j) {
                    float sum = 0;
                    if (i == 0) {
                        for (k = 0; k < INPUT_NO; ++k) {
                            sum += inp_data[k + dataset] * pond_n_bias[cursor];
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
            //TO IMPLEMENT:BACKPROPAGATION + GRADIENT DESCENT
            dataset += INPUT_NO;
        }
    }
    
    free(values_chart);
    free(values_pool);
    return p;
}