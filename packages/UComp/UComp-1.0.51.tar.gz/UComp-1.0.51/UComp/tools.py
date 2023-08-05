import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import multiprocessing as mp
import seaborn as sns
import scipy.stats as stats
if False:
    import UCmodule as uc
else:
    from UComp import UCmodule as uc
    from UComp import ETSmodule as ets
    from UComp import tsfile


ipi = pd.read_pickle("ipi.bin")
gdp = pd.read_pickle("gdp.bin")
airpas = pd.read_pickle("airpas.bin")


def obj2array(y):
    if isinstance(y, uc.UCmodel):
        x = y.v.values
    elif isinstance(y, ets.ETSmodel):
        x = y.comp[:, 0].values
    elif isinstance(y, pd.Series) or isinstance(y, pd.DataFrame):
        x = y.values
    elif isinstance(y, np.ndarray):
        x = y
    return x


def pacfFun(ACF):
    nCoef = len(ACF)
    fi = np.zeros(nCoef)
    fi[0] = ACF[0]
    PACF = np.zeros(nCoef)
    PACF[0] = fi[0]
    # for p in range(1, nCoef):
    #     fi[p] = (PACF[p] - np.sum(fi[:p] * np.flip(PACF[:p]))) / (1 - np.sum(fi * PACF))
    #     PACF[p] = fi[p]
    #     fi[:p] = fi[:p] - fi[p] * np.flip(fi[:p])
    for i in range(nCoef - 1):
         iACF = ACF[: i + 1]
         fi[i + 1] = (ACF[i + 1] - (sum(fi[0 : i + 1] * iACF[::-1]))) / (1 - sum(fi * ACF))
         PACF[i + 1] = fi[i + 1]
         iACF = fi[0 : i + 1]
         fi[0 : i + 1] -= fi[i + 1] * iACF[::-1]
    return PACF


def removeNaNs(x):
    """
    Remove nans at beginning or end of vector

    x: a vector or a ts object

    Returns:
    vector with nans removed (only those at beginning or end)

    Author:
    Diego J. Pedregal
    """
    x = tsfile.ts(x)
    time_index = x.index
    ind = np.where(~np.isnan(x))[0]
    ind1 = ind.min()
    ind2 = ind.max()
    return x[ind1 : ind2+1]


def sumStats(y, decimals=5):
    """
    SumStats
    Summary statistics of a matrix of variables

    Inputs:
    - y: a vector or matrix of time series
    - decimals: number of decimals for the table

    Returns:
    Table of values

    Author: Diego J. Pedregal
    """
    x = obj2array(y)
    x = x[~np.isnan(x)]
    q25 = np.quantile(x, 0.25)
    q75 = np.quantile(x, 0.75)
    maxx = np.max(x)
    minx = np.min(x)
    meanx = np.mean(x)
    sdx = np.std(x)
    n = len(x)
    m1 = x - meanx
    m2 = np.sum(m1 ** 2)
    skewness = (np.sum(m1 ** 3) / n) / ((m2 / n) ** (3 / 2))
    kurtosis = (np.sum(m1 ** 4) / n) / ((m2 / n) ** 2) - 3
    aux = [len(y),
           len(y) - len(x),
           minx,
           q25,
           meanx,
           2 * stats.t.cdf(-abs(meanx / (sdx / np.sqrt(n))), n - 1),
           np.median(x),
           q75,
           maxx,
           q75 - q25,
           maxx - minx,
           sdx,
           sdx ** 2,
           skewness,
           kurtosis]
    out = np.round(np.array(aux).reshape(15, 1), decimals=decimals)
    out = pd.DataFrame(out, columns=["Serie 1"])
    out.index = ["Data points: ",
                 "Missing: ",
                 "Minimum: ",
                 "1st quartile: ",
                 "Mean: ",
                 "P(Mean = 0): ",
                 "Median: ",
                 "3rd quartile:",
                 "Maximum: ",
                 "Interquartile range: ",
                 "Range: ",
                 "Standard deviation: ",
                 "Variance: ",
                 "Skewness: ",
                 "Kurtosis: "]
    return out


