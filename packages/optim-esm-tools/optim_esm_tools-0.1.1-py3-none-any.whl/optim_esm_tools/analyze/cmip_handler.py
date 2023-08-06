# -*- coding: utf-8 -*-
import optim_esm_tools as oet

import os
import xarray as xr
import numpy as np

import typing as ty
import collections
from warnings import warn
from functools import wraps
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

import datetime
from immutabledict import immutabledict
import xrft


_seconds_to_year = 365.25 * 24 * 3600
folder_fmt = 'model_group model scenario run domain variable grid version'.split()
__OPTIM_VERSION__ = '0.1.10'


def _native_date_fmt(time_array: np.array, date: ty.Tuple[int, int, int]):
    """Create date object using the date formatting from the time-array"""
    if isinstance(time_array, xr.DataArray):
        return _native_date_fmt(time_array=time_array.values, date=date)

    if not len(time_array):
        raise ValueError(f'No values in dataset?')

    # Support cftime.DatetimeJulian, cftime.DatetimeGregorian, cftime.DatetimeNoLeap and similar
    _time_class = time_array[0].__class__
    return _time_class(*date)


def read_ds(
    base: str,
    variable_of_interest: ty.Tuple[str] = ('tas',),
    max_time: ty.Optional[ty.Tuple[int, int, int]] = (2100, 1, 1),
    min_time: ty.Optional[ty.Tuple[int, int, int]] = None,
    _time_var='time',
    _detrend_type='linear',
    _ma_window: int = 10,
    _cache: bool = True,
) -> xr.Dataset:
    """Read a dataset from a folder called "base".

    Args:
        base (str): Folder to load the data from
        variable_of_interest (ty.Tuple[str], optional): _description_. Defaults to ('tas',).
        _time_var (str, optional): Name of the time dimention. Defaults to 'time'.
        _detrend_type (str, optional): Type of detrending applied. Defaults to 'linear'.
        _ma_window (int, optional): Moving average window (assumed to be years). Defaults to 10.
        _cache (bool, optional): cache the dataset with it's extra fields to alow faster (re)loading. Defaults to True.

    Returns:
        xr.Dataset: An xarray dataset with the appropriate variables
    """
    post_processed_file = (
        os.path.join(
            base,
            f'{variable_of_interest}'
            f'_{min_time if min_time else ""}'
            f'_{max_time if max_time else ""}'
            f'_ma{_ma_window}'
            f'_optimesm_v{__OPTIM_VERSION__}.nc',
        )
        .replace('(', '')
        .replace(')', '')
        .replace(' ', '_')
        .replace(',', '')
        .replace('\'', '')
    )

    if os.path.exists(post_processed_file) and _cache:
        return oet.synda_files.format_synda.load_glob(post_processed_file)

    data_path = os.path.join(base, 'merged.nc')
    if not os.path.exists(data_path):
        warn(f'No dataset at {data_path}')
        return None

    data_set = oet.synda_files.format_synda.load_glob(data_path)
    data_set = oet.synda_files.format_synda.recast(data_set)

    if min_time or max_time:
        time_slice = [
            _native_date_fmt(data_set[_time_var], d) if d is not None else None
            for d in [min_time, max_time]
        ]
        data_set = data_set.sel(**{_time_var: slice(*time_slice)})

    # Detrend and run_mean on the fly
    for variable in variable_of_interest:
        # NB these are DataArrays not Datasets!
        run_mean = data_set[variable].rolling(time=_ma_window, center=True).mean()
        detrended = xrft.detrend(
            data_set[variable], _time_var, detrend_type=_detrend_type
        )
        detrended_run_mean = xrft.detrend(
            run_mean.dropna(_time_var), _time_var, detrend_type=_detrend_type
        )
        detrended_run_mean.attrs['units'] = data_set[variable].attrs.get(
            'units', '{units}'
        )
        data_set[f'{variable}_run_mean_{_ma_window}'] = run_mean
        data_set[f'{variable}_detrend'] = detrended
        data_set[f'{variable}_detrend_run_mean_{_ma_window}'] = detrended_run_mean

    folders = base.split(os.sep)

    # start with -1 (for i==0)
    metadata = {k: folders[-i - 1] for i, k in enumerate(folder_fmt[::-1])}
    metadata.update(
        dict(path=base, file=post_processed_file, running_mean_period=_ma_window)
    )

    data_set.attrs.update(metadata)

    if _cache:
        print(f'Write {post_processed_file}' + ' ' * 100, flush=True, end='\r')
        data_set.to_netcdf(post_processed_file)
    return data_set


