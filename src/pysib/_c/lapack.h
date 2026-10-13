#ifndef LAPACK_COMPAT_H
#define LAPACK_COMPAT_H

#include <stddef.h>

/* System LAPACK (Fortran calling convention, underscore suffix).
   Uses int* for dimensions, unlike MATLAB's mwlapack which uses ptrdiff_t*. */
extern void dgelss_(int *m, int *n, int *nrhs,
                    double *a, int *lda,
                    double *b, int *ldb,
                    double *s, double *rcond, int *rank,
                    double *work, int *lwork,
                    int *info);

/* Inline wrapper: ptrdiff_t* (MATLAB convention) -> int* (system LAPACK).
   Safe because all models have dteta <= 100, well within int range. */
static inline void dgelss(ptrdiff_t *m, ptrdiff_t *n, ptrdiff_t *nrhs,
                           double *a, ptrdiff_t *lda,
                           double *b, ptrdiff_t *ldb,
                           double *s, double *rcond, ptrdiff_t *rank,
                           double *work, ptrdiff_t *lwork,
                           ptrdiff_t *info)
{
    int _m = (int)*m, _n = (int)*n, _nrhs = (int)*nrhs;
    int _lda = (int)*lda, _ldb = (int)*ldb, _lwork = (int)*lwork;
    int _rank, _info;
    dgelss_(&_m, &_n, &_nrhs, a, &_lda, b, &_ldb, s, rcond, &_rank,
            work, &_lwork, &_info);
    *rank = (ptrdiff_t)_rank;
    *info = (ptrdiff_t)_info;
}

#endif