def gaussTest(y, axes=None):
    """
    gausTests
    Tests of gaussianity of a time series

    Inputs:
    - y: a numpy vector or a Pandas time series object

    Author: Diego J. Pedregal
    """
    x = obj2array(y)
    x = x[~np.isnan(x)]
    n = len(x)
    nbins = int(np.sqrt(n))
    stdx = np.std(x)
    varx = stdx ** 2
    # Opening figure
    if axes == None:
        fig = plt.figure(figsize=(8, 6))
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)
    else:
        ax1 = axes[0]
        ax2 = axes[1]
    # Histogram and density plot
    sns.set(style="whitegrid")
    sns.set_palette("colorblind")
    sns.histplot(x, bins=nbins, kde=True, color='red', ax=ax1)
    xl = np.linspace(min(x), max(x), 130)
    y = np.exp(-0.5 * ((xl - np.mean(x)) ** 2) / varx) / np.sqrt(2 * np.pi * varx) * (max(x) - min(x)) * nbins
    ax1.plot(xl, y, color='black', linestyle='--')
    ax1.set_xlabel('Values')
    ax1.set_ylabel('Frequency')
    # QQ plot
    theoretical_quantiles = stats.norm.ppf(np.linspace(0.01, 0.99, num=100))
    # empirical_quantiles = np.percentile((x - np.mean(x)) / stdx, np.linspace(0, 100, num=100))
    empirical_quantiles = np.percentile(x, np.linspace(0, 100, num=100))
    ax2.scatter(theoretical_quantiles, empirical_quantiles, color='blue', alpha=0.5)
    x1, x2 = theoretical_quantiles[0], theoretical_quantiles[-1]
    ax2.plot([x1, x2], [x1 * stdx + np.nanmean(x), x2 * stdx + np.nanmean(x)], color='red')
    ax2.set_ylabel('Theoretical quantiles')
    ax2.set_xlabel('Empirical quantiles')
    # Gaussianity test
    stat, pvalue = stats.shapiro(x)
    print('Shapiro Gaussianity test:')
    print('=========================')
    print(f"Stat: {stat:.4f}   P-value: {pvalue:.4f}")


def ident(y, nCoef=None, nPar=0, axes=None):
    """
    ident
    Autocorrelation functions of a time series

    Inputs:
    - y: a numpy vector or a pandas time series
    - nCoef: number of autocorrelation coefficients to estimate
    - nPar: number of parameters in a model if y is a residual

    Returns:
    A vector with all the dimensions

    Author: Diego J. Pedregal
    """
    if isinstance(y, pd.Series) or isinstance(y, pd.DataFrame):
        s = y.resample('Y').count()[1]
    else:
        s = 1
    x = obj2array(y)
    if nCoef is None:
        nCoef = max(min(37, int(np.floor(len(x) / 4))), s)
    x = (x - np.nanmean(x))  / np.nanstd(x)
    n = len(x[~np.isnan(x)])
    # ACF and PACF with Ljung Box tests and plots
    ACF = np.full(nCoef, 0.0)
    BAND = 2 / np.sqrt(n)
    for i in range(nCoef):
        prod = x[-n + i + 1: ] * x[: n - i - 1]
        prod1 = prod[~np.isnan(prod)]
        ACF[i] = sum(prod1) / len(prod1)
    PACF = pacfFun(ACF)
    SIGa = np.where(ACF > BAND, "+", ".")
    SIGa = np.where(ACF < -BAND, "-", SIGa)
    SIGp = np.where(PACF > BAND, "+", ".")
    SIGp = np.where(PACF < -BAND, "-", SIGp)
    BOX = n * (n + 2) * np.cumsum((ACF ** 2) / (np.array(n, dtype=float) - range(1, nCoef + 1)))
    gl = range(1 - nPar, nCoef + 1 - nPar)
    gl = [1 if j < 1 else j for j in gl]
    pval = 1 - stats.chi2.cdf(BOX, gl)
    out = pd.DataFrame({"SACF": np.round(ACF, 3),
                        "sa": SIGa,
                        "LB": np.round(BOX, 3),
                        "p.val": np.round(pval, 3),
                        "SPACF": np.round(PACF, 3),
                        "sp": SIGp})
    out.index += 1
    if axes == None:
        plotAcfPacf(ACF, PACF, s, n)
    return out