def example_time_series(ds_combined: xr.Dataset, variable='tas', _ma_window=10) -> None:
    """Make an example of time series based on datset

    Args:
        ds_combined (xr.Dataset): dataset
    """
    sel = dict(x=20, y=20)
    detrend_variable = f'{variable}_detrend'
    detrend_variable_running_mean = f'{variable}_detrend_run_mean_{_ma_window}'
    time = 'time'

    _, axes = plt.subplots(3, 1, figsize=(12, 10))
    plt.sca(axes[0])

    ds_combined.isel(**sel)[detrend_variable].plot(label='detrended')
    ds_combined.isel(**sel)[detrend_variable_running_mean].plot(
        label='detrended, runmean'
    )
    plt.legend()

    plt.sca(axes[1])
    # ds_combined.differentiate("time").isel(**sel)[variable].plot(label='detrended')
    ds_combined[detrend_variable_running_mean].dropna(time).differentiate(time).isel(
        **sel
    ).plot(label='detrended, runmean')
    plt.legend()

    plt.sca(axes[2])
    # ds_combined.differentiate("time").differentiate("time").isel(**sel)[variable].plot(label='detrended')
    ds_combined[detrend_variable_running_mean].dropna(time).differentiate(
        time
    ).differentiate(time).isel(**sel).plot(label='detrended, runmean')
    plt.legend()


def check_accepts(
    accepts: ty.Mapping[str, ty.Iterable] = immutabledict(unit=('absolute', 'std')),
    do_raise: bool = True,
):
    """Wrapper for function if certain kwargs are from a defined list of variables.

    Example:
        ```
            @check_accepts(accepts=dict(far=('boo', 'booboo')))
            def bla(far):
                print(far)

            bla(far='boo')  # prints boo
            bla(far='booboo')  # prints booboo
            bla(far=1)  # raises ValueError
        ```


    Args:
        accepts (ty.Mapping[str, ty.Iterable], optional): which kwarg to accept a limited set of options.
            Defaults to immutabledict(unit=('absolute', 'std')).
        do_raise (bool, optional): if False, don't raise an error but just warn. Defaults to True.

    Returns:
        wrapped function
    """

    def somedec_outer(fn):
        @wraps(fn)
        def somedec_inner(*args, **kwargs):
            message = ''
            for k, v in kwargs.items():
                if k in accepts and v not in accepts[k]:
                    message += f'{k} for {v} but only accepts {accepts[k]}'
            if do_raise and message:
                raise ValueError(message)
            elif message:
                warn(message)
            response = fn(*args, **kwargs)
            return response

        return somedec_inner

    return somedec_outer


def apply_abs(apply=True, add_abs_to_name=True, _disable_kw='apply_abs'):
    """Apply np.max() to output of function (if apply=True)
    Disable in the function kwargs by using the _disable_kw argument

    Example:
        ```
        @apply_abs(apply=True, add_abs_to_name=False)
        def bla(a=1, **kw):
            print(a, kw)
            return a
        assert bla(-1, apply_abs=True) == 1
        assert bla(-1, apply_abs=False) == -1
        assert bla(1) == 1
        assert bla(1, apply_abs=False) == 1
        ```
    Args:
        apply (bool, optional): apply np.abs. Defaults to True.
        _disable_kw (str, optional): disable with this kw in the function. Defaults to 'apply_abs'.
    """

    def somedec_outer(fn):
        @wraps(fn)
        def somedec_inner(*args, **kwargs):
            response = fn(*args, **kwargs)
            do_abs = kwargs.get(_disable_kw)
            if do_abs or (do_abs is None and apply):
                if add_abs_to_name and isinstance(getattr(response, 'name'), str):
                    response.name = f'Abs. {response.name}'
                return np.abs(response)
            return response

        return somedec_inner

    return somedec_outer


def _remove_any_none_times(da, time_dim):
    data_var = da.copy()
    time_null = da.isnull().all(dim=set(da.dims) - {time_dim})
    if np.any(time_null):
        data_var = data_var.load().where(~time_null, drop=True)
    return data_var


