# Compile with:
# c++ -O3 -Wall -shared -std=c++11 -undefined dynamic_lookup -I/Library/Frameworks/Python.framework/Headers
# -I"/Users/diego.pedregal/Google Drive/C++/armadillo-10.8.2/include" -llapack -lblas $(python3 -m
# pybind11 --includes) pythonBSM.cpp -o BSMc$(python3-config --extension-suffix)
import numpy as np
import pandas as pd

if False:           # To run locally
    import UCmodule as uc
else:              # To run from package in PyPI
    from UComp import UCmodule as uc


def modelUC2arma(model):
    # ARMA model orders
    ar = 0
    ma = 0
    posi = model.find("arma")
    if posi == -1:
        return [ar, ma]
    posi += 5
    marma = model[posi : len(model) - 1]
    coma = marma.find(",")
    ar = int(marma[0 : coma])
    ma = int(marma[coma + 1 : len(marma)])
    return [ar, ma]


def modelUC2PTS(modelUC):
    # removing cycle from UC model
    modelUC = modelUC.replace("/none/", "/")
    # extracting components
    aux = modelUC.split("/")
    trend = aux[0]
    seasonal = aux[1]
    noise = aux[2]
    # noise
    model = "A"
    if noise == "none":
        model = "N"
    # trend
    if trend == "rw":
        model = model + "N"
    elif trend == "srw":
        model = model + "Ad"
    elif trend == "llt":
        model = model + "A"
    elif trend == "td":
        model = model + "L"
    # seasonal
    if seasonal == "none":
        model = model + "N"
    elif seasonal == "equal":
        model = model + "E"
    elif seasonal == "different":
        model = model + "D"
    elif seasonal == "linear":
        model = model + "L"
    return model


def PTS2modelUC(model, armaOrders=[0, 0]):
    modelU = ""
    n = len(model)
    # noise
    model = model.lower()
    aux = model[0]
    if aux == "?":
        modelU = "/?"
    elif aux == "n":
        modelU = "/none"
    elif aux == "a":
        modelU = "/arma({},{})".format(armaOrders[0], armaOrders[1])
    else:
        raise ValueError("ERROR: incorrect error model!!")
    # seasonal
    aux = model[-1]
    if aux == "?":
        modelU = "/?" + modelU
    elif aux == "n":
        modelU = "/none" + modelU
    elif aux == "a":
        modelU = "/linear" + modelU
    elif aux == "e":
        modelU = "/equal" + modelU
    elif aux == "d":
        modelU = "/different" + modelU
    else:
        raise ValueError("ERROR: incorrect seasonal model!!")
    # trend
    aux = model[1:n-1]
    if aux == "?":
        modelU = "?/none" + modelU
    elif aux == "n":
        modelU = "rw/none" + modelU
    elif aux == "a":
        modelU = "llt/none" + modelU
    elif aux == "ad":
        modelU = "srw/none" + modelU
    elif aux == "l":
        modelU = "td/none" + modelU
    else:
        raise ValueError("ERROR: incorrect trend model!!")
    return modelU