def plotBar(ACF, ax, s=1, n=None, label="ACF"):
    nCoef = len(ACF)
    BAND = 0.0
    if n != None:
        BAND = 2 / np.sqrt(n)
    axis = [i // 3 + 1 for i in range(1, 3 * nCoef)]
    axis.insert(0, 1)
    axis = np.array(axis)
    plotACF = np.zeros(3 * nCoef)
    if s > 1:
        plotSEAS = np.zeros(3 * nCoef)
        plotSEAS[range(3 * (s - 1) + 1, 3 * nCoef, 3 * s)] = ACF[range(s - 1, ACF.shape[0], s)]
        ACF[range(s - 1, ACF.shape[0], s)] = 0
    plotACF[range(1, 3 * nCoef, 3)] = ACF
    if s > 1:
        ax.plot(axis, plotSEAS, color="red", linestyle="dotted", linewidth=1)
    ax.plot(axis, plotACF, color="black", linestyle="solid", linewidth=1)
    ax.set_xlim(0, nCoef + 1)
    ax.plot([0, nCoef + 1], [BAND, BAND], color="red", linestyle="--")
    ax.plot([0, nCoef + 1], [-BAND, -BAND], color="red", linestyle="--")
    ax.plot([0, nCoef + 1], [0, 0], color="black")
    ax.set_xlabel("Lag")
    ax.set_ylabel(label)
    plt.show(block=False)


def plotAcfPacf(ACF, PACF, s=1, n=None, axes=None):
    if axes == None:
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(8, 6))
    plotBar(ACF, axes[0], s, n)
    plotBar(PACF, axes[1], s, n, "PACF")


def cusum(x, axes=None):
    """
    cusum
    Cusum and cusum squared tests

    Inputs:
    - y: a numpy vector or a Pandas time series

    Author: Diego J. Pedregal
    """
    x = obj2array(x)
    n = len(x)
    mz = np.nanmean(x)
    stdz = np.nanstd(x)
    NMiss = ~np.isnan(x)
    Miss = np.isnan(x)
    standz = np.full((n, 1), np.nan)
    cusumLine = standz.copy()
    cusumsq = standz.copy()
    NMissi = np.where(NMiss)
    zmi = x[NMissi] - mz
    standz[NMissi, 0] = zmi / stdz
    cusumLine[NMissi, 0] = np.cumsum(standz[NMissi])
    cusumsq[NMissi, 0] = np.cumsum(zmi ** 2 / np.sum(zmi ** 2))
    t = np.arange(1, n + 1)
    bands = np.full((n, 2), np.nan)
    bands[:, 0] = 0.948 * np.sqrt(n) + 2 * 0.948 * t / np.sqrt(n)
    bands[:, 1] = -bands[:, 0]
    # Plot CUSUM
    if axes == None:
        fig = plt.figure(figsize=(8, 6))
        ax0 = fig.add_subplot(2, 1, 1)
        ax1 = fig.add_subplot(2, 1, 2)
    else:
        ax0 = axes[0]
        ax1 = axes[1]
    ax0.set_xlim(0, n + 1)
    ax0.plot(bands, color="red", linestyle="dotted")
    ax0.plot([0, n + 1], [0, 0], color="red", linestyle="solid")
    ax0.plot(cusumLine, color="black", linestyle="solid")
    ax0.set_ylabel("CUSUM")
    # Plot CUSUMsq
    bands = np.column_stack((-.32894 + t / n, .32894 + t / n))
    ax1.set_xlim(0, n + 1)
    ax1.plot(bands, color="red", linestyle="dotted")
    ax1.plot(t / n, color="red", linestyle="solid")
    ax1.plot(cusumsq, color="black", linestyle="solid")
    ax1.set_ylabel("CUSUMsq")
    plt.show(block=False)


