"""Plotting module. Development plots only.
"""

import warnings
from pathlib import Path
import numpy as np
import pandas as pd
import datetime as dt
import pint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.transforms as transforms

from sunpeek.common.utils import ROOT_DIR

PLOTS_AVAILABLE_MSG = 'Modules "plotly" or "pendulum" not found. Install them to use development plots.'

try:
    from plotly import graph_objects as go
    from plotly.subplots import make_subplots
    import pendulum

    PLOTS_AVAILABLE = True
except ModuleNotFoundError:
    warnings.warn(PLOTS_AVAILABLE_MSG)
    PLOTS_AVAILABLE = False


def assert_modules():
    if not PLOTS_AVAILABLE:
        raise ModuleNotFoundError(PLOTS_AVAILABLE_MSG)


# Color: matplotlib style 'tableau-colorblind10'
# Style: https://viscid-hub.github.io/Viscid-docs/docs/dev/styles/tableau-colorblind10.html
# Color names https://stackoverflow.com/questions/74830439/list-of-color-names-for-matplotlib-style-tableau-colorblind10
COLORS = {
    'blue': '#5F9ED1',
    'sky_blue': '#006BA4',
    'sail_blue': '#A2C8EC',
    'pumpkin': '#FF800E',
    'orange': '#C85200',
    'cheese': '#FFBC79',
    'gray': '#595959',
    'warm_gray': '#898989',
    'light_gray': '#CFCFCF',
    'dark_gray': '#ABABAB',
    'almost_black': '#373737',
}

FULL_WIDTH = 16.59 / 2.54  # full page width, cm to inches
FONT_SIZE = 6
plt.rcParams.update({
    'figure.dpi': 600,
    # 'font.family': 'Times New Roman',
    'font.family': 'Open Sans',
    'font.size': FONT_SIZE,
    'text.usetex': False,
    'axes.labelsize': FONT_SIZE,
    'axes.titlesize': FONT_SIZE,
    'axes.labelpad': 2,
    'axes.titlepad': 4,
    'axes.linewidth': 0.5,
    'xaxis.labellocation': 'left',
    'grid.alpha': 0.5,
    'grid.linewidth': 0.5,
    'lines.linewidth': 0.75,
    'patch.linewidth': 0.25,
    'legend.fontsize': FONT_SIZE - 1,
    'legend.title_fontsize': FONT_SIZE - 1,
    'legend.framealpha': 0.8,
    'legend.borderpad': 0.2,
    'legend.columnspacing': 1.5,
    'legend.labelspacing': 0.25,
    'xtick.labelsize': FONT_SIZE - 1,
    'ytick.labelsize': FONT_SIZE,
    'xtick.major.size': 2,
    'xtick.major.pad': 1,
    'xtick.major.width': 0.5,
    'ytick.major.size': 2,
    'ytick.major.pad': 1,
    'ytick.major.width': 0.5,
    'xtick.minor.size': 2,
    'xtick.minor.pad': 1,
    'xtick.minor.width': 0.5,
    'ytick.minor.size': 2,
    'ytick.minor.pad': 1,
    'ytick.minor.width': 0.5,
})
# Avoid black unless necessary
# Taken from https://atchen.me/research/code/data-viz/2022/01/04/plotting-matplotlib-reference.html
plt.rcParams.update({
    'text.color': COLORS['almost_black'],
    'patch.edgecolor': COLORS['gray'],
    'patch.force_edgecolor': True,
    'hatch.color': COLORS['almost_black'],
    'axes.edgecolor': COLORS['almost_black'],
    'axes.labelcolor': COLORS['almost_black'],
    'xtick.color': COLORS['almost_black'],
    'ytick.color': COLORS['almost_black']
})


def plot_all(pc_output, mode='screen', use_safety=True, write_image=False, anonymize=False):
    """Create all defined plots.
    """
    assert_modules()
    assert mode in ['screen', 'presentation']
    if pc_output.n_intervals == 0:
        print('Nothing to plot, no PC intervals found.')
        return

    figures = dict(
        square=plot_square(pc_output, mode=mode, use_safety=use_safety, write_image=write_image, anonymize=anonymize),
        time=plot_time(pc_output, mode=mode, use_safety=use_safety, write_image=write_image, anonymize=anonymize),
        sums=plot_sums(pc_output, mode=mode, write_image=write_image, anonymize=anonymize),
    )

    return figures


