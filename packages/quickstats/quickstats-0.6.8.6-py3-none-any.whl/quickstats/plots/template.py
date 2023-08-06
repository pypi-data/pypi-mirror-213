from typing import Optional, Union, Dict, List, Tuple
from copy import deepcopy
import re
from cycler import cycler
from contextlib import contextmanager

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator, ScalarFormatter,
                               Locator, Formatter, AutoLocator,
                               MaxNLocator)

from quickstats.utils.common_utils import update_nested_dict
from quickstats import DescriptiveEnum

class ResultStatus(DescriptiveEnum):
    
    FINAL    = (0, "Finalised results", "")
    INT      = (1, "Internal results", "Internal")
    WIP      = (2, "Work in progress results", "Work in Progress")
    PRELIM   = (3, "Preliminary results", "Preliminary")
    OPENDATA = (4, "Open data results", "Open Data")

    def __new__(cls, value:int, description:str="", display_text:str=""):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        obj.display_text = display_text
        return obj
        
class NumericFormatter(ScalarFormatter):
    def __call__(self, x, pos=None):
        tmp_format = self.format
        if (x.is_integer() and abs(x) < 1e3):
            self.format = re.sub(r"1\.\d+f", r"1.0f", self.format)
        result = super().__call__(x, pos)
        self.format = tmp_format
        return result

TEMPLATE_STYLES = {
    'default': {
        'figure':{
            'figsize': (11.111, 8.333),
            'dpi': 72,
            'facecolor': "#FFFFFF"
        },
        'legend_Line2D': {
            'linewidth': 3
        },
        'annotation':{
            'fontsize': 12
        },
        'axis': {
            'major_length': 16,
            'minor_length': 8,
            'major_width': 2,
            'minor_width': 1,
            'spine_width': 2,
            'labelsize': 20,
            'offsetlabelsize': 20,
            'tick_bothsides': True
        },
        'xtick':{
            'format': 'numeric',
            'locator': 'auto',
            'steps': None,
            'prune': None,
            'integer': False
        },
        'ytick':{
            'format': 'numeric',
            'locator': 'auto',
            'steps': None,
            'prune': None,
            'integer': False
        },        
        'xlabel': {
            'fontsize': 22,
            'loc' : 'right',
            'labelpad': 10
        },
        'ylabel': {
            'fontsize': 22,
            'loc' : 'top',
            'labelpad': 10
        },
        'text':{
            'fontsize': 20,
        },
        'plot':{
            'linewidth': 2
        },
        'hist': {
            'linewidth': 2
        },
        'errorbar': {
            "marker": 'x',
            "linewidth": 0,
            "markersize": 0,
            "elinewidth": 1,
            "capsize": 2,
            "capthick": 1,
            "zorder": 1
        },
        'fill_between': {
            "alpha": 0.5
        },
        'legend':{
            "fontsize": 20
        },
        'ratio_frames':{
            'height_ratios': (3, 1),
            'hspace': 0.07            
        },
        'barh': {
            'height': 0.5
        },
        'bar': {
        }
    }
}

ANALYSIS_OPTIONS = {
    'default': {
        'status': 'int',
        'loc': (0.05, 0.95),
        'fontsize': 25
    },
    'ATLAS_Run2': {
        'colab': 'ATLAS',
        'status': 'int', 
        'energy' : '13 TeV', 
        'lumi' : "140 fb$^{-1}$",
        'fontsize': 25
    }
}

AXIS_LOCATOR_MAPS = {
    'auto': AutoLocator,
    'maxn': MaxNLocator
}

def handle_has_label(handle):
    try:
        label = handle.get_label()
        has_label = (label and not label.startswith('_'))
    except:
        has_label = False
    return has_label

def parse_styles(styles:Optional[Union[Dict, str]]=None):
    default_styles = deepcopy(TEMPLATE_STYLES['default'])
    if styles is None:
        styles = default_styles
    elif isinstance(styles, str):
        template_styles = TEMPLATE_STYLES.get(styles, None)
        if template_styles is None:
            raise ValueError(f"template styles `{styles}` not found")
        styles = update_nested_dict(default_styles, deepcopy(template_styles))
    else:
        styles = update_nested_dict(default_styles, deepcopy(styles))
    return styles