@apply_abs()
@check_accepts(accepts=dict(unit=('absolute', 'relative', 'std')))
def running_mean_diff(
    data_set: xr.Dataset,
    variable: str = 'tas',
    time_var: str = 'time',
    naming: str = '{variable}_run_mean_{running_mean}',
    running_mean: int = 10,
    rename_to: str = 'long_name',
    unit: str = 'absolute',
    apply_abs: bool = True,
    _t_0_date: ty.Optional[tuple] = None,
    _t_1_date: ty.Optional[tuple] = None,
) -> xr.Dataset:
    """Return difference in running mean of data set

    Args:
        data_set (xr.Dataset):
        variable (str, optional): . Defaults to 'tas'.
        time_var (str, optional): . Defaults to 'time'.
        naming (str, optional): . Defaults to '{variable}_run_mean_{running_mean}'.
        running_mean (int, optional): . Defaults to 10.
        rename_to (str, optional): . Defaults to 'long_name'.
        unit (str, optional): . Defaults to 'absolute'.
        apply_abs (bool, optional): . Defaults to True.
        _t_0_date (ty.Optional[tuple], optional): . Defaults to (2015, 1, 1).
        _t_1_date (ty.Optional[tuple], optional): . Defaults to (2100, 1, 1).

    Raises:
        ValueError: when no timestamps are not none?

    Returns:
        xr.Dataset:
    """
    var_name = naming.format(variable=variable, running_mean=running_mean)
    _time_values = data_set[time_var].dropna(time_var)

    if not len(_time_values):
        raise ValueError(f'No values for {time_var} in dataset?')

    data_var = _remove_any_none_times(data_set[var_name], time_var)

    if _t_0_date is not None:
        t_0 = _native_date_fmt(_time_values, _t_0_date)
        data_t_0 = data_var.sel(time=t_0, method='nearest')
    else:
        data_t_0 = data_var.isel(time=0)

    if _t_0_date is not None:
        t_1 = _native_date_fmt(_time_values, _t_1_date)
        data_t_1 = data_var.sel(time=t_1, method='nearest')
    else:
        data_t_1 = data_var.isel(time=-1)

    result = data_t_1 - data_t_0
    result = result.copy()
    var_unit = data_var.attrs.get('units', '{units}')
    name = data_var.attrs.get(rename_to, variable)

    if unit == 'absolute':
        result.name = f't[-1] - t[0] for {name} [{var_unit}]'
        return result

    if unit == 'relative':
        result = 100 * result / data_t_0
        result.name = f't[-1] - t[0] / t[0] for {name} $\%$'
        return result

    # Redundant if just for clarity
    if unit == 'std':
        result = result / result.std()
        result.name = f't[-1] - t[0] for {name} [$\sigma$]'
        return result


@apply_abs()
@check_accepts(accepts=dict(unit=('absolute', 'relative', 'std')))
def running_mean_std(
    data_set: xr.Dataset,
    variable: str = 'tas',
    time_var: str = 'time',
    naming: str = '{variable}_detrend_run_mean_{running_mean}',
    running_mean: int = 10,
    rename_to: str = 'long_name',
    apply_abs: bool = True,
    unit: str = 'absolute',
) -> xr.Dataset:
    data_var = naming.format(variable=variable, running_mean=running_mean)
    result = data_set[data_var].std(dim=time_var)
    result = result.copy()
    var_unit = data_set[data_var].attrs.get('units', '{units}')
    name = data_set[data_var].attrs.get(rename_to, variable)

    if unit == 'absolute':
        result.name = f'Std. {name} [{var_unit}]'
        return result

    if unit == 'relative':
        result = 100 * result / data_set[data_var].mean(dim=time_var)
        result.name = f'Relative Std. {name} [$\%$]'
        return result

    if unit == 'std':
        result = result / data_set[data_var].std()
        result.name = f'Std. {name} [$\sigma$]'
        return result