def plot_square(pc_output, mode,
                use_safety=True,
                write_image=False,
                anonymize=False,
                axis_range=None,
                tick0=None):
    """Plot measured vs. estimated power in intervals + trend line.
    """

    assert_modules()
    if pc_output.n_intervals == 0:
        print('Nothing to plot, no PC intervals found.')
        return

    if axis_range is None:
        axis_range = [250, 650]
    if tick0 is None:
        tick0 = 300

    measured = pc_output.tp_sp_measured.magnitude
    estimated = pc_output.tp_sp_estimated_safety.magnitude if use_safety else pc_output.tp_sp_estimated.magnitude
    slope = pc_output.target_actual_slope_safety.magnitude if use_safety else pc_output.target_actual_slope.magnitude
    font_size = 24 if mode == 'presentation' else 14

    fig = go.Figure()
    fig.add_scatter(x=estimated, y=measured,
                    name=f"Interval averages ("
                         f"{pendulum.duration(seconds=pc_output.interval_length.total_seconds()).in_words(locale='en')}"
                         f")",
                    mode='markers', marker_size=10, marker_opacity=0.8)

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.01,
        xanchor="right",
        x=1
    ))

    # Linear trendline with 0 intercept
    # rng = [estimated.min(), estimated.max()]
    # fig.add_scatter(x=rng, y=slope * np.array(rng),
    #                 name=f'y = {slope:.3f} x',
    #                 mode='lines', line_color='grey', line_width=3)

    # Bisection line
    fig.add_scatter(x=axis_range, y=axis_range, name='', showlegend=False,
                    mode='lines',
                    # line_dash='dash',
                    line_color='grey', line_width=0.5)
    fig.update_layout(
        width=1000,
        height=1000,
        autosize=False,
        xaxis=dict(
            type='linear',
            constrain="domain",
            title="<b>Estimated</b> power [W/m²]",
            linecolor="#BCCCDC",
            range=axis_range,
            title_font_size=font_size,
            tickfont_size=font_size,
            tick0=tick0,
            dtick=100,
        ),
        yaxis=dict(
            type='linear',
            constrain="domain",
            title="<b>Measured</b> power [W/m²]",
            title_font_size=font_size,
            title_standoff=30,
            linecolor="#BCCCDC",
            range=axis_range,
            scaleanchor="x",
            scaleratio=1,
            autorange=False,
            tickfont_size=font_size,
            tick0=tick0,
            dtick=100,
        ),
        legend_font_size=font_size,
    )

    # fig.update_xaxes(
    #     showspikes=True,
    #     spikecolor="grey",
    #     spikesnap="cursor",
    #     spikemode="across",
    #     spikedash="solid",
    # )
    # fig.update_yaxes(
    #     showspikes=True,
    #     spikecolor="grey",
    #     spikesnap="cursor",
    #     spikemode="across",
    #     spikedash="solid",
    # )

    _show(fig)
    if write_image:
        fig.write_image(_get_filename('square', pc_output))

    return fig


def plot_time(pc_output, mode,
              use_safety=True,
              write_image=False,
              anonymize=False,
              plot_trend=True,
              yrange=None,
              ):
    """Plots ratio of measured vs. estimated power over time.
    """
    assert_modules()
    if pc_output.n_intervals == 0:
        print('Nothing to plot, no PC intervals found.')
        return

    if yrange is None:
        yrange = [0.8, 1.2]

    estimated = pc_output.tp_sp_estimated_safety.magnitude if use_safety else pc_output.tp_sp_estimated.magnitude
    measured = pc_output.tp_sp_measured.magnitude
    ratio = measured / estimated
    # Plotting ratio against midpoint of intervals
    time_display = pc_output.datetime_intervals_start + 0.5 * pc_output.interval_length
    font_size = 24 if mode == 'presentation' else 14

    fig = go.Figure()
    fig.add_scatter(x=time_display, y=ratio,
                    mode='markers', marker_size=10, marker_opacity=0.5,
                    showlegend=False)

    if plot_trend:
        rm = pd.Series(data=ratio, index=time_display) \
            .rolling(dt.timedelta(days=45), min_periods=25, center=True, closed='both').median()
        fig.add_scatter(y=rm, x=rm.index, mode='lines', line_color='grey', line_width=5, showlegend=False)

    fig.update_layout(
        width=2000,
        height=600,
        xaxis=dict(title="",
                   title_font_size=font_size,
                   tickfont_size=font_size,
                   linecolor="#BCCCDC"),
        yaxis=dict(title="<b>Ratio measured vs. estimated</b> power [-]",
                   title_standoff=30,
                   title_font_size=font_size,
                   tickfont_size=font_size,
                   tickformat='0%',
                   range=yrange,
                   dtick=0.1,
                   linecolor="#BCCCDC")

    )
    _show(fig)
    if write_image:
        fig.write_image(_get_filename('time', pc_output))

    return fig