def varTest(x, parts=1/3):
    """
    varTest
    Homoscedasticity tests

    Inputs:
    - y: a numpy vector or a Pandas time series
    - parts: fraction of the sample to estimate variances

    Author: Diego J. Pedregal
    """
    x = obj2array(x)
    x = x[~np.isnan(x)]
    n = len(x)
    n1 = int(np.floor(n * parts))
    varStat = np.nanvar(x[:n1]) / np.nanvar(x[-n1:])
    if varStat > 1:
        varStat = 1 / varStat
    pval = stats.f.cdf(varStat, n1, n1)
    out = pd.DataFrame({
        "Portion_of_data": [np.round(parts, 4)],
        "F_statistic": [np.round(varStat, 4)],
        "p.value": [np.round(pval, 4)]
    })
    out.index = [""]
    return out


def conv(*args):
    """
    1D convolution: filtering or polynomial multiplication

    *args: list of vectors to convolute

    Returns:
    Convolution of all input vectors

    Author: Diego J. Pedregal
    """
    n = len(args)
    if n > 2:
        return conv(args[0], conv(*args[1:]))
    else:
        # Convolution of two vectors
       return np.convolve(args[0], args[1])


def armaFilter(MA, AR, y):
    """
    Filter of time series

    MA: MA numerator polynomial
    AR: AR denominator polynomial
    y: a vector, ts or tsibble object

    Returns:
    Filtered time series

    Author: Diego J. Pedregal
    """
    # Filtering a time series with linear filter
    if isinstance(y, pd.Series) or isinstance(y, pd.DataFrame):
        xs = y.values
        y.t = y.index
        timeSeries = True
    else:
        xs = y
        timeSeries = False
    q = len(MA)
    p = len(AR) - 1
    x = np.convolve(np.array(xs, dtype=float), MA)
    if p > 0:
        if isinstance(AR, list):
            ARpoly = -np.array(AR[1:])
        for t in range(p, len(y)):
            x[t] += sum(ARpoly * x[t - p : t])
        x = x[:len(xs)]
        if timeSeries:
            x = pd.Series(x[:len(xs)], index=y.index)
            x = x[:len(xs)]
    else:
        if timeSeries:
            x = pd.Series(x[q-1:len(xs)], index=y.index[q-1:])
        else:
            x = x[q-1:len(xs)]
    return x


def dif(y, difs=[1], seas=[1]):
    """
    Discrete differencing of time series

    y: a vector, ts or tsibble object
    difs: vector with differencing orders
    seas: vector of seasonal periods

    Returns:
    Differenced time series

    Author: Diego J. Pedregal
    """
    # Mixture of differences operating on x
    n = len(difs)
    pol = np.array([1])
    for i in range(n):
        poli = np.concatenate(([1], np.zeros(seas[i] - 1), [-1]))
        if difs[i] > 0:
            for j in range(difs[i]):
                pol = np.convolve(pol, poli)
    dx = armaFilter(pol, [1], y)
    dx = dx[:len(y) - len(pol) + 1]
    return dx


def roots(x):
    """
    Roots of polynomial

    x: coefficients of polynomial in descending order

    Returns:
    Roots of polynomial

    Author: Diego J. Pedregal
    """
    # Roots of a polynomial
    if isinstance(x, list):
        x = np.array(x)
    if len(x) > 1:
        return np.roots(x)
    else:
        return None