class PTSmodel:
    """
    Run PTS general univariate MSOE models

    Inputs:
        y:  A time series to forecast (it may be either a numpy vector or a Panda time series object).
            This is the only input required. If a vector, the additional input 's' should be supplied
            compulsorily (see below).
        s: Seasonal period of time series (1 for annual, 4 for quarterly, ...)
        u:  A matrix of input time series. If the output wanted to be forecast, matrix 'u' should
            contain future values for inputs.
        model:  The model to estimate. It is a single string indicating the type of model for each
                component with one or two letters:
                - Error: ? / N / A
                - Trend: ? / N / A / Ad / L
                - Seasonal: ? / N / A / D (trigonometric with different variances)
        h: Forecast horizon. If the model includes inputs, 'h' is not used; the length of 'u' is used instead.
        criterion: Information criterion for identification ("aic", "bic", or "aicc").
        lambdaBoxCox: Box-Cox lambda parameter (None: estimate)
        armaIdent: Check for ARMA models for the error component (True / False).
        verbose: Intermediate estimation output (True / False)

    Output:
        An object of class 'PTS'. It is a dictionary with fields including all the inputs and the fields
        listed below as outputs. All the functions in this package fill in part of the fields of any 'PTS'
        object as specified in what follows (function 'PTS' fills in all of them at once):

        After running 'PTSmodel':
        - p0: Initial values for parameter search
        - p: Estimated parameters
        - lambdaBoxCox: Estimated Box-Cox lambda parameter
        - v: Estimated innovations (white noise in correctly specified models)
        - yFor: Forecasted values of output
        - yForV: Variance of forecasted values of output

        After running 'object.validate':
        - table: Estimation and validation table

        After running 'object.components':
        - comp: Estimated components in matrix form

    See Also:
        PTS, UCmodel, UC, ETS, ETSmodel

    Author: Diego J. Pedregal
    """
    def __init__(self, y: pd.DataFrame, s: int = np.nan, u: np.array = np.array([]), model: str = "???",
                 h: int = 9999, criterion: str="aicc", lambdaBoxCox: np.array = np.array(1.0), armaIdent: bool=False,
                 verbose: bool = False):
        if isinstance(y, np.ndarray) and np.isnan(s):
            raise ValueError("Either 'y' should be a Panda time series or 's' should be supplied!!")
        if isinstance(y, pd.Series) or isinstance(y, pd.DataFrame):
            s = y.resample('Y').count()[1]
        if h == 9999:
            h = 2 * s
        self.y = y
        self.s = s
        self.u = u
        self.model = model
        self.h = h
        self.p0 = np.empty((0, 0))
        self.criterion = criterion
        self.lambdaBoxCox = lambdaBoxCox
        self.verbose = verbose
        self.armaIdent = armaIdent
        self.armaOrders = [0, 0]
        self.yFor = np.empty((0, 0))
        self.yForV = np.empty((0, 0))
        self.comp = np.empty((0, 0))
        self.table = ""
        self.p = np.empty((0, 0))
        self.v = np.empty((0, 0))
        self.modelUC = PTS2modelUC(model, self.armaOrders)
        self.modelUCmodel = None
        if s < 2:
            periods = np.array([1])
        else:
            periods = np.array(s) / range(1, int(s / 2) + 1)
        mUC = uc.UCmodel(y, s, u, self.modelUC, h, lambdaBoxCox=lambdaBoxCox,
                         criterion=criterion, periods=periods,
                         verbose=verbose, trendOptions="none/rw/llt/dt",
                         seasonalOptions="none/equal/different", irregularOptions="none/arma(0,0)",
                         MSOE=True, PTSnames=True)
        if mUC.model == "error":
            self.model = "error"
            return
        self.armaOrders = modelUC2arma(mUC.model)
        self.model = modelUC2PTS(mUC.model)
        self.p0 = mUC.p0
        self.lambdaBoxCox = mUC.lambdaBoxCox
        self.yFor = mUC.yFor
        self.yForV = mUC.yForV
        self.p = mUC.p
        self.modelUCmodel = mUC

    def validate(self, show=True):
        self.modelUCmodel = self.modelUCmodel.validate(False)
        self.table = self.modelUCmodel.table
        # Buscando test de heterocedasticidad con valor p NaN
        # ind = [i for i, line in enumerate(m['table']) if re.search(r"nan", line)]
        # if any(ind):
        #     for i in ind:
        #         line = m['table'][i]
        #         df = float(line[8:12])
        #         Fstat = float(line[14:30])
        #         pval = round(f.sf(Fstat, df, df), 4)
        #         line = line.replace("   nan", f"  {pval}")
        #         m['table'][i] = line
        if show:
            print(self.table)
        self.v = self.modelUCmodel.v

    def components(self):
        self.modelUCmodel = self.modelUCmodel.components()
        self.comp = self.modelUCmodel.comp
        # names = self.modelUCmodel.comp.columns
        # nComp = len(names)
        # ind = [0] + list(np.where(names == "Seasonal")) + list(np.where(names == "Slope"))
        # pos = np.where(names == "Irregular")
        # if len(pos) > 0 and pos < len(names) - 1:
        #     ind += list(range(pos[-1] + 1, len(names)))
        # if isinstance(self.y, np.ndarray):
        #     self.comp = np.hstack((self.modelUCmodel.v, self.modelUCmodel.comp[:, 0], self.modelUCmodel.comp[:, ind]))
        #     if self.modelUCmodel.comp.shape[1] == 3:
        #         self.modelUCmodel.comp[:, 1] = self.modelUCmodel.comp[:, 2]
        #     else:
        #         self.modelUCmodel.comp[:, 1] = np.sum(self.modelUCmodel.comp[:, 2 : ], axis=1)
        # else:
        #     self.comp = self.modelUCmodel.v.join(self.modelUCmodel.comp].iloc[:, [0] + ind])
        #     if m['comp'].shape[1] == 3:
        #         m['comp'].iloc[:, 1] = m['comp'].iloc[:, 2]
        #     else:
        #         m['comp'].iloc[:, 1] = m['comp'].iloc[:, 3:].sum(axis=1)
        #     self.comp.columns = ["Error", "Fit"] + list(names[ind])


def PTS(y: pd.DataFrame, s: int = np.nan, u: np.array = np.array([]), model: str = "???",
                 h: int = 9999, criterion: str="aicc", lambdaBoxCox: np.array = np.array(1.0), armaIdent: bool=False,
                 verbose: bool = False):
    """
    Run PTS general univariate MSOE models

    Inputs:
        y:  A time series to forecast (it may be either a numpy vector or a Panda time series object).
            This is the only input required. If a vector, the additional input 's' should be supplied
            compulsorily (see below).
        s: Seasonal period of time series (1 for annual, 4 for quarterly, ...)
        u:  A matrix of input time series. If the output wanted to be forecast, matrix 'u' should
            contain future values for inputs.
        model:  The model to estimate. It is a single string indicating the type of model for each
                component with one or two letters:
                - Error: ? / N / A
                - Trend: ? / N / A / Ad / L
                - Seasonal: ? / N / A / D (trigonometric with different variances)
        h: Forecast horizon. If the model includes inputs, 'h' is not used; the length of 'u' is used instead.
        criterion: Information criterion for identification ("aic", "bic", or "aicc").
        lambdaBoxCox: Box-Cox lambda parameter (None: estimate)
        armaIdent: Check for ARMA models for the error component (True / False).
        verbose: Intermediate estimation output (True / False)

    Output:
        An object of class 'PTS'. It is a dictionary with fields including all the inputs and the fields
        listed below as outputs. All the functions in this package fill in part of the fields of any 'PTS'
        object as specified in what follows (function 'PTS' fills in all of them at once):

        After running 'PTSmodel':
        - p0: Initial values for parameter search
        - p: Estimated parameters
        - lambdaBoxCox: Estimated Box-Cox lambda parameter
        - v: Estimated innovations (white noise in correctly specified models)
        - yFor: Forecasted values of output
        - yForV: Variance of forecasted values of output

        After running 'object.validate':
        - table: Estimation and validation table

        After running 'object.components':
        - comp: Estimated components in matrix form

    See Also:
        PTSmodel, UCmodel, UC, ETS, ETSmodel

    Author: Diego J. Pedregal

    """
    m = PTSmodel(y, s, u, model, h, criterion, lambdaBoxCox, armaIdent, verbose)
    m.validate(m.verbose)
    m.components()
    return m