def parse_analysis_label_options(options:Optional[Dict]=None):
    default_options = deepcopy(ANALYSIS_OPTIONS['default'])
    if options is None:
        options = default_styles
    elif isinstance(options, str):
        template_options = ANALYSIS_OPTIONS.get(options, None)
        if template_options is None:
            raise ValueError(f"template analysis label options `{options}` not found")
        options = update_nested_dict(default_options, deepcopy(template_options))
    else:
        options = update_nested_dict(default_options, deepcopy(options))
    return options

def ratio_frames(height_ratios:Tuple[int]=(3, 1), hspace:float=0.07,
                 logx:bool=False, logy:bool=False, 
                 styles:Optional[Union[Dict, str]]=None,
                 analysis_label_options:Optional[Union[Dict, str]]=None,
                 prop_cycle:Optional[List[str]]=None,
                 figure_index:Optional[int]=None):
    if figure_index is None:
        plt.clf()
    else:
        plt.figure(figure_index)
    styles = parse_styles(styles)
    gridspec_kw = {
        "height_ratios": height_ratios,
        "hspace": hspace
    }
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, gridspec_kw=gridspec_kw,
                                   sharex=True, **styles['figure'])
    
    if logx:
        ax1.set_xscale('log')
        ax2.set_xscale('log')
        
    if logy:
        ax1.set_yscale('log')
        
    format_axis_ticks(ax1, x_axis=True, y_axis=True, x_axis_styles={"labelbottom":False},
                      xtick_styles=styles['xtick'], ytick_styles=styles['ytick'], **styles['axis'])
    format_axis_ticks(ax2, x_axis=True, y_axis=True, xtick_styles=styles['xtick'],
                      ytick_styles=styles['ytick'], **styles['axis'])
    
    if analysis_label_options is not None:
        draw_analysis_label(ax1, text_options=styles['text'], **analysis_label_options)
        
    if prop_cycle is not None:
        ax1.set_prop_cycle(prop_cycle)
    
    return ax1, ax2

def single_frame(logx:bool=False, logy:bool=False, 
                 styles:Optional[Union[Dict, str]]=None,
                 analysis_label_options:Optional[Union[Dict, str]]=None,
                 prop_cycle:Optional[List[str]]=None,
                 figure_index:Optional[int]=None):
    if figure_index is None:
        plt.clf()
    else:
        plt.figure(figure_index)
    styles = parse_styles(styles)
    fig, ax = plt.subplots(nrows=1, ncols=1, **styles['figure'])
    
    if logx:
        ax.set_xscale('log')
    if logy:
        ax.set_yscale('log')
        
    format_axis_ticks(ax, x_axis=True, y_axis=True, xtick_styles=styles['xtick'],
                      ytick_styles=styles['ytick'], **styles['axis'])
    
    if analysis_label_options is not None:
        draw_analysis_label(ax, text_options=styles['text'], **analysis_label_options)
        
    if prop_cycle is not None:
        ax.set_prop_cycle(prop_cycle)
    
    return ax

def suggest_markersize(nbins:int):
    bin_max  = 200
    bin_min  = 40
    size_max = 8
    size_min = 2
    if nbins <= bin_min:
        return size_max
    elif (nbins > bin_min) and (nbins <= bin_max):
        return ((size_min - size_max) / (bin_max - bin_min))*(nbins - bin_min) + size_max
    return size_min