def zplane(MApoly=[1], ARpoly=[1]):
    """
    Real-imaginary plane to show roots of digital filters (ARMA)

    MApoly: coefficients of numerator polynomial in descending order
    ARpoly: coefficients of denominator polynomial in descending order

    Author: Diego J. Pedregal
    """
    if isinstance(MApoly, list):
        MApoly = np.array(MApoly)
    if isinstance(ARpoly, list):
        ARpoly = np.array(ARpoly)
    # zplane plot
    arRoots = np.roots(ARpoly)
    maRoots = np.roots(MApoly)
    x = np.arange(-1, 1, 0.005)
    y = np.sqrt(1 - x ** 2)
    # Dibujando círculo
    fig, ax = plt.subplots()
    # Añadiendo raices
    if len(arRoots) > 0:
        modAR = np.abs(arRoots)
        # Stationary
        aux = arRoots[modAR < 0.99]
        if len(aux) > 0:
            plt.plot(np.real(aux), np.imag(aux), 'bx', markersize=6)
        # Non-stationary
        aux = arRoots[modAR >= 0.99]
        if len(aux) > 0:
            plt.plot(np.real(aux), np.imag(aux), 'rx', markersize=6)
    if len(maRoots) > 0:
        # Inverible
        modMA = np.abs(maRoots)
        aux = maRoots[modMA < 0.99]
        if len(aux) > 0:
            plt.plot(np.real(aux), np.imag(aux), 'bo', markersize=6)
        # Non-invertible
        aux = maRoots[modMA >= 0.99]
        if len(aux) > 0:
            plt.plot(np.real(aux), np.imag(aux), 'ro', markersize=6)
    ylim = ax.get_ylim()
    xlim = ax.get_xlim()
    xlim = (min(xlim[0], -1) - 0.1, max(xlim[1], 1) + 0.1)
    ylim = (min(ylim[0], -1) - 0.1, max(ylim[1], 1) + 0.1)
    # Crear el círculo
    circulo = plt.Circle((0, 0), 1, edgecolor='black', facecolor='none', linestyle='dotted')
    ax.add_patch(circulo)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal')
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    plt.axhline(y=0, color="black", linestyle="dotted")
    plt.axvline(x=0, color="black", linestyle="dotted")
    plt.title("Poles (x - AR) and zeros (o - MA)")
    plt.show(block=False)


def arma2tsi(MApoly, ARpoly, n=100):
    """
    AR polynomial coefficients of ARMA model

    MApoly: coefficients of numerator polynomial in descending order
    ARpoly: coefficients of denominator polynomial in descending order
    n: number of coefficients

    Returns:
    Time series representation of the ARMA model

    Author: Diego J. Pedregal
    """
    # Converts ARMA to pure AR
    return armaFilter(MApoly, ARpoly, [1] + [0] * (n - 1))


def acft(MApoly=[1], ARpoly=[1], ncoef=38, s=1):
    """
    Theoretical autocorrelation functions of ARMA models
    Inputs:
        MApoly: coefficients of numerator polynomial in descending order
        ARpoly: coefficients of denominator polynomial in descending order
        ncoef: number of coefficients
        s: seasonal period, number of observations per year
    Returns:
        Theoretical autocorrelation functions

    Author: Diego J. Pedregal
    """
    # Theoretical ACF and PACF from ARMA model
    correct = True
    if len(ARpoly) > 1 and any(np.abs(np.roots(ARpoly)) >= 1):
        print('Non-stationary model')
        correct = False
    if len(MApoly) > 1 and any(np.abs(np.roots(MApoly)) >= 1):
        print('Non-invertible model')
        correct = False
    if not correct:
        print('SACF and SPACF do not exist for this model!!!')
        return np.array([])
    p = len(ARpoly) - 1
    q = len(MApoly) - 1
    out = np.ones((ncoef, 3))
    out[:, 0] = np.arange(1, ncoef + 1)
    # ACF
    aux = 250
    MAPi = np.ones(aux)
    MAP = np.array(MApoly)
    if p > 0:
        while MAPi[aux - 1] > 1e-4:
            aux += 100
            MAPi = arma2tsi(MApoly, ARpoly, aux)
        MAP = MAPi
    if len(MAP) < aux:
        MAP = np.concatenate((MAP, np.zeros(aux - len(MAP))))
    gam0 = np.sum(MAP ** 2)
    for i in range(ncoef):
        out[i, 1] = np.sum(MAP[i + 1 : aux + 1] * MAP[:(aux - i - 1)]) / gam0
    # # PACF
    out[:, 2] = pacfFun(out[:, 1])
    # fi = np.zeros(ncoef)
    # fi[0] = out[0, 1]
    # out[0, 2] = fi[0]
    #
    # for p in range(1, ncoef):
    #     fi[p] = (out[p, 1] - np.sum(fi[:p] * np.flip(out[:p, 1]))) / (1 - np.sum(fi * out[:, 1]))
    #     out[p, 2] = fi[p]
    #     fi[:p] = fi[:p] - fi[p] * np.flip(fi[:p])
    plotAcfPacf(out[:, 1], out[:, 2], s)
    out = pd.DataFrame(out, columns=["lag", "SACF", "SPACF"])
    return out


