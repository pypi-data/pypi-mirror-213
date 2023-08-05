# Compile with:
# c++ -O3 -Wall -shared -std=c++11 -undefined dynamic_lookup -I/Library/Frameworks/Python.framework/Headers
# -I"/Users/diego.pedregal/Google Drive/C++/armadillo-10.8.2/include" -llapack -lblas $(python3 -m
# pybind11 --includes) pythonBSM.cpp -o BSMc$(python3-config --extension-suffix)
import numpy as np
import pandas as pd


if False:           # To run locally
    import UCc
else:              # To run from package in PyPI
    from UComp import UCc
    from UComp import tsfile


class UCmodel:
    """
    UCmodel
    Estimates and forecasts UC general time series models

    Inputs:
    - y: a time series to forecast (can be a numerical vector or a time series object).
         This is the only required parameter. If it is a vector, the 'periods' parameter
         must be provided compulsorily (see below).
    - u: a matrix of external regressors included only in the observation equation.
         (can be a numerical vector or a time series object). If the output is to be forecasted,
         matrix 'u' should contain future values for inputs.
    - model: the model to estimate. It is a single string indicating the type of model for each component.
             It allows two formats: "trend/seasonal/irregular" or "trend/cycle/seasonal/irregular".
             The possibilities available for each component are:
             - Trend: ? / none / rw / irw / llt / dt / td;
             - Seasonal: ? / none / equal / different;
             - Irregular: ? / none / arma(0, 0) / arma(p, q) - with p and q positive integer orders.
    - outlier: critical level of outlier tests. If NA, it does not carry out any outlier detection (default).
               A positive value indicates the critical minimum t-test for outlier detection in any
               model during identification. Three types of outliers are identified, namely Additive Outliers (AO),
               Level Shifts (LS), and Slope Change (SC).
    - stepwise: stepwise identification procedure (True / False).
    - tTest: augmented Dickey Fuller test for unit roots used in the stepwise algorithm (True / False).
             The number of models to search for is reduced, depending on the result of this test.
    - p0: initial parameter vector for optimization search.
    - h: forecast horizon. If the model includes inputs, 'h' is not used, the length of 'u' is used instead.
    - lambda_: Box-Cox transformation lambda, None for automatic estimation.
    - criterion: information criterion for identification ("aic", "bic", or "aicc").
    - periods: vector of fundamental period and harmonics required.
    - verbose: intermediate results shown about progress of estimation (True / False).
    - arma: check for ARMA models for irregular components (True / False).
    - TVP: vector of zeros and ones to indicate TVP parameters.
    - trendOptions: trend models to select amongst (e.g., "rw/llt").
    - seasonalOptions: seasonal models to select amongst (e.g., "none/different").
    - irregularOptions: irregular models to select amongst (e.g., "none/arma(0,1)").

    Returns:
    An object of class 'UComp'. It is a list with fields including all the inputs and
    the fields listed below as outputs. All the functions in this package fill in
    part of the fields of any 'UComp' object as specified in what follows (function
    'UC' fills in all of them at once):

    After running 'UCmodel':
    - p: Estimated parameters
    - v: Estimated innovations (white noise in correctly specified models)
    - yFor: Forecasted values of output
    - yForV: Variance of forecasts
    - criteria: Value of criteria for estimated model
    - iter: Number of iterations in estimation
    - grad: Gradient at estimated parameters
    - covp: Covariance matrix of parameters

    After running 'object.validate':
    - table: Estimation and validation table

    After running 'object.components':
    - comp: Estimated components in matrix form
    - compV: Estimated components variance in matrix form

    After running 'UCfilter', 'UCsmooth', or 'UCdisturb':
    - yFit: Fitted values of output
    - yFitV: Estimated fitted values variance
    - a: State estimates
    - P: Variance of state estimates
    - aFor: Forecasts of states
    - PFor: Forecasts of states variances

    After running 'object.disturb':
    - eta: State perturbations estimates
    - eps: Observed perturbations estimates

    See Also:
        PTS, PTSmodel, UC, ETS, ETSmodel

    Author: Diego J. Pedregal
    """
    def __init__(self, y: pd.DataFrame, s: int = np.nan, u: np.array = np.array([]), model: str = "?/none/?/?",
                 h: int = 9999, lambdaBoxCox: np.array = np.array(1.0), outlier: float = 9999.0, tTest: bool = False,
                 criterion: str = "aic", periods: np.array = np.array([np.nan]), verbose: bool = False,
                 stepwise: bool = False, p0: np.array = np.array([-9999.9]), arma: bool = False,
                 TVP: np.array = np.array([0.0]),
                 trendOptions: str = "none/rw/llt/dt", seasonalOptions: str = "none/equal/different",
                 irregularOptions: str = "none/arma(0,0)", MSOE: bool = False, PTSnames: bool = False):
        if isinstance(y, np.ndarray) and np.isnan(s):
            raise ValueError("Either 'y' should be a Panda time series or 's' should be supplied!!")
        if isinstance(y, pd.Series) or isinstance(y, pd.DataFrame):
            s = y.resample('Y').count()[1]
        if np.isnan(lambdaBoxCox):
            lambdaBoxCox = np.array([9999.9])
        if (any(np.isnan(TVP)) and u.size != 0):
           TVP = np.zeros(u.shape)
        if (any(np.isnan(TVP))):
            TVP = -9999.99
        # if s == 1:
        #     periods = np.array([1.0]);
        if any(np.isnan(periods)):
            periods = np.array(s / (np.arange(np.floor(s / 2)) + 1))
        periods = np.reshape(periods, (-1, 1))
        # Creating class
        self.y = y
        self.s = s
        self.u = u
        self.model = model
        self.h = h
        self.outlier = -abs(outlier)
        self.tTest = tTest
        self.criterion = criterion
        self.periods = periods
        self.verbose = verbose
        self.stepwise = stepwise
        self.p0 = p0
        self.arma = arma
        self.comp = np.empty((0, 0))
        self.compV = np.empty((0, 0))
        self.p = np.empty((0, 0))
        self.covp = np.empty((0, 0))
        self.grad = np.empty((0, 0))
        self.v = np.empty((0, 0))
        self.yFit = np.empty((0, 0))
        self.yFor = np.empty((0, 0))
        self.yFitV = np.empty((0, 0))
        self.yForV = np.empty((0, 0))
        self.a = np.empty((0, 0))
        self.P = np.empty((0, 0))
        self.eta = np.empty((0, 0))
        self.eps = np.empty((0, 0))
        self.table = ""
        self.iter = 0
        self.criteria = np.empty((0, 0))
        self.lambdaBoxCox = lambdaBoxCox
        self.TVP = TVP
        self.trendOptions = trendOptions
        self.seasonalOptions = seasonalOptions
        self.irregularOptions = irregularOptions
        class hidden:
            d_t: int = 0
            estimOk: str = "Not estimated"
            objFunValue: float = 0.0
            innVariance: float = 1.0
            nonStationaryTerms: int = 0
            ns: np.array = np.array([np.nan])
            nPar: np.array = np.array([np.nan])
            harmonics: np.array = np.array([np.nan])
            rhos = np.ones((len(periods), 1))
            constPar: np.array = np.array([np.nan])
            typePar: np.array = np.array([np.nan])
            cycleLimits: np.array = np.array([np.nan])
            typeOutliers: np.array = np.array([-1, -1])
            truePar: np.array = np.array([np.nan])
            beta: np.array = np.array([np.nan])
            betaV: np.array = np.array([np.nan])
            seas: int = s
            truePar: np.array = np.array([np.nan])
            MSOE: bool = False
            PTSnames: bool = False
        hidden.MSOE = MSOE
        hidden.PTSnames = PTSnames
        self.hidden = hidden
        # End of class creation
        if u.size == 0:
            u = np.array([-99999])
            rowu = 0
            colu = 0
        else:
            if len(u.shape) == 1:
                rowu = 1
                colu = u.shape[0]
            else:
                rowu, colu = u.shape
            if rowu > colu:
                u = np.transpose(u)
                rowu, colu = u.shape
        kInitial = rowu


        m1 = UCc.UCfunC("estimate", self.y, u.flatten(), rowu, colu, self.model, self.periods, self.hidden.rhos,
                        self.h, self.tTest, self.criterion, self.hidden.truePar, self.verbose, self.stepwise,
                        self.hidden.estimOk, self.p0, self.v, self.yFitV, self.hidden.nonStationaryTerms,
                        self.hidden.harmonics, self.criteria, self.hidden.beta, self.hidden.betaV, self.hidden.d_t,
                        self.hidden.innVariance, self.hidden.objFunValue,
                        self.outlier, self.arma, self.iter, self.hidden.seas, self.grad, self.hidden.constPar,
                        self.hidden.typePar, self.hidden.ns,
                        self.hidden.nPar, self.hidden.cycleLimits.flatten(), self.hidden.cycleLimits.shape[0], self.hidden.typeOutliers,
                        self.hidden.typeOutliers.shape[0], self.hidden.MSOE, self.hidden.PTSnames, self.lambdaBoxCox, self.TVP,
                        self.trendOptions, self.seasonalOptions, self.irregularOptions)
        if m1.model != "error":  # ERROR!!!
            if isinstance(y, np.ndarray):
                yFor = np.array(m1.yFor)
            else:
                tNext = pd.date_range(y.index[-1], periods=2, freq=y.index.freq)[1]
                yFor = tsfile.ts(np.array(m1.yFor), tNext, y.index.freq)
            if yFor.size != 0:
                self.yFor = yFor
                if isinstance(y, np.ndarray):
                    self.yForV = np.array(m1.yForV)
                else:
                    self.yForV = tsfile.ts(np.array(m1.yForV), tNext, y.index.freq)