@apply_abs()
@check_accepts(accepts=dict(unit=('absolute', 'relative', 'std')))
def max_change_xyr(
    data_set: xr.Dataset,
    variable: str = 'tas',
    time_var: str = 'time',
    naming: str = '{variable}_run_mean_{running_mean}',
    x_yr: ty.Union[int, float] = 10,
    running_mean: int = 10,
    rename_to: str = 'long_name',
    apply_abs: bool = True,
    unit: str = 'absolute',
) -> xr.Dataset:
    data_var = naming.format(variable=variable, running_mean=running_mean)
    plus_x_yr = data_set.isel({time_var: slice(x_yr, None)})[data_var]
    to_min_x_yr = data_set.isel({time_var: slice(None, -x_yr)})[data_var]

    # Keep the metadata (and time stamps of the to_min_x_yr)
    result = to_min_x_yr.copy(data=plus_x_yr.values - to_min_x_yr.values)

    result = result.max(dim=time_var).copy()
    var_unit = data_set[data_var].attrs.get('units', '{units}')
    name = data_set[data_var].attrs.get(rename_to, variable)

    if unit == 'absolute':
        result.name = f'{x_yr} yr diff. {name} [{var_unit}]'
        return result

    if unit == 'relative':
        result = 100 * result / to_min_x_yr.mean(dim=time_var)
        result.name = f'{x_yr} yr diff. {name} [$\%$]'
        return result

    if unit == 'std':
        result = result / result.std()
        result.name = f'{x_yr} yr diff. {name} [$\sigma$]'
        return result


@apply_abs()
@check_accepts(accepts=dict(unit=('absolute', 'relative', 'std')))
def max_derivative(
    data_set: xr.Dataset,
    variable: str = 'tas',
    time_var: str = 'time',
    naming: str = '{variable}_run_mean_{running_mean}',
    running_mean: int = 10,
    rename_to: str = 'long_name',
    apply_abs: bool = True,
    unit: str = 'absolute',
) -> xr.Dataset:
    var_name = naming.format(variable=variable, running_mean=running_mean)

    data_array = _remove_any_none_times(data_set[var_name], time_var)
    result = data_array.differentiate(time_var).max(dim=time_var) * _seconds_to_year

    var_unit = data_array.attrs.get('units', '{units}')
    name = data_array.attrs.get(rename_to, variable)

    if unit == 'absolute':
        result.name = f'Max $\partial/\partial t$ {name} [{var_unit}/yr]'
        return result

    if unit == 'relative':
        result = 100 * result / data_array.mean(dim=time_var)
        result.name = f'Max $\partial/\partial t$ {name} [$\%$/yr]'
        return result

    if unit == 'std':
        # A local unit of sigma might be better X.std(dim=time_var)
        result = result / data_array.std()
        result.name = f'Max $\partial/\partial t$ {name} [$\sigma$/yr]'
        return result