def plot_sums(pc_output, mode,
              write_image=False,
              anonymize=False):
    """Plot sums / average powers in intervals, measured vs. estimated.
    """
    assert_modules()
    # if not PLOTS_AVAILABLE:
    #     raise ModuleNotFoundError(PLOTS_AVAILABLE_MSG)
    if pc_output.n_intervals == 0:
        print('Nothing to plot, no PC intervals found.')
        return

    # estimated = np.mean(pc_output.tp_sp_estimated.magnitude)
    estimated_safe = np.mean(pc_output.tp_sp_estimated_safety.magnitude)
    measured = np.mean(pc_output.tp_sp_measured.magnitude)

    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]],
                        shared_xaxes=False,
                        shared_yaxes=False, vertical_spacing=0.001)

    font_size = 18 if mode == 'presentation' else 14
    labels = ['Average power<br><b>measured</b>', 'Average power<br><b>estimated</b>']
    x = [measured, estimated_safe]
    colors = ['rgba(192, 0, 0, 0.6)', 'rgba(68, 114, 196, 0.6)']

    text = [str(np.round(val, decimals=1)) + ' W/m²' for val in x]
    fig.append_trace(go.Bar(
        x=x,
        y=labels,
        marker=dict(
            color=colors,
            line=dict(color='rgba(90, 90, 90, 1.0)', width=1),
        ),
        orientation='h',
        width=0.4,
        text=text,
        textposition="outside",
        insidetextanchor="end",
        outsidetextfont_size=font_size
    ), 1, 1)

    plant_name = '<anonymized>' if anonymize else pc_output.plant.name
    if plant_name.startswith('FHW Arcon South'):
        plant_name = 'FHW Fernheizwerk Graz, Arcon South'
    title = (f"<b>Check of Performance</b> ({pc_output.pc_method_name}. "
             f"Equation: {pc_output.equation}).<br>"
             # f"Plant name: <b>{plant_name}</b>.<br>"
             f"<b>Data from</b> {pc_output.datetime_eval_start} to "
             f"{pc_output.datetime_eval_end}.<br>"
             f"n={pc_output.n_intervals} intervals, "
             f"interval duration "
             f"{pendulum.duration(seconds=pc_output.interval_length.total_seconds()).in_words(locale='en')}."
             )
    axis_range = [0, np.max(x).round(-1) + 100]
    fig.update_layout(
        title=dict(text=title,
                   xanchor='left',
                   xref='paper',
                   x=fig.layout.xaxis.domain[0],
                   # yanchor='top',
                   yanchor='bottom',
                   y=fig.layout.height,
                   font_size=font_size + 1,
                   ),
        autosize=False,
        height=700,
        width=2400,
        margin=dict(l=250, r=20, t=70, b=250),
        yaxis=dict(
            tickfont=dict(size=font_size),
            title_standoff=30,
            showgrid=False,
            showline=False,
            showticklabels=True,
            domain=[0, 0.85],
        ),
        xaxis=dict(
            title=dict(text='Specific thermal power [W/m²]',
                       font_size=font_size,
                       ),
            # title='Specific thermal power [W/m²]',
            title_font_size=font_size - 1,
            tickfont=dict(size=font_size),
            range=axis_range,
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True,
            domain=[0, 0.42],
        ),
    )

    # Adding labels
    # x_power = np.round([measured, estimated], decimals=1)
    # for xp, yp in zip(x_power, labels):
    #     # labeling the bar net worth
    #     annotations.append(dict(xref='x1', yref='y1',
    #                             y=yp, x=xp + 10,
    #                             text=str(xp) + ' W/m²',
    #                             align="left",
    #                             font=dict(family='Arial', size=font_size,
    #                                       color='rgb(0, 0, 0)'),
    #                             showarrow=False))

    # Guarantee fulfilled statement
    ratio = measured / estimated_safe
    fulfill_txt = 'not ' if ratio < 1 else ''
    ratio_text = (f'<b>Performance Check {fulfill_txt}fulfilled:'
                  f'</b> Ratio measured / estimated power = {ratio:.1%}'
                  f'<br>Combined safety factor f<sub>safe</sub> = {float(pc_output.safety_combined):.2} taken into account.')
    fig.add_annotation(
        text=ratio_text,
        font_size=font_size,
        xref='paper',
        x=fig.layout.xaxis.domain[0],
        align='left',
        # xanchor='left',
        y=-230 / fig.layout.height,
        yref='paper',
        showarrow=False,
    )

    fig.update_layout(showlegend=False)

    _show(fig)
    if write_image:
        fig.write_image(_get_filename('sums', pc_output))

    return fig