def format_axis_ticks(ax, x_axis=True, y_axis=True, major_length:int=16, minor_length:int=8,
                      spine_width:int=2, major_width:int=2, minor_width:int=1, direction:str='in',
                      label_bothsides:bool=False, tick_bothsides:bool=False,
                      labelsize:Optional[int]=None,
                      offsetlabelsize:Optional[int]=None,
                      x_axis_styles:Optional[Dict]=None, 
                      y_axis_styles:Optional[Dict]=None,
                      xtick_styles:Optional[Dict]=None,
                      ytick_styles:Optional[Dict]=None):
    if x_axis:
        if (ax.get_xaxis().get_scale() != 'log'):
            ax.xaxis.set_minor_locator(AutoMinorLocator())
        styles = {"labelsize":labelsize}
        styles['labeltop'] = label_bothsides
        styles['labelbottom'] = True
        styles['top'] = tick_bothsides
        styles['bottom'] = True
        styles['direction'] = direction
        if x_axis_styles is not None:
            styles.update(x_axis_styles)
        ax.tick_params(axis="x", which="major", length=major_length,
                       width=major_width, **styles)
        ax.tick_params(axis="x", which="minor", length=minor_length,
                       width=minor_width, **styles)
    if y_axis:
        if (ax.get_yaxis().get_scale() != 'log'):
            ax.yaxis.set_minor_locator(AutoMinorLocator())    
        styles = {"labelsize":labelsize}
        styles['labelleft'] = True
        styles['labelright'] = label_bothsides
        styles['left'] = True
        styles['right'] = tick_bothsides
        styles['direction'] = direction
        if y_axis_styles is not None:
            styles.update(y_axis_styles)
        ax.tick_params(axis="y", which="major", length=major_length,
                       width=major_width, **styles)
        ax.tick_params(axis="y", which="minor", length=minor_length,
                       width=minor_width, **styles)
        
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(spine_width)
        
    set_axis_tick_styles(ax.xaxis, xtick_styles)
    set_axis_tick_styles(ax.yaxis, ytick_styles)

    # take care of offset labels
    if offsetlabelsize is None:
        offsetlabelsize = labelsize
    # update the offset text
    if plt.gca().__class__.__name__ != "AxesSubplot":
        plt.tight_layout()
        
    if ax.xaxis.get_offset_text().get_text():
        ax.xaxis.get_offset_text().set_fontsize(offsetlabelsize)
        ax.xaxis.labelpad = ax.xaxis.labelpad + ax.xaxis.get_offset_text().get_fontsize()
    if ax.yaxis.get_offset_text().get_text():
        ax.yaxis.get_offset_text().set_fontsize(offsetlabelsize)
        ax.yaxis.labelpad = ax.yaxis.labelpad + ax.yaxis.get_offset_text().get_fontsize()

def set_axis_tick_styles(ax, styles=None):   
    if styles is None:
        return None
    if ax.get_scale() == "log":
        return None
    fmt = styles['format']
    if fmt is not None:
        formatter = None
        if isinstance(fmt, str):
            if fmt == 'numeric':
                formatter = NumericFormatter()
        if isinstance(fmt, Formatter):
            formatter = fmt
        if formatter is None:
            raise ValueError(f"unsupported axis tick format {fmt}")
        ax.set_major_formatter(formatter)
        
    locator = ax.get_major_locator()
    
    if isinstance(locator, (AutoLocator, MaxNLocator)):
        new_locator = AXIS_LOCATOR_MAPS.get(styles['locator'].lower(), type(locator))()
        try:
            available_params = list(new_locator.default_params)
        except:
            available_params = ['steps', 'prune', 'integer']
        locator_params = {}
        for param in available_params:
            value = styles.get(param, None)
            if value is not None:
                locator_params[param] = value
        new_locator.set_params(**locator_params)
        ax.set_major_locator(new_locator)
                

def centralize_axis(ax, which='x', ref_value:float=0, padding:float=0.1):
    if which == 'x':
        get_lim = ax.get_xlim
        set_lim = ax.set_xlim
    elif which == 'y':
        get_lim = ax.get_ylim
        set_lim = ax.set_ylim    
    limits = get_lim()
    vmax = np.max(np.abs([ref_value - limits[0], limits[1] - ref_value]))
    pad = (limits[1] - limits[0]) * padding
    set_lim(ref_value - vmax - pad, ref_value + vmax + pad)
        
def parse_transform(obj:str):
    if not obj:
        transform = None
    elif obj == 'figure':
        transform = plt.gcf().transFigure
    elif obj == 'axis':
        transform = plt.gca().transAxes
    elif obj == 'data':
        transform = plt.gca().transData
    return transform

def create_transform(transform_x:str='axis', transform_y:str='axis'):
    transform = transforms.blended_transform_factory(parse_transform(transform_x), 
                                                     parse_transform(transform_y))
    return transform

def get_box_dimension(box):
    axis = plt.gca()
    plt.gcf().canvas.draw()
    bb = box.get_window_extent()
    points = bb.transformed(axis.transAxes.inverted()).get_points().transpose()
    xmin = np.min(points[0])
    xmax = np.max(points[0])
    ymin = np.min(points[1])
    ymax = np.max(points[1])
    return xmin, xmax, ymin, ymax

def draw_sigma_bands(axis, ymax:float, height:float=1.0):
    # +- 2 sigma band
    axis.add_patch(Rectangle((-2, -height/2), 2*2, ymax + height/2, fill=True, color='yellow'))
    # +- 1 sigma band
    axis.add_patch(Rectangle((-1, -height/2), 1*2, ymax + height/2, fill=True, color='lime'))
    
def draw_sigma_lines(axis, ymax:float, height:float=1.0, **styles):
    y = [-height/2, ymax*height - height/2]
    axis.add_line(Line2D([-1, -1], y, **styles))
    axis.add_line(Line2D([+1, +1], y, **styles))
    axis.add_line(Line2D([0, 0], y, **styles)) 
    