def slide(y, orig, forecFun, *args, h=12, step=1, output=True, window=None, parallel=False):
    """
    Rolling forecasting of a matrix of time series
    Inputs:
        y: a vector or matrix of time series
        orig: starting forecasting origin
        forecFun: user function that implements forecasting methods
        *args: rest of inputs to forecFun function
        h: forecasting horizon
        step: observations ahead to move the forecasting origin
        output: output TRUE/FALSE
        window: fixed window width in number of observations (None for non-fixed)
        parallel: run forecasts in parallel
    Returns:
        A vector with all the dimensions

    Author: Diego J. Pedregal
    """
    # Rolling for nSeries
    # out = [h, nOrigs, nModels, nSeries]
    if y.ndim == 1:
        y = y.reshape(-1, 1)
    nSeries = y.shape[1]
    n = y.shape[0]
    dataList = [y[:, j] for j in range(nSeries)]
    nOr = len(range(orig, n - h + 1, step))
    if not parallel or (nSeries == 1 and nOr == 1):
        listOut = [slideAux(data, orig, forecFun, h, step, output, False, window, False, *args) for data in dataList]
    else:
        if nSeries > 1:
            with mp.Pool() as pool:
                listOut = pool.starmap(slideAux,
                                       [(data, orig, forecFun, h, step, output, False, window, False, *args) for data in
                                        dataList])
        elif nOr > 1:
            listOut = [slideAux(data, orig, forecFun, h, step, output, False, window, True, *args) for data in dataList]
    out = np.empty(listOut[0].shape + (nSeries,))
    for i in range(nSeries):
        out[:, :, :, i] = listOut[i]
    return out

def slideAux(y, orig, forecFun, h=12, step=1, output=True, graph=True, window=None, parallel=False, *args, **kwargs):
    """
    Auxiliary function run from slide
    Inputs:
        y: a vector or matrix of time series
        orig: starting forecasting origin
        forecFun: user function that implements forecasting methods
        h: forecasting horizon
        step: observations ahead to move the forecasting origin
        output: output TRUE/FALSE
        graph: graphical output TRUE/FALSE
        window: fixed window width in number of observations (None for non-fixed)
        parallel: run forecasts in parallel
        *args, **kwargs: rest of inputs to forecFun function
    Returns:
        Next time stamp

    Author: Diego J. Pedregal
    """
    # Rolling for 1 series
    # out = [h, nOrigs, nModels]
    n = len(y)
    origs = range(orig, n - h + 1, step)
    nOr = len(origs)
    if window is None:
        outi = forecFun(y[:orig], h, *args, **kwargs)
    else:
        outi = forecFun(y[orig - window + 1:orig], h, *args, **kwargs)
    outi = np.array(outi)
    if outi.ndim > 1:
        nMethods = outi.shape[1]
    else:
        nMethods = 1
        outi = np.reshape(outi, (-1, 1))
    out = np.empty((h, nOr, nMethods))
    out[:, 0, :] = outi
    # colnames = list(outi.columns)
    dataList = []
    if nOr > 1:
        for j in range(1, nOr):
            if window is None:
                dataList.append(y[:orig + j])
            else:
                dataList.append(y[orig - window + step:orig + j])
    if parallel:
        with mp.Pool() as pool:
            listOut = pool.map(forecFun, dataList, (h, ) + args)
    else:
        listOut = [forecFun(data, h, *args, **kwargs) for data in dataList]
    if nOr > 1:
        for i in range(1, nOr):
            if nMethods == 1:
                out[:, i, :] = np.reshape(np.array(listOut[i - 1]), (-1, 1))
            else:
                out[:, i, :] = np.array(listOut[i - 1])
    if output:
        return out