def plot_mask(pc_output, mask):
    """Produces a subplot figure with the PC criteria mask.
    mask is usually pc_obj._mask
    """
    assert_modules()
    if pc_output.n_intervals == 0:
        print('Nothing to plot, no PC intervals found.')
        return

    subplot_cols = mask.columns
    fig = make_subplots(rows=1 + len(subplot_cols), shared_xaxes=True, subplot_titles=subplot_cols)

    t = mask.index
    for i, col in enumerate(subplot_cols):
        fig.add_scatter(x=t, y=mask[col], row=i + 1, col=1,
                        mode='lines+markers', line={'width': 1}, marker={'size': 3})
        fig.add_scatter(x=t, y=mask[col], row=i + 1, col=1,
                        mode='lines', line={'width': 0.5})

    fig.layout.update(showlegend=False)
    _show(fig)

    return fig


def format_xaxis(ax,
                 tz,
                 interval,
                 # date_start=DAY_START, date_end=DAY_END,
                 minor_locator=mdates.MinuteLocator(interval=5),
                 major_locator=mdates.MinuteLocator(interval=15),
                 major_formatter=None):
    ax.set_xlim(interval[0], interval[1], auto=None)
    if major_formatter is None:
        major_formatter = mdates.DateFormatter("%#H:%M", tz=tz)
    ax.xaxis_date(tz)
    ax.xaxis.set_minor_locator(minor_locator)
    ax.xaxis.set_major_locator(major_locator)
    ax.xaxis.set_major_formatter(major_formatter)
    # adjust_xlabel_positions(ax, 4, remove_last=True)

    # Position extra text below x axis
    vertical_offset_points = 10
    offset = transforms.ScaledTranslation(0, vertical_offset_points / 72, ax.figure.dpi_scale_trans)
    ax.text(0, 0, f'{mdates.num2date(ax.get_xlim()[0]):%Y-%m-%d} ({str(tz)})', ha='left',
            transform=ax.transAxes - offset, va='top', fontsize=plt.rcParams['axes.labelsize'] - 1)

    return ax


