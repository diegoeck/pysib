#include <stdint.h>
#include <math.h>
#include <string.h>
#include <float.h>
#include <stdio.h>
#include <stdlib.h>
#include "lapack.h"
#include <sib_basic.h>
#include <sib_optimize.h>
typedef uint16_t char16_t;

extern double *teta;
extern double *gra;
extern double **H;
extern int dteta;
extern int mode;

extern void grad(double *teta, double *J);


void sib_steepest(double* tetafim)
{

    int i,j,k;
    double *tetatemp;
    double *dir;
    double passo = 0.00001;
    double N;
    double J1[1];
    double J2[1];

    tetatemp=malloc((dteta)*sizeof(double));
    dir=malloc((dteta)*sizeof(double));
    
    //memcpy(tetafim,teta,sizeof(double) *dteta);

    for(i=1; i<=100; i++)
    {

        

        for(j=1; j<=100; j++)
        {   
            mode=1;
            grad(tetafim,J1);
            
            //printf("T %1.10f %1.10f %1.10f %1.10f\n",tetafim[0],tetafim[1],tetafim[2],tetafim[3]);
            //printf("G %1.10f %1.10f %1.10f %1.10f\n",gra[0],gra[1],gra[2],gra[3]);

            if((i==1)&(j==1))
            {
                memcpy(dir,gra,sizeof(double)*dteta);
            }

            for (k = 0; k < dteta; k++)
            {
                dir[k] = (4*dir[k]+gra[k])/5;
            }
    
            N = norm(dir,dteta); 

            for (k = 0; k < dteta; k++)
            {
                tetatemp[k] = tetafim[k] - passo*dir[k]/N;
            }

            mode=0;
            grad(tetatemp,J2);

            if (J2[0]>J1[0])
            {
                passo=passo*0.99;

            }else{   
                passo=passo*1.01;
                memcpy(tetafim,tetatemp,sizeof(double) *dteta);
            }
    
        }    
    
        
        printf("G: ");
        for (k = 0; k < i/5; k++)
        {
            printf("#");
        }
        for (k = i/5; k < 20; k++)
        {
            printf("-");
        }
        printf(" %03d%% %1.10f %1.10f \n", i, J1[0], passo);

        

        if (passo<0.0000001)
        {
            break;
        }    
    }

    free(tetatemp);
    free(dir);

}
 



void sib_newton(double* tetafim)
{

    int i,j,k;
    double *tetatemp;
    double passo = 0.00001;
    double J1[1];
    double J2[1];

    //#ifdef _WIN64
    //long long Ns = (long long)dteta;
    //long long Ms = 1;
    //long long *ipiv;
    //ipiv=malloc((dteta)*sizeof(long long));
    //long long info;
    //#else
    ptrdiff_t Ns = dteta;
    ptrdiff_t Ms = 1;
    ptrdiff_t info = 0;
    
    char uplo[] = "U";
    //ptrdiff_t *ipiv;
    //ipiv=malloc((dteta)*sizeof(ptrdiff_t));

    //#endif
    

    
    //int erro=0;


    tetatemp=malloc((dteta)*sizeof(double));

    //memcpy(tetafim,teta,sizeof(double) *dteta);


    for(i=1; i<=1000; i++)
    {

        mode=2;
        grad(tetafim,J1);

        //printf("G: \n");
        //printf("antes %1.10f %1.10f %1.10f %1.10f\n",gra[0],gra[1],gra[2],gra[3]);
        
        //printf("antes: %f\n", gra[3]);
        //printf("H: \n");
        //printf("%1.10f %1.10f %1.10f %1.10f\n",H[0][0],H[0][1],H[0][2],H[0][3]);
        //printf("%1.10f %1.10f %1.10f %1.10f\n",H[1][0],H[1][1],H[1][2],H[1][3]);
        //printf("%1.10f %1.10f %1.10f %1.10f\n",H[2][0],H[2][1],H[2][2],H[2][3]);
        //printf("%1.10f %1.10f %1.10f %1.10f\n",H[3][0],H[3][1],H[3][2],H[3][3]);        

        //printf("%1.10f %1.10f %1.10f\n",H[0][0],H[0][1],H[0][2]);
        //printf("%1.10f %1.10f %1.10f\n",H[1][0],H[1][1],H[1][2]);
        //printf("%1.10f %1.10f %1.10f\n",H[2][0],H[2][1],H[2][2]);

        
        
        //dgesv(&Ns, &Ms, *H, &Ns, ipiv, gra, &Ns, &info);
        dposv(uplo, &Ns, &Ms, *H, &Ns, gra, &Ns, &info);

        //printf("depois %1.10f %1.10f %1.10f %1.10f\n",gra[0],gra[1],gra[2],gra[3]);
        
        //printf("info: %d\n", info);

    /*
        if (isnan(gra[0]))
        {
            break;
        }
     */
        
        for (k = 0; k < dteta; k++)
        {
            tetatemp[k] = tetafim[k] - gra[k]*(i+1)/1000;
        }
    
        //memcpy(tetafim,tetatemp,sizeof(double) *dteta);
        
        
        for (j = 0; j < 10; j++)
        {
    
            mode=0;
            grad(tetatemp,J2);

            if (J2[0]>J1[0] || !isfinite(J2[0]) || !isfinite(tetatemp[0]))
            {
                //printf("ERRO \n");
                for (k = 0; k < dteta; k++)
                {
                    tetatemp[k] = (tetatemp[k]+tetafim[k])/2;
                }

            }else{   
                
                memcpy(tetafim,tetatemp,sizeof(double) *dteta);
                break;
                
            }
        }

        // if (j==10)
        // {
        //     break;
        // }

        
        
        
        if (i%10==0)
        {
            printf("N: ");
            for (k = 0; k < (i/50); k++)
            {
                printf("#");
            }
            for (k = (i/50); k < 20; k++)
            {
                printf("-");
            }
            printf(" %03d%% %1.10f %1.10f \n", i/10, J1[0], ((float)i)/1000.0);
        }
        
        
        
        
    }

    //free(ipiv);
    free(tetatemp);

}
 

