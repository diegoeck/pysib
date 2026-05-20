#define PY_SSIZE_T_CLEAN
#include <Python.h>

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>

#include <stdint.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <float.h>
#include <sib_basic.h>
#include <sib_optimize.h>

double *teta;
double *u;
double *ym;
double *tetafim;
double **H;
double *gra;

int du;
int dteta;
int dB;
int dF;
int delay;
int mode;

void grad(double* teta, double* J)
{
    // Calcula o gradiente da estrutura OE e o custo atual
    double *e;
    double *y0;
    double *dydB;
    double *dydF;
    int i,j,k;

    double *pB;
    double *pF;

    double p1[1]={1};
    double p1n[1]={-1};
    
    pB = malloc( (dB)*sizeof(double) );
    pF = malloc( (dF+1)*sizeof(double) );

    e=malloc((du)*sizeof(double));
    y0=malloc((du)*sizeof(double));
    dydB=malloc((du)*sizeof(double));
    dydF=malloc((du)*sizeof(double));


    for (k = 0; k < dB; k++)
    {
        pB[k] = teta[k];
    }

    pF[0] = 1;
    for (k = 0; k < dF; k++)
    {
        pF[k+1] = teta[dB+k];
    }
    
    // Calcula o custo
    filter(pB, pF, dB, dF+1, delay, u, du, y0); 
    J[0]=0;
    for (k = 0; k < du; k++)
    {
        e[k]=(y0[k]-ym[k]);
        J[0]+=(e[k])*(e[k]);
    }
    J[0] = sqrt(J[0]/du);


    if(mode==1 | mode==2){
        // Calcula gradiente com relacao ao numerador

        filter(p1, pF, 1, dF+1, delay, u, du, dydB); 
        for (j = 0; j < dB; j++)
        {
            gra[j]=0;
            for (k = j; k < du; k++)
            {
                gra[j]+=(e[k])*(dydB[k-j]);
            }
        }

        // Calcula gradiente com relacao ao denominador
        filter(p1n, pF, 1, dF+1, 1, y0, du, dydF); 
        for (j = 0; j < dF; j++)
        {
            gra[dB+j]=0;
            for (k = j; k < du; k++)
            {
                gra[dB+j] += (e[k])*(dydF[k-j]);
            }
        }
    }
    
    if(mode==2)
    {

        for (j = 0; j < dB+dF; j++)
        {
            for (k = 0; k < dB+dF; k++)
            {
                H[j][k]=0;
            }
        }
        
        for (j = 0; j < dB; j++)
        {
            for (k = j; k < dB; k++)
            {
                for (i = 0; i < du; i++)
                {   
                    if ((i>=j)&(i>=k))
                    {
                        H[j][k] += dydB[i-j]*dydB[i-k];
                    }
                }
                H[k][j] = H[j][k];
            }
            for (k = 0; k < dF; k++)
            {
                for (i = 0; i < du; i++)
                {            
                    if ((i>=j)&(i>=k))
                    {
                        H[j][dB+k] += dydB[i-j]*dydF[i-k];
                    }
                }
                H[dB+k][j] = H[j][dB+k];
            }
        }

        for (j = 0; j < dF; j++)
        {
            for (k = j; k < dF; k++)
            {
                for (i = 0; i < du; i++)
                {            
                    if ((i>=j)&(i>=k))
                    {
                        H[dB+j][dB+k] += dydF[i-j]*dydF[i-k];
                    }
                }
                H[dB+k][dB+j] = H[dB+j][dB+k];
            }
        }
        

    }
    
    free(dydB);
    free(dydF);
    free(y0);
    free(e);

    free(pB);
    free(pF);

}

static PyObject *py_identify(PyObject *self, PyObject *args)
{
    PyObject *u_obj;
    PyObject *y_obj;
    PyObject *theta_obj;
    PyArrayObject *u_arr = NULL;
    PyArrayObject *y_arr = NULL;
    PyArrayObject *theta_arr = NULL;
    PyArrayObject *theta_out = NULL;
    npy_intp dims[1];
    int i;
    int nb;
    int nf;
    int nz;

    (void)self;

    if (!PyArg_ParseTuple(args, "OOOiii", &u_obj, &y_obj, &theta_obj, &nb, &nf, &nz))
    {
        return NULL;
    }

    u_arr = (PyArrayObject *)PyArray_FROM_OTF(u_obj, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
    if (u_arr == NULL)
    {
        goto fail;
    }

    y_arr = (PyArrayObject *)PyArray_FROM_OTF(y_obj, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
    if (y_arr == NULL)
    {
        goto fail;
    }

    theta_arr = (PyArrayObject *)PyArray_FROM_OTF(theta_obj, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
    if (theta_arr == NULL)
    {
        goto fail;
    }

    du = (int)PyArray_SIZE(u_arr);
    if (PyArray_SIZE(y_arr) != du)
    {
        PyErr_SetString(PyExc_ValueError, "u and y must have the same number of elements");
        goto fail;
    }

    dteta = (int)PyArray_SIZE(theta_arr);
    dB = nb;
    dF = nf;
    delay = nz;

    if (dteta != dB+dF)
    {
        PyErr_SetString(PyExc_ValueError, "theta_init must have nb + nf elements");
        goto fail;
    }

    dims[0] = dteta;
    theta_out = (PyArrayObject *)PyArray_SimpleNew(1, dims, NPY_DOUBLE);
    if (theta_out == NULL)
    {
        goto fail;
    }

    u = (double *)PyArray_DATA(u_arr);
    ym = (double *)PyArray_DATA(y_arr);
    teta = (double *)PyArray_DATA(theta_arr);
    tetafim = (double *)PyArray_DATA(theta_out);

    gra = malloc((dteta)*sizeof(double));
    H = malloc(dteta * sizeof(double *));
    H[0] = malloc(dteta * dteta * sizeof(double));
    for(i = 1; i < dteta; i++)
        H[i] = H[0] + i * dteta;

    memcpy(tetafim, teta, sizeof(double) *dteta);
    sib_steepest(tetafim);
    sib_newton(tetafim);
    
    free(gra);
    free(H[0]);
    free(H);

    Py_DECREF(u_arr);
    Py_DECREF(y_arr);
    Py_DECREF(theta_arr);

    return (PyObject *)theta_out;

fail:
    Py_XDECREF(u_arr);
    Py_XDECREF(y_arr);
    Py_XDECREF(theta_arr);
    Py_XDECREF(theta_out);
    return NULL;
}

static PyMethodDef methods[] = {
    {"identify", py_identify, METH_VARARGS, "Run OE identification."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "_pysib_oe_core",
    NULL,
    -1,
    methods
};

PyMODINIT_FUNC PyInit__pysib_oe_core(void)
{
    import_array();
    return PyModule_Create(&module);
}
