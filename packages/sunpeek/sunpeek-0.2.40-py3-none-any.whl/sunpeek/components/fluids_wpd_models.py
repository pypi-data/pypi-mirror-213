from typing import Union
import warnings
from pathlib import Path
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import numbers

from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV, ShuffleSplit
from sunpeek.definitions import FluidProps, fluid_data_dir


class ModelFactory:

    @classmethod
    def from_info_and_property(cls, fluid_info: 'sunpeek.definitions.fluid_definitions.WPDFluidInfo', prop: FluidProps):
        # fluid_names = [f.name for f in WPDFluids]
        # if fluid_info.name not in fluid_names:
        #     raise ValueError(f'Predefined fluid called "{fluid_info.name}" not found or not implemented.')

        # TODO change this. store fluid paths like Plant.raw_data_path -> env
        # raw_data_dir = Path(__file__).with_name('fluid_data')
        fn = fluid_data_dir / fluid_info.name / prop.value
        csv_file = fn.with_suffix('.csv')

        unit = fluid_info.unit_density if prop == FluidProps.density else fluid_info.unit_heat_capacity

        return ModelFactory(unit=unit,
                            is_pure=fluid_info.is_pure,
                            csv_file=csv_file)

    def __new__(cls, unit: dict = None,
                is_pure: bool = None,
                csv_file: Union[str, Path] = None,
                df: pd.DataFrame = None):
        """Returns an instance of a trained WPDModel.

        Returns a pure fluid model (WPDModelPure) if unit has only 2 entries (output, temperature),
        otherwise if unit has 3 entries (output, temperature, concentration) a mixed fluid model (WPDFluidMixed).
        This method also trains the model (= fits a sklearn model), based on the given df or csv_file.

        Parameters
        ----------
        unit : dict
            Units for inputs and outputs of the fluid model.
            Must have keys 'te' and 'out', optionally 'c' (then a WPDModelMixed is returned).
            Values must be valid pint unit strings.
        is_pure : bool
            True if unit
        csv_file : str, Path
            Data file used to train the model. Usually, this is a WebPlotDigitizer export csv file.
            Is expected to have multiple datasets, one for each concentration level.
        df: pd.DataFrame
            Is used to train the model.

        Raises
        ------
        TypeError
            If unit is not a dict.
        KeyError
            If required keys 'te' and 'out' are not found, or dictionary has extra keys not 'te', 'c' or 'out'.
        """

        model = WPDModelPure(unit) if is_pure else WPDModelMixed(unit)

        # Make sure either df or csv_file is given
        has_df = df is not None
        has_file = csv_file is not None
        if not (has_df ^ has_file):
            raise ValueError(
                'Model training accepts either a raw data file or a DataFrame. None or both of them were given.')

        # Train model
        model.df = df if has_df else model.csv2df(csv_file)
        model.sk_model = model.train()

        return model


