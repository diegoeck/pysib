#include <math.h>


void filtra(double* teta, int n, int d, int k, double* u, int du, double* y)
{
    // Funcao Filtro A(z)y(t)=B(z)u(t)
    // Considera que A[0]=1 
 
    int i;
    int j;

    for (i = 0; i <du; i++)  
    {
        y[i]=0;
        for (j = 0; j < n; j++)
        {
            if ((i-j-k)>=0)
            {
                y[i] += u[i-j-k]*teta[j]; 
            }
        }
    
        for (j = 0; j < d; j++)
        {
            if ((i-j-1)>=0)
            {
                y[i] -= y[i-j-1]*teta[j+n]; 
            }
        }
        
    }

}

void filter(double* B, double* A, int nB, int nA, int k, double* u, int du, double* y)
{
    // Funcao Filtro A(z)y(t)=B(z)u(t)
    // Considera que A[0]=1 
 
    int i;
    int j;

    for (i = 0; i <du; i++)  
    {
        y[i]=0;
        for (j = 0; j < nB; j++)
        {
            if ((i-j-k)>=0)
            {
                y[i] += u[i-j-k]*B[j]; 
            }
        }
    
        for (j = 1; j < nA; j++)
        {
            if ((i-j)>=0)
            {
                y[i] -= y[i-j]*A[j]; 
            }
        }
        
    }

}

double norm(double* A,int dA)
{
    // Norma de A
    
    double resultado=0;    
    int i;
    
    for (i = 0; i <dA; i++)  
    {
        resultado+=A[i] * A[i];
    }
    
    return sqrt(resultado);

}