#            if (regexp(sys.model, '\?'))
#                sys.model = model;
#            end
            self.model = m1.model
            self.periods = np.array(m1.periods)
            self.hidden.cycleLimits = np.array(m1.cycleLimits)
            if self.hidden.cycleLimits.size > 1:
                self.hidden.cycleLimits = np.reshape(self.hidden.cycleLimits, (np.floor_divide(self.hidden.cycleLimits.size, m1.rowc), m1.rowc))
            self.hidden.rhos = np.array(m1.rhos)
            if self.hidden.rhos.size == 0:
                self.hidden.rhos = np.ones((len(self.periods)))
            self.criteria = np.array(m1.criteria)
            if self.criteria.size == 1:
                self.criteria = np.reshape(self.criteria, (4, 1))
            self.outlier = m1.outlier
            self.hidden.harmonics = np.array(m1.harmonics)
            if self.hidden.harmonics.size == 0:
                self.hidden.harmonics = np.empty((len(self.periods), 1)) * np.nan
            self.hidden.truePar = np.array(m1.p)
            self.p0 = np.array(m1.p0)
            self.grad = np.array(m1.grad)
            self.lambdaBoxCox = m1.lambdaBoxCox
            self.hidden.constPar = np.array(m1.constPar)
            self.hidden.typePar = np.array(m1.typePar)
            self.hidden.d_t = m1.d_t
            self.hidden.innVariance = m1.innVariance
            self.hidden.objFunValue = m1.objFunValue
            self.hidden.beta = np.array(m1.betaAug)
            self.hidden.betaV = np.array(m1.betaAugVar)
            self.h = m1.h
            self.hidden.estimOk = m1.estimOk
            self.hidden.nonStationaryTerms = m1.nonStationaryTerms
            self.hidden.ns = np.array(m1.ns)
            self.hidden.nPar = np.array(m1.nPar)
            self.iter = m1.iter
            if self.outlier != 9999.0 and kInitial > 0:
                nu = len(self.y) + self.h
                k = self.u.size / nu
                nOut = k - kInitial
                if nOut > 0:
                    self.u = np.reshape(self.u, k, nu)
                    self.hidden.typeOutliers = np.reshape(m1.typeOutliers, (np.floor_divide(m1.typeOutliers.size, m1.rowtype), m1.rowtype))


    def components(self):
        u = self.u
        if u.size == 0:
            u = np.array([-99999])
            rowu = 0
            colu = 0
        else:
            if len(u.shape) == 1:
                rowu = 1
                colu = u.shape[0]
            else:
                rowu, colu = u.shape
            if rowu > colu:
                u = np.transpose(u)
                rowu, colu = u.shape
        m1 = UCc.UCfunC("components", self.y, u.flatten(), rowu, colu, self.model, self.periods, self.hidden.rhos,
                        self.h, self.tTest, self.criterion, self.hidden.truePar, self.verbose, self.stepwise,
                        self.hidden.estimOk, self.p0, self.v, self.yFitV, self.hidden.nonStationaryTerms,
                        self.hidden.harmonics, self.criteria, self.hidden.beta, self.hidden.betaV, self.hidden.d_t,
                        self.hidden.innVariance, self.hidden.objFunValue,
                        self.outlier, self.arma, self.iter, self.hidden.seas, self.grad, self.hidden.constPar,
                        self.hidden.typePar, self.hidden.ns,
                        self.hidden.nPar, self.hidden.cycleLimits.flatten(), self.hidden.cycleLimits.shape[0], self.hidden.typeOutliers,
                        self.hidden.typeOutliers.shape[0], self.hidden.MSOE, self.hidden.PTSnames, self.lambdaBoxCox, self.TVP,
                        self.trendOptions, self.seasonalOptions, self.irregularOptions)
        self.v = np.array(m1.v)
        self.comp = np.array(m1.comp)
        self.compV = np.array(m1.compV)
        self.comp = np.reshape(self.comp, (np.floor_divide(self.comp.size, m1.rowcomp), m1.rowcomp))
        self.compV = np.reshape(self.compV, (np.floor_divide(self.compV.size, m1.rowcomp), m1.rowcomp))
        if m1.compNames[-1] == "/":
            names = m1.compNames[:-1]
        else:
            names = m1.compNames
        names = names.split("/")
        if not isinstance(self.y, np.ndarray):
            self.v = tsfile.ts(np.array(m1.v), self.y.index[0], self.y.index.freq)
            self.comp = tsfile.ts(self.comp, self.y.index[0], self.y.index.freq)
            self.compV = tsfile.ts(self.compV, self.y.index[0], self.y.index.freq)
            self.comp.columns = names
            self.compV.columns = names
        else:
            dt = [(nombre, self.comp.dtype) for nombre in names]
            self.comp = self.comp.view(dtype=dt)
            self.compV = self.compV.view(dtype=dt)


            a = 1
        #m1.compNames = compNames
        return self


    def validate(self, show=True):
        u = self.u
        if u.size == 0:
            u = np.array([-99999])
            rowu = 0
            colu = 0
        else:
            if len(u.shape) == 1:
                rowu = 1
                colu = u.shape[0]
            else:
                rowu, colu = u.shape
            if rowu > colu:
                u = np.transpose(u)
                rowu, colu = u.shape
        m1 = UCc.UCfunC("validate", self.y, u.flatten(), rowu, colu, self.model, self.periods, self.hidden.rhos,
                        self.h, self.tTest, self.criterion, self.hidden.truePar, self.verbose, self.stepwise,
                        self.hidden.estimOk, self.p0, self.v, self.yFitV, self.hidden.nonStationaryTerms,
                        self.hidden.harmonics, self.criteria, self.hidden.beta, self.hidden.betaV, self.hidden.d_t,
                        self.hidden.innVariance, self.hidden.objFunValue,
                        self.outlier, self.arma, self.iter, self.hidden.seas, self.grad, self.hidden.constPar,
                        self.hidden.typePar, self.hidden.ns,
                        self.hidden.nPar, self.hidden.cycleLimits.flatten(), self.hidden.cycleLimits.shape[0], self.hidden.typeOutliers,
                        self.hidden.typeOutliers.shape[0], self.hidden.MSOE, self.hidden.PTSnames, self.lambdaBoxCox, self.TVP,
                        self.trendOptions, self.seasonalOptions, self.irregularOptions)
        self.table = ' '.join([str(i) for i in m1.table])
        if isinstance(self.y, np.ndarray):
            self.v = np.array(m1.v)
        else:
            self.v = tsfile.ts(np.array(m1.v), self.y.index[0], self.y.index.freq)
        if show:
            print(self.table)
        return self


    def filter_(self, smooth: str):
        u = self.u
        if u.size == 0:
            u = np.array([-99999])
            rowu = 0
            colu = 0
        else:
            if len(u.shape) == 1:
                rowu = 1
                colu = u.shape[0]
            else:
                rowu, colu = u.shape
            if rowu > colu:
                u = np.transpose(u)
                rowu, colu = u.shape
        m1 = UCc.UCfunC(smooth, self.y, u.flatten(), rowu, colu, self.model, self.periods, self.hidden.rhos,
                        self.h, self.tTest, self.criterion, self.hidden.truePar, self.verbose, self.stepwise,
                        self.hidden.estimOk, self.p0, self.v, self.yFitV, self.hidden.nonStationaryTerms,
                        self.hidden.harmonics, self.criteria, self.hidden.beta, self.hidden.betaV, self.hidden.d_t,
                        self.hidden.innVariance, self.hidden.objFunValue,
                        self.outlier, self.arma, self.iter, self.hidden.seas, self.grad, self.hidden.constPar,
                        self.hidden.typePar, self.hidden.ns,
                        self.hidden.nPar, self.hidden.cycleLimits.flatten(), self.hidden.cycleLimits.shape[0], self.hidden.typeOutliers,
                        self.hidden.typeOutliers.shape[0], self.hidden.MSOE, self.hidden.PTSnames, self.lambdaBoxCox, self.TVP,
                        self.trendOptions, self.seasonalOptions, self.irregularOptions)
        if (smooth != "disturb"):
            self.a = np.array(m1.a)
            self.P = np.array(m1.P)
            self.a = np.reshape(self.a, (np.floor_divide(self.a.size, m1.rowa), m1.rowa))
            self.P = np.reshape(self.P, (np.floor_divide(self.a.size, m1.rowa), m1.rowa))
            self.v = np.array(m1.v)
            self.F = np.array(m1.F)
            self.yFit = np.array(m1.yFit)
            if not isinstance(self.y, np.ndarray):
                self.a = tsfile.ts(self.a, self.y.index[0], self.y.index.freq)
                self.P = tsfile.ts(self.P, self.y.index[0], self.y.index.freq)
                self.v = tsfile.ts(np.array(m1.v), self.y.index[0], self.y.index.freq)
                self.F = tsfile.ts(np.array(m1.F), self.y.index[0], self.y.index.freq)
                self.yFit = tsfile.ts(np.array(m1.yFit), self.y.index[0], self.y.index.freq)
        else:
            self.eps = np.array(m1.eps)
            self.eta = np.array(m1.eta)
            self.eta = np.reshape(self.eta, (np.floor_divide(self.eta.size, m1.roweta), m1.roweta))
            if not isinstance(self.y, np.ndarray):
                self.eps = tsfile.ts(np.array(m1.eps), self.y.index[0], self.y.index.freq)
                self.eta = tsfile.ts(self.eta, self.y.index[0], self.y.index.freq)
        #m1.stateNames = statesN;


    def filter(self):
        self.filter_("filter")


    def smooth(self):
        self.filter_("smooth")


    def disturb(self):
        self.filter_("disturb")