class MapMaker(object):
    data_set: xr.Dataset

    # This is a bit rough, conditions is a mapping of keys to decsriptions and functions
    conditions: ty.Mapping[str, ty.Tuple] = immutabledict(
        {
            'i ii iii iv v vi vii viii ix x'.split()[i]: props
            for i, props in enumerate(
                zip(
                    [
                        'Difference of running mean (10 yr) between start and end of time series. Not detrended',
                        'Standard deviation of running mean (10 yr). Detrended',
                        'Max change in 10 yr in the running mean (10 yr). Not detrended',
                        'Max value of the first order derivative of the running mean. Not deterended',
                    ],
                    [
                        running_mean_diff,
                        running_mean_std,
                        max_change_xyr,
                        max_derivative,
                    ],
                )
            )
        }
    )

    kw: ty.Mapping = immutabledict(
        fig=dict(dpi=200, figsize=(12, 8)),
        title=dict(fontsize=8),
        gridspec=dict(hspace=0.3),
        cbar=dict(orientation='horizontal', extend='both'),
        plot=dict(transform=ccrs.PlateCarree()),
    )
    normalizations: ty.Optional[ty.Mapping] = None

    _cache: bool = False

    def __init__(
        self,
        data_set: xr.Dataset,
        normalizations: ty.Union[None, ty.Mapping, ty.Iterable] = None,
        cache: bool = False,
    ):
        self.data_set = data_set
        if normalizations is None:
            self.normalizations = {i: [None, None] for i in self.conditions.keys()}
        elif isinstance(normalizations, collections.abc.Mapping):
            self.normalizations = normalizations
        elif isinstance(normalizations, collections.abc.Iterable):
            self.normalizations = {
                i: normalizations[j] for j, i in enumerate(self.conditions.keys())
            }

        def _incorrect_format():
            return (
                any(
                    not isinstance(v, collections.abc.Iterable)
                    for v in self.normalizations.values()
                )
                or any(len(v) != 2 for v in self.normalizations.values())
                or any(k not in self.normalizations for k in self.conditions)
            )

        if self.normalizations is None or _incorrect_format():
            raise TypeError(
                f'Normalizations should be mapping from'
                f'{self.conditions.keys()} to vmin, vmax, '
                f'got {self.normalizations} (from {normalizations})'
            )
        self._cache = cache

    def plot(self, *a, **kw):
        print('Depricated use plot_all')
        return self.plot_all(*a, **kw)

    def plot_all(
        self,
        nx=2,
        fig=None,
        **kw,
    ):
        ny = np.ceil(len(self.conditions) / nx).astype(int)
        if fig is None:
            fig = plt.figure(**self.kw['fig'])

        from matplotlib.gridspec import GridSpec

        gs = GridSpec(nx, ny, **self.kw['gridspec'])
        plt_axes = []

        for i, label in enumerate(self.conditions.keys()):
            ax = fig.add_subplot(
                gs[i],
                projection=ccrs.PlateCarree(
                    central_longitude=0.0,
                ),
            )
            self.plot_i(label, ax=ax, **kw)
            plt_axes.append(ax)
        return plt_axes

    def plot_i(self, label, ax=None, coastlines=True, **kw):
        if ax is None:
            ax = plt.gca()
        if coastlines:
            ax.coastlines()

        prop = getattr(self, label)

        cmap = plt.get_cmap('viridis').copy()
        cmap.set_extremes(under='cyan', over='orange')

        c_kw = self.kw['cbar'].copy()
        c_range_kw = {
            vm: self.normalizations[label][j]
            for j, vm in enumerate('vmin vmax'.split())
        }

        for k, v in {
            **self.kw['plot'],
            **c_range_kw,
            **dict(
                cbar_kwargs=c_kw,
                cmap=cmap,
            ),
        }.items():
            kw.setdefault(k, v)

        plt_ax = prop.plot(**kw)

        plt.xlim(-180, 180)
        plt.ylim(-90, 90)
        description = self.conditions[label][0]
        ax.set_title(label.upper() + '\n' + description, **self.kw['title'])
        gl = ax.gridlines(draw_labels=True)
        gl.top_labels = False
        gl.right_labels = False
        return plt_ax

    def __getattr__(self, item):
        if item in self.conditions:
            _, function = self.conditions[item]
            key = f'_{item}'
            if self._cache:
                if not isinstance(self._cache, dict):
                    self._cache = dict()
                if key in self._cache:
                    data = self._cache.get(key)
                    return data

            data = function(self.data_set)
            if self._cache or isinstance(self._cache, dict):
                self._cache[key] = data.load()
            return data

        return self.__getattribute__(item)

    @staticmethod
    def _ts_single(time_val, mean, std, plot_kw, fill_kw):
        if fill_kw is None:
            fill_kw = dict(alpha=0.4, step='mid')

        l = mean.plot(**plot_kw)

        if std is not None:
            # TODO, make this more elegant!
            # import cftime
            # plt.fill_between(   [cftime.real_datetime(dd.year, dd.month, dd.day) for dd in time_val], mean - std, mean+std, **fill_kw)
            (mean - std).plot(color=l[0]._color, alpha=0.4, drawstyle='steps-mid')
            (mean + std).plot(color=l[0]._color, alpha=0.4, drawstyle='steps-mid')

    def _ts(
        self,
        variable,
        ds=None,
        time='time',
        other_dim=(),
        running_mean=10,
        fill_kw=None,
        labels=dict(),
        only_rm=False,
        **plot_kw,
    ):
        if ds is None:
            ds = self.data_set
        if not only_rm:
            mean, std = self._mean_and_std(ds, variable, other_dim)
            # return mean, std
            plot_kw['label'] = labels.get(variable, variable)
            self._ts_single(ds[time].values, mean, std, plot_kw, fill_kw)

        mean, std = self._mean_and_std(
            ds, f'{variable}_run_mean_{running_mean}', other_dim
        )
        plot_kw['label'] = labels.get(
            f'{variable}_run_mean_{running_mean}',
            f'{variable} running mean {running_mean}',
        )
        self._ts_single(ds[time].values, mean, std, plot_kw, fill_kw)

        plt.ylabel('T [K]')
        plt.legend()
        plt.title('')

    def _det_ts(
        self,
        variable,
        ds=None,
        time='time',
        other_dim=(),
        running_mean=10,
        fill_kw=None,
        labels=dict(),
        only_rm=False,
        **plot_kw,
    ):
        if ds is None:
            ds = self.data_set
        if not only_rm:
            mean, std = self._mean_and_std(ds, f'{variable}_detrend', other_dim)
            plot_kw['label'] = labels.get(
                f'{variable}_detrend', f'detrended {variable}'
            )
            self._ts_single(ds[time].values, mean, std, plot_kw, fill_kw)

        mean, std = self._mean_and_std(
            ds, f'{variable}_detrend_run_mean_{running_mean}', other_dim
        )
        plot_kw['label'] = labels.get(
            f'{variable}_detrend_run_mean_{running_mean}',
            f'detrended {variable} running mean {running_mean}',
        )
        self._ts_single(ds[time].values, mean, std, plot_kw, fill_kw)
        plt.ylabel('detrend(T) [K]')
        plt.legend()
        plt.title('')

    def _ddt_ts(
        self,
        variable,
        ds=None,
        time='time',
        other_dim=(),
        running_mean=10,
        fill_kw=None,
        labels=dict(),
        only_rm=False,
        **plot_kw,
    ):
        if ds is None:
            ds = self.data_set
        variable_rm = f'{variable}_run_mean_{running_mean}'

        if not only_rm:
            # Dropna should take care of any nones in the data-array
            dy_dt = ds[variable].mean(other_dim).dropna(time).differentiate(time)
            dy_dt *= _seconds_to_year
            # mean, std = self._mean_and_std(dy_dt, variable=None, other_dim=other_dim)
            # plot_kw['label'] = variable
            # self._ts_single(ds[time].values, mean, std, plot_kw, fill_kw)
            label = f'd/dt {labels.get(variable, variable)}'
            dy_dt.plot(label=label, **plot_kw)

        dy_dt_rm = ds[variable_rm].mean(other_dim).dropna(time).differentiate(time)
        dy_dt_rm *= _seconds_to_year
        label = (
            f"d/dt {labels.get(variable_rm, f'{variable} running mean {running_mean}')}"
        )
        dy_dt_rm.plot(label=label, **plot_kw)
        # mean, std = self._mean_and_std(dy_dt_rm, variable=None, other_dim=other_dim)
        # plot_kw['label'] = variable
        # self._ts_single(ds[time].values, mean, std, plot_kw, fill_kw)

        plt.ylim(dy_dt_rm.min() / 1.05, dy_dt_rm.max() * 1.05)
        plt.ylabel('$\partial T/\partial t$ [K/yr]')
        plt.legend()
        plt.title('')

    @staticmethod
    def _mean_and_std(ds, variable, other_dim):
        if variable is None:
            da = ds
        else:
            da = ds[variable]
        if other_dim is None:
            return da.mean(other_dim), None
        return da.mean(other_dim), da.std(other_dim)

    def time_series(
        self,
        variable='tas',
        time='time',
        other_dim=('x', 'y'),
        running_mean=10,
        interval=True,
        axes=None,
        **kw,
    ):
        if variable != 'tas':
            raise NotImplementedError('Currently only works for tas')

        ds = self.data_set
        if interval is False:
            ds = ds.copy().mean(other_dim)
            other_dim = None

        plot_kw = dict(drawstyle='steps-mid', **kw)

        if axes is None:
            _, axes = plt.subplots(3, 1, figsize=(12, 10), gridspec_kw=dict(hspace=0.3))

        plt.sca(axes[0])
        self._ts(
            variable, ds=ds, running_mean=running_mean, other_dim=other_dim, **plot_kw
        )

        plt.sca(axes[1])
        self._det_ts(
            variable, ds=ds, running_mean=running_mean, other_dim=other_dim, **plot_kw
        )

        plt.sca(axes[2])
        self._ddt_ts(
            variable,
            ds=ds,
            time=time,
            running_mean=running_mean,
            other_dim=other_dim,
            **plot_kw,
        )

        return axes

    @property
    def ds(self):
        warn('MapMaker.ds is depricated, use MapMaker.data_set')
        return self.data_set


def make_title(ds):
    return '{model_group} {model} {scenario} {run} {variable}'.format(**ds.attrs)
