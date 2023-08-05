"""Cochran-Mantel-Haenzsel Chi2 Test.

Code ported from/based on "Categorical Data Analysis", page 295 by Agresti
(2002) and R implementation of the function `mantelhaen.test()`.
"""
import logging
import textwrap

import numpy as np
import pandas as pd
from scipy import stats


class CMHResult(object):
    """Represents the result of a Cochran-Mantel-Haenszel Chi2 analysis."""

    def __init__(self, STATISTIC, dof, p, var1, var2, stratifier, alpha=0.05):
        """
        Initialize a new CMHResult.

            STATISTIC: X2 statistic
            dof: degrees of freedom
            p: p-value
        """
        self.STATISTIC = STATISTIC
        self.dof = dof
        self.p = p
        self.var1 = var1
        self.var2 = var2
        self.stratifier = stratifier
        self.alpha = alpha

    def __repr__(self):
        """repr(x) <==> x.__repr__()"""
        stat = round(self.STATISTIC, 5)
        pval = round(self.p, 4)
        dof = self.dof

        return textwrap.dedent(f"""
                Cochran-Mantel-Haenszel Chi2 test

        "{self.var1}" x "{self.var2}", stratified by "{self.stratifier}"

        Cochran-Mantel-Haenszel M^2 = {stat}, dof = {dof}, p-value = {pval}
        """)

    def _repr_html_(self):
        """Return HTML representation of result.

        USed in Jupyter when `display(result)."""
        stat = round(self.STATISTIC, 5)
        pval = round(self.p, 4)
        dof = self.dof

        # Inner HTML, formats the result.
        inner_html = f"""
        <div style="font-family: courier; font-size: 10pt; padding: 0px 10px;">
            <div style="text-align:center">
                Cochran-Mantel-Haenszel Chi&#x00B2; test
            </div>

            <div>
                <b>{self.var1}</b> x <b>{self.var2}</b>,
                stratified by <b>{self.stratifier}</b>
            </div>
            <div>
                Cochran-Mantel-Haenszel
                    M^2 = {stat},
                    dof = {dof},
                    p-value = <b>{pval}</b>
            </div>
        </div>
        """

        # Outer HTML, determines the color depending on p-value

        if pval > self.alpha:
            background_color, border_color = '#efefef', '#cfcfcf'
        else:
            background_color, border_color = '#b0cbe9', '#4393e1'

        html_ = f"""
        <div style="
            background-color: {background_color};
            border: 1px solid {border_color};
            padding: 5px;"
            >
            {inner_html}
        </div>
        """
        return html_


def CMH(df: pd.DataFrame, var: str, outcome: str, stratifier: str, raw=False,
        adjustment=0.0):
    """Compute the CMH statistic.

    Based on "Categorical Data Analysis", page 295 by Agresti (2002) and
    R implementation of mantelhaen.test().
    """
    df = df.copy()
    df[outcome] = df[outcome].astype('category')
    df[var] = df[var].astype('category')
    df[stratifier] = df[stratifier].astype('category')

    # Compute contingency table size KxIxJ
    I = len(df[outcome].cat.categories)
    J = len(df[var].cat.categories)
    K = len(df[stratifier].cat.categories)

    contingency_tables = np.zeros((I, J, K), dtype='float')

    # Create stratified contingency tables
    for k in range(K):
        cat = df[stratifier].cat.categories[k]

        subset = df.loc[df[stratifier] == cat, [var, outcome]]
        xs = pd.crosstab(subset[outcome], subset[var], dropna=False)
        contingency_tables[:, :, k] = xs  + adjustment

    # Compute the actual CMH
    STATISTIC, df, pval = CMH_numpy(contingency_tables)

    if raw:
        return STATISTIC, df, pval

    return CMHResult(STATISTIC, df, pval, var, outcome, stratifier)


def CMH_numpy(X):
    """Compute the CMH statistic.

    Based on "Categorical Data Analysis", page 295 by Agresti (2002) and
    R implementation of mantelhaen.test().
    """
    log = logging.getLogger('CMH_numpy')

    # I: nr. of rows
    # J: nr. of columns
    # K: nr. of strata
    # ⚠️ Note: this does *not* match the format used when printing!
    I, J, K = X.shape

    log.debug(f"I: {I}, J: {J}, K: {K}")

    df = (I - 1) * (J - 1)
    log.debug(f'{df} degree(s) of freedom')

    # Initialize m and n to a vector(0) of length df
    n = np.zeros(df)
    m = np.zeros(df)
    V = np.zeros((df, df))

    # iterate over the strata
    for k in range(K):
        log.debug(f'partial {k}')
        # f holds partial contigency table k
        f = X[:, :, k]

        # debuggin'
        log.debug('  f:')
        log.debug(f)

        # Sum of *all* values in the partial table
        ntot = f.sum()
        log.debug(f'  ntot: {ntot}')

        # Compute the sum over all row/column entries *excluding* the last
        # entry. The last entries are excluded, as they hold redundant
        # information in combination with the row/column totals.
        colsums = f.sum(axis=0)[:-1]
        rowsums = f.sum(axis=1)[:-1]

        log.debug(f'  rowsums: {rowsums}')
        log.debug(f'  colsums: {colsums}')

        # f[-I, -J] holds the partial matrix, excluding the last row & column.
        # The result is reshaped into a vector.
        log.debug(f'  f[:-1, :-1].reshape(-1): {f[:-1, :-1].reshape(-1)}')
        n = n + f[:-1, :-1].reshape(-1)

        # Take the outer product of the row- and colsums, divide it by the
        # total of the partial table. Yields a vector of length df. This holds
        # the expected value under the assumption of conditional independence.
        m_k = (np.outer(rowsums, colsums) / ntot).reshape(-1)
        m = m + m_k
        log.debug(f'  m_k: {m_k}')

        # V_k holds the null covariance matrix (matrices).
        k1 = np.diag(ntot * colsums)[:J, :J] - np.outer(colsums, colsums)
        k2 = np.diag(ntot * rowsums)[:I, :I] - np.outer(rowsums, rowsums)

        log.debug('np.kron(k1, k2):')
        log.debug(np.kron(k1, k2))

        V_k = np.kron(k1, k2) / (ntot**2 * (ntot - 1))

        log.debug('  V_k:')
        log.debug(V_k)

        V = V + V_k

    # Subtract the mean from the entries
    n = n - m
    log.debug(f'n: {n}')

    log.debug('np.linalg.solve(V, n):')
    log.debug(np.linalg.solve(V, n))

    STATISTIC = np.inner(n, np.linalg.solve(V, n).transpose())
    log.debug(f'STATISTIC: {STATISTIC}')

    pval = 1 - stats.chi2.cdf(STATISTIC, df)

    return STATISTIC, df, pval