def draw_hatches(axis, ymax, height=1.0, **styles):
    x_min    = axis.get_xlim()[0]
    x_max    = axis.get_xlim()[1]
    x_range  = x_max - x_min
    y_values = np.arange(0, height*ymax, 2*height) - height/2
    transform = create_transform(transform_x='axis', transform_y='data')
    for y in y_values:
        axis.add_patch(Rectangle((0, y), 1, 1, **styles, zorder=-1, transform=transform))

def draw_text(axis, x:float, y:float, s:str,
              transform_x:str='axis',
              transform_y:str='axis',
              **styles):
    with change_axis(axis):
        transform = create_transform(transform_x, transform_y)
        text = axis.text(x, y, s, transform=transform, **styles)
        xmin, xmax, ymin, ymax = get_box_dimension(text)
    return xmin, xmax, ymin, ymax

@contextmanager
def change_axis(axis):
    current_axis = plt.gca()
    plt.sca(axis)
    yield
    plt.sca(current_axis)

def draw_analysis_label(axis, loc=(0.05, 0.95), fontsize:float=25, status:str='int',
                        energy:Optional[str]=None, lumi:Optional[str]=None,
                        colab:str='ATLAS', extra_text:Optional[str]=None, dy:float=0.05,
                        transform_x:str='axis', transform_y:str='axis',
                        vertical_align:str='top', horizontal_align:str='left',
                        text_options:Optional[Dict]=None):
    """
    Draw analysis label and additional texts on a given axis.
    
        Parameters
        ---------------------------------------------------------------
        axis: matplotlib.pyplot.axis
            Axis to be drawn on.
        loc: (float, float), default = (0.05, 0.95)
            The location of the analysis label and additional texts.
        fontsize: float, default = 25
            Font size of the analysis label and the status label.
        status: str or ResultStatus, default = 'int'
            Display text for the analysis status. Certain keywords can be used to convert
            automatically to the corresponding built-in status texts
            (see `ResultStatus`).
        energy: (optional) str
            Display text for the Center-of-mass energy. A prefix of "\sqrt{s} = " will be
            automatically appended to the front of the text.
        lumi: (optional) str
            Display text for the luminosity. It will be displayed as is.
        colab: str
            Display text for the collaboration involved in the analysis. It will be
            bolded and italised.
        extra_text: (optional) str
            Extra text to be displayed after energy and luminosity texts. A new line
            can be added by adding a double-slash, i.e. "//".
        dy: float, default = 0.05
            Vertical separation between each line of text in the axis coordinates.
        transform_x: str, default = 'axis'
            Coordinate transform for the x location of the analysis label.
        transform_y: str, default = 'axis'
            Coordinate transform for the y location of the analysis label.
        vertical_align: str, default = 'top'
            Vertical alignment of the analysis label.
        horizontal_align: str, default = 'top'
            Horizontal alignment of the analysis label.
        text_options: (optional), dict
            A dictionary specifying the styles for drawing texts.
    """
    try:
        status_text = ResultStatus.parse(status).display_text
    except:
        status_text = status
    
    with change_axis(axis):
        transform = create_transform(transform_x, transform_y)
        x, y = loc
        # draw collaboration label
        text_colab = axis.text(x, y, colab, fontsize=fontsize, transform=transform,
                               horizontalalignment=horizontal_align,
                               verticalalignment=vertical_align,
                               fontproperties={"weight":"bold", "style":"italic"})
        xmin, xmax, ymin, _ = get_box_dimension(text_colab)
        text_width = xmax - xmin
        dx = text_width / 15
        # draw status label
        text_status = axis.text(xmax + dx, ymin, status_text, fontsize=fontsize,
                                transform=axis.transAxes,
                                horizontalalignment='left',
                                verticalalignment='bottom')
        
    # draw energy and luminosity labels as well as additional texts
    elumi_text = []
    if energy is not None:
        elumi_text.append(r"$\sqrt{s} = $" + energy )
    if lumi is not None:
        elumi_text.append(lumi)
    elumi_text = ", ".join(elumi_text)

    all_texts = []
    if elumi_text:
        all_texts.append(elumi_text)

    if extra_text is not None:
        all_texts.extend(extra_text.split("//"))

    if text_options is None:
        text_options = {}

    for text in all_texts:
        _, _, ymin, _ = draw_text(axis, xmin, ymin - dy, text, **text_options)