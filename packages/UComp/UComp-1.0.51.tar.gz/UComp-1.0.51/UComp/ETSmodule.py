# Compile with:
# c++ -O3 -Wall -shared -std=c++11 -undefined dynamic_lookup -I/Library/Frameworks/Python.framework/Headers
# -I"/Users/diego.pedregal/Google Drive/C++/armadillo-10.8.2/include" -llapack -lblas $(python3 -m
# pybind11 --includes) pythonBSM.cpp -o BSMc$(python3-config --extension-suffix)
import numpy as np
import pandas as pd


if False:           # To run locally
    import ETSc
else:              # To run from package in PyPI
    from UComp import ETSc
    from UComp import tsfile


class ETSmodel:
    """
    ETSmodel
    Estimates and forecasts a general ETS model

    Inputs:
    - y: a time series to forecast (can be a numerical vector or a time series object).
         This is the only required input. If it is a vector, the 's' input should be supplied compulsorily (see below).
    - s: seasonal period of the time series (1 for annual, 4 for quarterly, ...)
    - u: a matrix of input time series. If the output is to be forecasted, matrix 'u' should contain future
         values for inputs.
    - model: the model to estimate. It is a single string indicating the type of model for each component with one or two letters:
             - Error: ? / A / M
             - Trend: ? / N / A / Ad / M / Md
             - Seasonal: ? / N / A / M
    - h: forecast horizon. If the model includes inputs, 'h' is not used, the length of 'u' is used instead.
    - criterion: information criterion for identification ("aic", "bic", or "aicc").
    - lambda_: Box-Cox lambda parameter (None: estimate)
    - armaIdent: check for ARMA models for error component (True / False).
    - identAll: run all models to identify the best one (True / False)
    - forIntervals: estimate forecasting intervals (True / False)
    - bootstrap: use bootstrap simulation for predictive distributions
    - nSimul: number of simulation runs for bootstrap simulation of predictive distributions
    - verbose: intermediate estimation output (True / False)
    - alphaL: constraints limits for alpha parameter
    - betaL: constraints limits for beta parameter
    - gammaL: constraints limits for gamma parameter
    - phiL: constraints limits for phi parameter
    - p0: initial values for parameter search (alpha, beta, phi, gamma) with constraints:
          - 0 < alpha < 1
          - 0 < beta < alpha
          - 0 < phi < 1
          - 0 < gamma < 1 - alpha

    Returns:
    An object of class 'ETS'. See 'ETSmodel'.

    See Also:
        ETSmodel, PTS, PTSmodel, UC

    Author: Diego J. Pedregal
    """
    def __init__(self, y: pd.DataFrame, s: int = np.nan, u: np.array = np.array([]), model: str = "???",
                 h: int = 24, criterion: str = "aicc",
                 armaIdent: bool = False, identAll: bool = False, forIntervals: bool = False,
                 bootstrap: bool = False, nSimul: int = 5000, verbose: bool = False,
                 alphaL: np.array = np.array([0, 1]), betaL: np.array = np.array([0, 1]),
                 gammaL: np.array = np.array([0, 1]), phiL: np.array = np.array([0.8, 0.98]),
                 p0: np.array = np.array([-99999]), lambdaBoxCox: np.array = np.array(1.0)):
        if isinstance(y, np.ndarray) and np.isnan(s):
            raise ValueError("Either 'y' should be a Panda time series or 's' should be supplied!!")
        if isinstance(y, pd.Series) or isinstance(y, pd.DataFrame):
            s = y.resample('Y').count()[1]
        self.y = y
        self.u = u
        self.model = model
        self.s = s
        self.h = h
        self.p0 = p0
        self.criterion = criterion
        self.armaIdent = armaIdent
        self.identAll = identAll
        self.forIntervals = forIntervals
        self.bootstrap = bootstrap
        self.nSimul = nSimul
        self.verbose = verbose
        self.alphaL = alphaL
        self.betaL = betaL
        self.gammaL = gammaL
        self.phiL = phiL
        self.yFor = np.empty((0, 0))
        self.yForV = np.empty((0, 0))
        self.comp = np.empty((0, 0))
        self.ySimul = np.empty((0, 0))
        self.table = ""
        self.p = np.empty((0, 0))
        self.lambdaBoxCox = lambdaBoxCox
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
        if np.isnan(lambdaBoxCox):
            lambdaBoxCox = 9999.9
        m1 = ETSc.ETSfunC("estimate", y, u.flatten(), rowu, colu, model, s, h, verbose, criterion,
                          identAll, alphaL, betaL, gammaL, phiL, "standard", forIntervals,
                          bootstrap, nSimul, np.array([0, 0]), armaIdent, p0, lambdaBoxCox)
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
            self.model = m1.model
            self.p = np.array(m1.p)
            self.lambdaBoxCox = lambdaBoxCox
            if bootstrap:
                self.ySimul = np.array(m1.ySimul)
                self.ySimul = self.ySimul.reshape((len(self.ySimul) // nSimul, nSimul))


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
        m1 = ETSc.ETSfunC("components", self.y, u.flatten(), rowu, colu, self.model, self.s, self.h, False,
                          self.criterion, self.identAll, self.alphaL, self.betaL, self.gammaL, self.phiL,
                          "standard", False, False, 0, np.array([0, 0]), self.armaIdent, self.p0, self.lambdaBoxCox)
        self.compNames = m1.compNames
        nComp = m1.compNames.count('/') + 1
        self.comp = np.array(m1.comp)
        self.comp = np.transpose(self.comp.reshape((nComp, len(self.comp) // nComp)))
        self.comp = tsfile.ts(self.comp, self.y.index[0], self.y.index.freq)
        if not isinstance(self.y, np.ndarray):
            self.comp = tsfile.ts(self.comp, self.y.index[0], self.y.index.freq)


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
        m1 = ETSc.ETSfunC("validate", self.y, u.flatten(), rowu, colu, self.model, self.s, self.h, False,
                          self.criterion, self.identAll, self.alphaL, self.betaL, self.gammaL, self.phiL,
                          "standard", False, False, 0, np.array([0, 0]), self.armaIdent, self.p0, self.lambdaBoxCox)
        self.compNames = m1.compNames
        nComp = m1.compNames.count('/') + 1
        self.comp = np.array(m1.comp)
        self.comp = np.transpose(self.comp.reshape((nComp, len(self.comp) // nComp)))
        self.comp = tsfile.ts(self.comp, self.y.index[0], self.y.index.freq)
        if not isinstance(self.y, np.ndarray):
            self.comp = tsfile.ts(self.comp, self.y.index[0], self.y.index.freq)
        self.table = ' '.join([str(i) for i in m1.table])
        if show:
            print(self.table)


def ETS(y: np.array, s: int = np.nan, u: np.array = np.array([]), model: str = "???",
        h: int = 24, criterion: str = "aicc",
        armaIdent: bool = False, identAll: bool = False, forIntervals: bool = False,
        bootstrap: bool = False, nSimul: int = 5000, verbose: bool = False,
        alphaL: np.array = np.array([0, 1]), betaL: np.array = np.array([0, 1]),
        gammaL: np.array = np.array([0, 1]), phiL: np.array = np.array([0.8, 0.98]),
        p0: np.array = np.array([-99999]), lambdaBoxCox: np.array = np.array(1.0)):
    """
    ETSmodel
    Estimates and forecasts a general ETS model

    Inputs:
    - y: a time series to forecast (can be a numerical vector or a time series object).
         This is the only required input. If it is a vector, the 's' input should be supplied compulsorily (see below).
    - s: seasonal period of the time series (1 for annual, 4 for quarterly, ...)
    - u: a matrix of input time series. If the output is to be forecasted, matrix 'u' should contain future
         values for inputs.
    - model: the model to estimate. It is a single string indicating the type of model for each component with one or two letters:
             - Error: ? / A / M
             - Trend: ? / N / A / Ad / M / Md
             - Seasonal: ? / N / A / M
    - h: forecast horizon. If the model includes inputs, 'h' is not used, the length of 'u' is used instead.
    - criterion: information criterion for identification ("aic", "bic", or "aicc").
    - lambda_: Box-Cox lambda parameter (None: estimate)
    - armaIdent: check for ARMA models for error component (True / False).
    - identAll: run all models to identify the best one (True / False)
    - forIntervals: estimate forecasting intervals (True / False)
    - bootstrap: use bootstrap simulation for predictive distributions
    - nSimul: number of simulation runs for bootstrap simulation of predictive distributions
    - verbose: intermediate estimation output (True / False)
    - alphaL: constraints limits for alpha parameter
    - betaL: constraints limits for beta parameter
    - gammaL: constraints limits for gamma parameter
    - phiL: constraints limits for phi parameter
    - p0: initial values for parameter search (alpha, beta, phi, gamma) with constraints:
          - 0 < alpha < 1
          - 0 < beta < alpha
          - 0 < phi < 1
          - 0 < gamma < 1 - alpha

    Returns:
    An object of class 'ETS'. See 'ETSmodel'.

    See Also:
        ETSmodel, PTS, PTSmodel, UC

    Author: Diego J. Pedregal
    """
    m = ETSmodel(y, s, u, model, h, criterion, armaIdent, identAll, forIntervals,
                 bootstrap, nSimul, verbose, alphaL, betaL, gammaL, phiL, p0, lambdaBoxCox)
    m.validate(m.verbose)
    return m

