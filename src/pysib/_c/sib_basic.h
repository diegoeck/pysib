#ifndef BASIC_H
#define BASIC_H

void filtra(double* teta, int n, int d, int delay, double* u, int du, double* y);
void filter(double* B, double* A, int nB, int nA, int k, double* u, int du, double* y);
double norm(double* A, int dA);

#endif