def plot_sensor_data(array,
                     interval,
                     anonymize=False,
                     ):
    """Plot main sensor values in given interval.
    Using matplotlib here because plotly doesn't behave with subplot grid legends...
    """
    a = array
    p = array.plant

    fig, ax = plt.subplots(ncols=2, nrows=3, sharex=True,
                           constrained_layout=True,
                           gridspec_kw=dict(width_ratios=[1, 1], height_ratios=[3, 3, 2]),
                           )
    fig.subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)

    def _get_plot_data(sensor, unit):
        idx = sensor.data.index
        mask = (idx > interval[0]) & (idx <= interval[1])
        sub_series = sensor.data.loc[mask]
        sub_series = sub_series.pint.to(unit).pint.magnitude

        remove_virtual = lambda s: s.split('__', 1)[0] if '__' in s else s
        sub_series.rename(remove_virtual(sensor.raw_name), inplace=True)

        return sub_series

    def _format_subplot(ax_, title_txt, unit, ylims=None, has_legend=True):
        ax_.set_title(title_txt, loc='center')
        print_unit = lambda s: f"[{pint.Unit(s):~P}]" if s else "[dimensionless]"
        if isinstance(unit, list):
            ylabel_txt = ", ".join([print_unit(s) for s in unit])
        else:
            ylabel_txt = print_unit(unit)
        ax_.set_ylabel(ylabel_txt)
        if ylims is not None:
            ax_.set_ylim(ylims[0], ylims[1])
        if has_legend:
        # ax.get_legend().remove()
            legend = ax_.legend(loc="upper right")
            legend.get_frame().set_facecolor((1, 1, 1, 0.8))
            legend.set_zorder(1000)
        ax_.grid()
        ax_.set_axisbelow('line')

    # plot data (Fluid Temperatures)
    ax_ = ax[0][0]
    unit = 'degC'
    data = _get_plot_data(a.te_out, unit)
    ax_.plot(data, color=COLORS['orange'], label=data.name, zorder=10)
    data = _get_plot_data(a.te_op, unit)
    ax_.plot(data, color=COLORS['warm_gray'], label=data.name, zorder=15)
    data = _get_plot_data(a.te_in, unit)
    ax_.plot(data, color=COLORS['blue'], label=data.name, zorder=5)
    _format_subplot(ax_, "(a) Fluid Temperatures", unit)

    # plot data (Thermal Power)
    ax_ = ax[0][1]
    data = _get_plot_data(p.tp, 'kW')
    ax_.plot(data, color=COLORS['warm_gray'], label=data.name, zorder=5)
    _format_subplot(ax_, "(b) Thermal Power", 'kW', has_legend=False)

    # plot data (Solar Radiation)
    ax_ = ax[1][0]
    unit = 'W m**-2'
    if a.rd_gti is not None:
        data = _get_plot_data(a.rd_gti, unit)
        ax_.plot(data, color=COLORS['orange'], label=data.name, zorder=15)
    if a.rd_bti is not None:
        data = _get_plot_data(a.rd_bti, unit)
        ax_.plot(data, color=COLORS['cheese'], label=data.name, zorder=10)
    if a.rd_dti is not None:
        data = _get_plot_data(a.rd_dti, unit)
        ax_.plot(data, color=COLORS['dark_gray'], label=data.name, zorder=5)
    _format_subplot(ax_, "(c) Solar Radiation", unit, ylims=[0, 1200])

    # plot data (Ambient)
    ax_ = ax[1][1]
    data = _get_plot_data(p.te_amb, 'degC')
    ax_.plot(data, color=COLORS['cheese'], label=data.name, zorder=15)
    if p.ve_wind is not None:
        data = _get_plot_data(p.ve_wind, 'm s**-1')
        ax_.plot(data, color=COLORS['light_gray'], label=data.name, zorder=10)
        _format_subplot(ax_, "(d) Ambient", ['degC', 'm s**-1'])
    else:
        _format_subplot(ax_, "(d) Ambient", 'degC')

    # plot data (Angle of Incidence)
    ax_ = ax[2][0]
    data = _get_plot_data(a.aoi, 'deg')
    ax_.plot(data, color=COLORS['almost_black'], label=data.name, zorder=15)
    _format_subplot(ax_, "(e) Angle of Incidence", 'deg', has_legend=False)

    # plot data (Incidence Angle Modifier)
    ax_ = ax[2][1]
    data = _get_plot_data(a.iam, '')
    ax_.plot(data, color=COLORS['almost_black'], label=data.name, zorder=15)
    _format_subplot(ax_, "(f) Incidence Angle Modifier", '', has_legend=False)

    fig.set_size_inches(w=FULL_WIDTH, h=FULL_WIDTH / 1.9)
    fig.tight_layout()
    format_xaxis(ax[2][0], tz=p.tz_data, interval=interval)
    format_xaxis(ax[2][1], tz=p.tz_data, interval=interval)

    plant_name = '<anonymized>' if anonymize else array.plant.name
    if plant_name.startswith('FHW Arcon South'):
        plant_name = 'FHW Fernheizwerk Graz, Arcon South'
    title_txt = (f"Sensor data for plant: {plant_name}. "
                 # f"Data from {interval[0]} to {interval[1]}."
                 )
    plt.suptitle(title_txt, fontweight='bold',
                 x=0.05, y=0.98,
                 horizontalalignment='left')

    plt.tight_layout()

    plt.savefig(_get_filename('sensor_data'))
    plt.close()
    print(f'Saved plot "sensor_data".')


def _show(fig):
    fig.update_layout(dragmode='pan')
    config = {'scrollZoom': True,
              'displayModeBar': True,
              'modeBarButtonsToRemove': ['zoomIn', 'zoomOut'],
              'modeBarButtonsToAdd': ['drawline',
                                      'drawrect',
                                      'eraseshape'
                                      ]}
    fig.show(config=config)


def _get_filename(plot_name, pc_output=None):
    """Generate png file name from method, equation and plot name.
    """
    save_folder = Path(ROOT_DIR).parent / 'tests' / 'resources'
    if pc_output is None:
        filename = f'{plot_name}__{dt.datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    else:
        m = pc_output.evaluation_mode
        e = pc_output.equation
        filename = f'{m}_eq{e}__{plot_name}__{dt.datetime.now().strftime("%Y%m%d_%H%M%S")}.png'

    return save_folder / filename