class WPDModel(ABC):
    """
    Model for a particular property of a fluid, e.g. for density or for heat capacity.
    # Has an ONNX filename and the units for all inputs (temperature, optionally concentration) and the calculated output.
    Has the units for all inputs (temperature, optionally concentration) and the calculated output.
    Can read WebPlotDigitizer csv files, train sklearn fit, save trained model as ONNX file and make predictions.
    Attributes
    ----------
    unit : dict
        Units for temperature ['te'], optionally concentration ['c'] and (mandatory) output property ['out'].
        Must be valid pint unit strings. These units are sent to the trained model if a prediction is required,
        and the prediction output is interpreted in unit['out'].
    """

    n_inputs = None
    predictor_cols_in = []
    predictor_col_out = 'out'

    def __init__(self, unit):
        if len(unit) != 1 + self.n_inputs:
            raise ValueError(f'Unit dictionary of fluid definition must have length {self.n_inputs}, '
                             f'the units for output (e.g. density), temperature, and concentration (for mixed fluids).')

        expected_cols = set(['out'] + self.predictor_cols_in)
        if set(unit.keys()) != expected_cols:
            raise KeyError(f'Missing or mismatched keys in unit dictionary. Required keys: {", ".join(expected_cols)}.')

        self.unit = unit
        self.df = None
        self.sk_model = None

    def train(self, fit_type: str = 'polynomial'):
        """Fits polynomial interpolation model to fluid raw data in df.

        Parameters
        ----------
        fit_type : str
            Type of sklearn fit. Currently, only 'polynomial' implemented, works good enough.

        Returns
        -------
        Trained sklearn model.
        """
        if fit_type == 'polynomial':
            # Polynomial interpolation with grid-search cross-validation of interpolation coefficients.
            # Inspired by https://stackoverflow.com/questions/47442102/how-to-find-the-best-degree-of-polynomials
            degree_range = np.arange(2, 4)  # quadratic or cubic polynomials
            pipe = make_pipeline(StandardScaler(), PolynomialFeatures(), Ridge(alpha=1e-3))
            param_grid = {'polynomialfeatures__degree': degree_range}
            # grid = GridSearchCV(pipe, param_grid, cv=20)
            # grid = GridSearchCV(pipe, param_grid, cv=20, scoring='neg_mean_absolute_error')
            # grid = GridSearchCV(pipe, param_grid, cv=LeaveOneOut(), scoring='neg_mean_absolute_error')
            grid = GridSearchCV(pipe, param_grid, cv=ShuffleSplit(n_splits=10), scoring='neg_mean_absolute_error')

        # elif fit_type == 'spline':
        # # SplineTransformer not supported in ONNX conversion
        # Spline & ridge regression: Would be an interesting option, but currently not convertible to onnx.
        # https://scikit-learn.org/stable/auto_examples/linear_model/plot_polynomial_interpolation.html#sphx-glr-auto-examples-linear-model-plot-polynomial-interpolation-py
        # pipeline example: https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.SplineTransformer.html#sklearn.preprocessing.SplineTransformer
        # pipe = make_pipeline(SplineTransformer(degree=3), Ridge(alpha=1e-3))
        # param_grid = {'splinetransformer__n_knots': np.arange(4,10)}
        # # grid = GridSearchCV(pipe, param_grid, cv=20)
        # # grid = GridSearchCV(pipe, param_grid, cv=20, scoring='neg_mean_absolute_error')
        # # grid = GridSearchCV(pipe, param_grid, cv=LeaveOneOut(), scoring='neg_mean_absolute_error')
        # grid = GridSearchCV(pipe, param_grid, cv=ShuffleSplit(n_splits=10), scoring='neg_mean_absolute_error')

        else:
            raise ValueError(f'Unknown "fit_type": {fit_type}.')

        # X = self.df[['te', 'c']].to_numpy()
        # X = self.get_predictors_in().to_numpy()
        # y = self.df['out'].to_numpy()
        # grid.fit(X, y)
        # grid.fit(self.get_predictors_in, self.get_predictors_out)

        X = self.df[self.predictor_cols_in]
        y = self.df[self.predictor_col_out]
        grid.fit(X, y)
        model = grid.best_estimator_

        return model

        # reg = model.named_steps['linearregression']
        # reg.get_params()
        # coefs = reg.coef_
        # intercept = reg.intercept_

    @staticmethod
    def _preprocess_prediction_inputs(*args):
        """Args can be a) only temperature, or b) temperature and concentration.
        If concentration is given as a scalar -> gracefully expand to match temperature dimension.
        Returns temperature or tuple temperature, concentration.
        """

        if len(args) == 1:
            # only temperature given (pure fluid)
            return args,

        # Temperature and concentration given (mixed fluid)
        temperature = args[0]
        concentration_ = args[1]
        if concentration_ is None:
            return temperature

        scalar_concentration = isinstance(concentration_, numbers.Number)
        if scalar_concentration:
            concentration = np.full_like(temperature, concentration_)
        else:
            concentration = concentration_
            if len(temperature) != len(concentration):
                raise ValueError('Dimension mismatch among the given inputs "temperature" and "concentration".')

        return temperature, concentration

    def predict(self, *args):
        """Compute model prediction (fluid density, heat capacity) based on trained sklearn model, self.sk_model.

        Parameters
        ----------
        args : pint Quantity
            Inputs required for prediciton: temperature and (for mixed fluids) concentration.
            Fluid temperature in unit self.unit['te'], typically 'degC'
            Fluid concentration in unit self.unit['c'], typically 'percent'

        Returns
        -------
        pint Quantity : Calculated fluid property (density or heat capacity) in unit self.unit['out']
        """
        inputs = self._preprocess_prediction_inputs(*args)
        X = np.array(inputs).transpose().reshape(-1, self.n_inputs)
        nan_inputs = np.isnan(X).any(axis=1)

        out = np.full(nan_inputs.shape, np.nan)
        out[~nan_inputs] = self.sk_model.predict(X[~nan_inputs].reshape(-1, self.n_inputs))

        return out.flatten()

    @abstractmethod
    def csv2df(self, csv_file):
        raise NotImplementedError()