def plotSlide(py1, y, orig, step=1, errorFun=None, collectFun=np.mean):
    """
    Plot summarised results from slide
    Inputs:
        py1 output from slide function
        y a vector or matrix of time series (the same used in slide call)
        orig starting forecasting origin (the same used in slide call)
        step observations ahead to move the forecasting origin (the same used in slide call)
        errorFun user function to calculate error measures
        collectFun aggregation function (mean, median, etc.)
    Returns:
        Errors table

    Author: Diego J. Pedregal
    """
    # py1 = [h, nOrigs, nModels, nSeries]
    h = py1.shape[0]
    nOrigs = py1.shape[1]
    nMethods = py1.shape[2]
    nSeries = py1.shape[3]
    if pd.isna(nSeries):
        nSeries = 1
        py = np.empty((h, nOrigs, nMethods, 1))
        py[:, :, :, 0] = py1
    else:
        py = py1
    # y = np.array(y)
    metrics = np.empty((h, nMethods))
    outj = np.empty((h, nOrigs, nMethods, nSeries))
    for i in range(nOrigs):
        actuali = y[:orig + (i - 1) * step + h, :]
        aux = py[:, i, :, :].copy()
        # aux = pd.DataFrame(aux, columns=np.arange(1, nMethods + 1))
        if nSeries == 1:
            for j in range(nMethods):
                outj[:, i, j, 0] = errorFun(aux[:, j], actuali)
        else:
            for k in range(nSeries):
                for j in range(nMethods):
                    outj[:, i, j, k] = errorFun(aux[:, j, k], actuali[:, k])
    for m in range(nMethods):
        for j in range(h):
            metrics[j, m] = collectFun(outj[j, :, m])
    plotH = pd.DataFrame(metrics, index=np.arange(1, h + 1))
    plt.plot(plotH)
    plt.ylabel("Error metric")
    plt.show(block=False)
    return outj


def Accuracy(py, y, collectFun=np.mean):
    """
    Accuracy for 1 time series y and several forecasting
    methods py and h steps ahead py is h x nMethods x nSeries
    Inputs:
        py:         matrix of forecasts (h x nMethods x nForecasts)
        y:          a matrix of actual values (n x nForecasts)
        s:          seasonal period, number of observations per year
        collectFun: aggregation function (mean, median, etc.)
    Returns:
        Table of results

    Author: Diego J. Pedregal
    """
    # Accuracy for 1 time series y and several forecasting methods py and h steps ahead
    # py is h x nMethods x nSeries
    # y is n x nSeries
    spy = len(py.shape)
    if (isinstance(py, pd.Series) or isinstance(py, pd.DataFrame)) and isinstance(y, pd.Series):
        tpy = py.index
        ty = y.index
        if min(tpy) - max(ty) > 1e-5:
            raise ValueError("No errors to estimate, check dates!!!")
        if max(tpy) - max(ty) > 1e-5:
            # Cut forecasts
            py = py.head(np.where(max(ty) == tpy)[0])
        if max(ty) - max(tpy) > 1e-5:
            # Cut time series
            y = y.head(np.where(max(tpy) == ty)[0])
    if spy == 1:
        raise ValueError("Input 'py' should be: h x number of methods x number of series!!!")
    elif spy == 2:
        # aux = np.empty((py.shape[0], py.shape[1], 1))
        # aux[:, :, :] = py
        # aux = np.asmatrix(aux)
        py = np.reshape(py, (py.shape[0], py.shape[1], 1))
        # y = np.asarray(y)
    h = py.shape[0]
    ny = py.shape[1]
    nSeries = py.shape[2]
    n = y.shape[0]
    if y.ndim == 1:
        y = np.reshape(y, (y.shape[0], 1))
    # if nSeries == 1:
    #     y = tsfile.ts(y, start=start(y), frequency=frequency(y))
    insample = False
    if n > h:
        insample = True
    elif n < h:
        raise ValueError("Insample data should be longer than forecasting horizon!!!")
    out = np.empty((ny, 7 + 3 * insample))
    rownames = [str(i) for i in range(1, ny + 1)]
    colnames = ["ME", "RMSE", "MAE", "MPE", "PRMSE", "MAPE", "sMAPE"]
    if insample:
        colnames.extend(["MASE", "RelMAE", "Theil's U"])
    out = np.zeros((len(rownames), len(colnames)))
    # out.index.name = colnames(py)
    for i in range(ny):
        e = py[:, i, :] - y[-h:, :]
        p = 100 * e / y[-h:, :]
        aux = np.stack((np.nanmean(e, axis=0),
                              np.sqrt(np.nanmean(e * e, axis=0)),
                              np.nanmean(np.abs(e), axis=0),
                              np.nanmean(p, axis=0),
                              np.sqrt(np.nanmean(p * p, axis=0)),
                              np.nanmean(np.abs(p), axis=0),
                              np.nanmean(200 * np.abs(e) / (py[:, i, :] + y[-h:, :]), axis=0)),
                             axis=0)
        if insample:
            theil = 100 * (y[-h:, :] - y[(n - h):(n - 1), :]) / y[-h:, :]
            fRW = y[(s + 1):(n - h), :] - y[1:(n - h - s), :]
            if nSeries == 1:
                fRW = np.reshape(fRW, (len(fRW), 1))
            aux = np.column_stack((aux,
                                   np.nanmean(np.abs(e), axis=0) / np.nanmean(np.abs(fRW), axis=0),
                                   np.nansum(np.abs(e), axis=0) / np.nansum(np.abs(fRW), axis=0),
                                   np.sqrt(np.nansum(p * p, axis=0) / np.nansum(theil * theil, axis=0))))
        out[i, :] = collectFun(aux, axis=1)
    return pd.DataFrame(out, index=rownames, columns=colnames)


