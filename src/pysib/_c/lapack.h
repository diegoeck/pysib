#ifndef LAPACK_COMPAT_H
#define LAPACK_COMPAT_H

#include <stddef.h>

/* System LAPACK (Fortran calling convention, underscore suffix).
   Uses int* for dimensions, unlike MATLAB's mwlapack which uses ptrdiff_t*. */
extern void dposv_(char *uplo, int *n, int *nrhs,
                   double *a, int *lda,
                   double *b, int *ldb,
                   int *info);

/* Inline wrapper: ptrdiff_t* (MATLAB convention) -> int* (system LAPACK).
   Safe because all models have dteta <= 100, well within int range. */
static inline void dposv(char *uplo, ptrdiff_t *n, ptrdiff_t *nrhs,
                          double *a, ptrdiff_t *lda,
                          double *b, ptrdiff_t *ldb,
                          ptrdiff_t *info)
{
    int _n = (int)*n, _nrhs = (int)*nrhs;
    int _lda = (int)*lda, _ldb = (int)*ldb, _info;
    dposv_(uplo, &_n, &_nrhs, a, &_lda, b, &_ldb, &_info);
    *info = (ptrdiff_t)_info;
}

#endif