class WPDModelPure(WPDModel):
    n_inputs = 1
    predictor_cols_in = ['te']

    def csv2df(self, csv_file):
        """Read WebPlotDigitizer csv with single dataset into dataframe.
        """
        df = pd.read_csv(csv_file, header=0, sep=',')
        df = df.rename(columns={'X': 'te', 'Y': 'out'})

        return df

    def _plot_fit(self, plot_type: FluidProps = None):  # pragma: no cover
        """Check quality of model fit, after calling self.train().
        Plots model fit and original / ground truth data from WebPlotDigitizer csv dataset.
        """
        try:
            import plotly.graph_objects as go
        except ModuleNotFoundError:
            warnings.warn(
                'This function requires the plotly package, which is not installed. Install it with `pip install plotly`')
            return

        N_POINTS = 50
        fig = go.Figure()
        te = np.linspace(self.df['te'].min() - 20, self.df['te'].max() + 20, N_POINTS)
        out = self.predict(te)
        fig.add_trace(go.Scatter(x=te, y=out,
                                 mode='lines',
                                 name='Model prediction'))
        # Measured values as scatter
        fig.add_trace(go.Scatter(x=self.df['te'], y=self.df['out'],
                                 mode='markers',
                                 marker=dict(
                                     color='Black',
                                     size=10,
                                     opacity=0.4,
                                     line=dict(
                                         color='Black',
                                         width=1
                                     )),
                                 name='WPD measurements'))

        if plot_type == FluidProps.density:
            fig.update_layout(title='Density', width=1600, height=1200,
                              xaxis_title="Temperature [degC]", yaxis_title="Density [{self.unit['out']}]",
                              legend_traceorder="reversed")
        elif plot_type == FluidProps.heat_capacity:
            fig.update_layout(title='Heat capacity', width=1600, height=1200,
                              xaxis_title="Temperature [degC]", yaxis_title=f"Heat capacity [{self.unit['out']}]",
                              legend_traceorder="reversed")
        fig.show()


class WPDModelMixed(WPDModel):
    n_inputs = 2
    predictor_cols_in = ['te', 'c']

    def csv2df(self, csv_file):
        """
        Read WebPlotDigitizer csv with multiple datasets, combine into single dataframe with added dataset level column.
        """
        df_csv = pd.read_csv(csv_file, header=[0, 1], sep=',')
        dataset_names = [c for c in df_csv.columns.get_level_values(0) if not c.startswith('Unnamed')]
        df = pd.DataFrame()
        for n in dataset_names:
            i = df_csv.columns.get_loc((n, 'X'))
            x = df_csv.iloc[:, i].dropna()
            y = df_csv.iloc[:, i + 1].dropna()
            c = pd.Series(float(n), index=x.index)
            df2 = pd.concat([x.rename('te'), y.rename('out'), c.rename('c')], axis=1)
            df = pd.concat([df, df2], ignore_index=True)

        return df

    def _plot_fit(self, plot_type: FluidProps = None):  # pragma: no cover
        """Check quality of model fit, after calling self.train().
        Plots model fit and original / ground truth data from WebPlotDigitizer csv dataset.
        """
        try:
            import plotly.graph_objects as go
        except ModuleNotFoundError:
            warnings.warn(
                'This function requires the plotly package, which is not installed. Install it with `pip install plotly`')
            return

        N_POINTS = 50
        # For all concentration levels, create output curves within measured temperature limits
        df = self.df.groupby('c').te.agg(['min', 'max'])
        fig = go.Figure()
        for i in np.arange(df.shape[0]):
            te = np.linspace(df.iloc[i, 0], df.iloc[i, 1], N_POINTS)
            c = df.index[i]
            out = self.predict(te, c)
            fig.add_trace(go.Scatter(x=te, y=out,
                                     mode='lines',
                                     name=f"Model prediction, c={df.index[i]}%"))
        # Measured values as scatter
        fig.add_trace(go.Scatter(x=self.df['te'], y=self.df['out'],
                                 mode='markers',
                                 marker=dict(
                                     color='Black',
                                     size=10,
                                     opacity=0.4,
                                     line=dict(
                                         color='Black',
                                         width=1
                                     )),
                                 name='WPD measurements'))

        if plot_type == FluidProps.density:
            fig.update_layout(title='Density', width=1600, height=1200,
                              xaxis_title="Temperature [degC]", yaxis_title="Density [{self.unit['out']}]",
                              legend_traceorder="reversed")
        elif plot_type == FluidProps.heat_capacity:
            fig.update_layout(title='Heat capacity', width=1600, height=1200,
                              xaxis_title="Temperature [degC]", yaxis_title=f"Heat capacity [{self.unit['out']}]",
                              legend_traceorder="reversed")

        fig.show()