def tsDisplay(y, nCoef=None, nPar=0):
    """
    tsDisplay
    Displays a time series plot with autocorrelation functions

    Inputs:
    - y: a numpy vector or a Pandas time series object
    - nCoef: number of autocorrelation coefficients to estimate
    - nPar: number of parameters in a model if y is a residual
    - s: seasonal period, number of observations per year

    Author: Diego J. Pedregal
    """
    if isinstance(y, pd.Series) or isinstance(y, pd.DataFrame):
        s = y.resample('Y').count()[1]
    else:
        s = 1
    # x = obj2array(y)
    # if s is None:
    #     s = frequency(x)
    fig = plt.figure(figsize=(8, 6))
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.plot(y)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Value')
    ax2 = fig.add_subplot(2, 2, 3)
    ax3 = fig.add_subplot(2, 2, 4)
    out = ident(y, nCoef, nPar, True)
    plotAcfPacf(np.array(out["SACF"]), np.array(out["SPACF"]), s, len(y), [ax2, ax3])
    plt.show(block=False)


def tests(x, parts=1/3, nCoef=None, nPar=0, avoid=16):
    """
    Tests on a time series

    y: a vector, ts or tsibble object
    parts: proportion of sample to include in ratio of variances test
    nCoef: number of autocorrelation coefficients to estimate
    nPar: number of parameters in a model if y is a residual
    s: seasonal period, number of observations per year
    avoid: number of observations to avoid at beginning of sample to eliminate initial effects

    Author: Diego J. Pedregal
    """
    if isinstance(x, pd.Series) or isinstance(x, pd.DataFrame):
        s = x.resample('Y').count()[1]
    else:
        s = 1
    print("Summary statistics:")
    print("===================")
    print(sumStats(x))
    print("Autocorrelation tests:")
    print("=====================")
    nCoef = min(25, len(x) / 4)
    # Plot figure
    fig = plt.figure(figsize=(8, 6))
    ax1 = fig.add_subplot(4, 1, 1)
    ax1.plot(x)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Value')
    ax2 = fig.add_subplot(4, 2, 3)
    ax3 = fig.add_subplot(4, 2, 4)
    out = ident(x, nCoef, nPar, [ax2, ax3])
    plotAcfPacf(np.array(out["SACF"]), np.array(out["SPACF"]), s, len(x), [ax2, ax3])
    print(out)
    ax4 = fig.add_subplot(4, 2, 5)
    ax5 = fig.add_subplot(4, 2, 6)
    pGAUSS = gaussTest(x, [ax4, ax5])
    print("Ratio of variance tests:")
    print("=======================")
    out1 = varTest(x, parts)
    ax4 = fig.add_subplot(4, 2, 7)
    ax5 = fig.add_subplot(4, 2, 8)
    pCUSUM = cusum(x, [ax4, ax5])
    # Plotting
    plt.show(block=False)