def UC(y: np.array, s: int = np.nan, u: np.array = np.array([]), model: str = "?/none/?/?",
       h: int = 9999, lambdaBoxCox: np.array = np.array(1.0), outlier: float = 9999.0, tTest: bool = False,
       criterion: str = "aic", periods: np.array = np.array([np.nan]), verbose: bool = False,
       stepwise: bool = False, p0: np.array = np.array([-9999.9]), arma: bool = False,
       TVP: np.array = np.array([0.0]),
       trendOptions: str = "none/rw/llt/dt", seasonalOptions: str = "none/equal/different",
       irregularOptions: str = "none/arma(0,0)"):
    """
    UCmodel
    Estimates and forecasts UC general time series models

    Inputs:
    - y: a time series to forecast (can be a numerical vector or a time series object).
         This is the only required parameter. If it is a vector, the 'periods' parameter
         must be provided compulsorily (see below).
    - u: a matrix of external regressors included only in the observation equation.
         (can be a numerical vector or a time series object). If the output is to be forecasted,
         matrix 'u' should contain future values for inputs.
    - model: the model to estimate. It is a single string indicating the type of model for each component.
             It allows two formats: "trend/seasonal/irregular" or "trend/cycle/seasonal/irregular".
             The possibilities available for each component are:
             - Trend: ? / none / rw / irw / llt / dt / td;
             - Seasonal: ? / none / equal / different;
             - Irregular: ? / none / arma(0, 0) / arma(p, q) - with p and q positive integer orders.
    - outlier: critical level of outlier tests. If NA, it does not carry out any outlier detection (default).
               A positive value indicates the critical minimum t-test for outlier detection in any
               model during identification. Three types of outliers are identified, namely Additive Outliers (AO),
               Level Shifts (LS), and Slope Change (SC).
    - stepwise: stepwise identification procedure (True / False).
    - tTest: augmented Dickey Fuller test for unit roots used in the stepwise algorithm (True / False).
             The number of models to search for is reduced, depending on the result of this test.
    - p0: initial parameter vector for optimization search.
    - h: forecast horizon. If the model includes inputs, 'h' is not used, the length of 'u' is used instead.
    - lambda_: Box-Cox transformation lambda, None for automatic estimation.
    - criterion: information criterion for identification ("aic", "bic", or "aicc").
    - periods: vector of fundamental period and harmonics required.
    - verbose: intermediate results shown about progress of estimation (True / False).
    - arma: check for ARMA models for irregular components (True / False).
    - TVP: vector of zeros and ones to indicate TVP parameters.
    - trendOptions: trend models to select amongst (e.g., "rw/llt").
    - seasonalOptions: seasonal models to select amongst (e.g., "none/different").
    - irregularOptions: irregular models to select amongst (e.g., "none/arma(0,1)").

    Returns:
    An object of class 'UComp'. It is a list with fields including all the inputs and
    the fields listed below as outputs. All the functions in this package fill in
    part of the fields of any 'UComp' object as specified in what follows (function
    'UC' fills in all of them at once):

    After running 'UCmodel':
    - p: Estimated parameters
    - v: Estimated innovations (white noise in correctly specified models)
    - yFor: Forecasted values of output
    - yForV: Variance of forecasts
    - criteria: Value of criteria for estimated model
    - iter: Number of iterations in estimation
    - grad: Gradient at estimated parameters
    - covp: Covariance matrix of parameters

    After running 'object.validate':
    - table: Estimation and validation table

    After running 'object.components':
    - comp: Estimated components in matrix form
    - compV: Estimated components variance in matrix form

    After running 'UCfilter', 'UCsmooth', or 'UCdisturb':
    - yFit: Fitted values of output
    - yFitV: Estimated fitted values variance
    - a: State estimates
    - P: Variance of state estimates
    - aFor: Forecasts of states
    - PFor: Forecasts of states variances

    After running 'object.disturb':
    - eta: State perturbations estimates
    - eps: Observed perturbations estimates

    See Also:
        PTS, PTSmodel, UC, ETS, ETSmodel

    Author: Diego J. Pedregal
    """
    m = UCmodel(y, s, u, model, h, lambdaBoxCox, outlier, tTest, criterion, periods, verbose, stepwise, p0, arma,
                TVP, trendOptions, seasonalOptions, irregularOptions)
    m.validate(m.verbose)
    m.disturb()
    m.components()
    return m


