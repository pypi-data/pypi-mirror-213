from typing import Dict, Optional, Union, List, Sequence

from itertools import repeat

import numpy as np
import pandas as pd

from quickstats.plots import AbstractPlot
from quickstats.plots.template import create_transform
from quickstats.utils.common_utils import combine_dict
from quickstats.maths.interpolation import get_regular_meshgrid
from matplotlib.lines import Line2D


class Likelihood2DPlot(AbstractPlot):

    CONFIG = {
        # intervals to include in the plot
        "interval_formats": {
            "68_95"               : ('0.68', '0.95'),
            "one_two_sigma"       : ('1sigma', '2sigma'),
            "68_95_99"            : ('0.68', '0.95', '0.99'),
            "one_two_three_sigma" : ('1sigma', '2sigma', '3sigma')
        },
        'highlight_styles': {
            'linewidth': 0,
            'marker': '*',
            'markersize': 20,
            'color': '#E9F1DF',
            'markeredgecolor': 'black'
        },
        'bestfit_styles':{
            'marker': 'P',
            'linewidth': 0,
            'markersize': 15
        },
        'contour_styles': {
            'linestyles': 'solid',
            'linewidths': 3
        },
        'bestfit_label': "Best fit ({x:.2f}, {y:.2f})",
        'cmap': 'GnBu',
        'interpolation': 'cubic',
        'num_grid_points': 500,
    }
    
    # qmu from https://pdg.lbl.gov/2018/reviews/rpp2018-rev-statistics.pdf#page=31
    coverage_proba_data = {
        '0.68': {
            'qmu': 2.30,
            'label': '68% CL',
            'color': "hh:darkblue"
        },
        '1sigma': {  
            'qmu': 2.30, # 68.2%
            'label': '1 $\sigma$',
            'color': "hh:darkblue"
        },
        '0.90': {
            'qmu': 4.61,
            'label': '90% CL',
            'color': "#36b1bf"
        },
        '0.95': {
            'qmu': 5.99,
            'label': '95% CL',
            'color': "#F2385A"
        },
        '2sigma': {
            'qmu': 6.18, # 95.45%
            'label': '2 $\sigma$',
            'color': "#F2385A"
        },
        '0.99': {
            'qmu': 9.21,
            'label': '99% CL',
            'color': "#FDC536"
        },
        '3sigma': {
            'qmu': 11.83, # 99.73%
            'label': '3 $\sigma$',
            'color': "#FDC536"
        }
    }

    def __init__(self, data_map: Union[pd.DataFrame, Dict[str, pd.DataFrame]],
                 label_map: Optional[Dict] = None,
                 styles_map: Optional[Dict] = None,
                 config_map: Optional[Dict] = None,
                 color_cycle=None,
                 styles: Optional[Union[Dict, str]] = None,
                 analysis_label_options: Optional[Dict] = None,
                 config: Optional[Dict] = None):

        self.data_map = data_map
        self.label_map = label_map
        self.styles_map = styles_map
        self.config_map = config_map
        self.highlight_data = []
        self.contours = None

        super().__init__(color_cycle=color_cycle,
                         styles=styles,
                         analysis_label_options=analysis_label_options,
                         config=config)
        
    def get_sigma_levels(self, interval_format:str="one_two_three_sigma"):
        if interval_format not in self.config['interval_formats']:
            choices = ','.join([f'"{choice}"' for choice in self.config['interval_formats']])
            raise ValueError(f'undefined sigma interval format: {interval_format} (choose from {choices})')
        sigma_levels = self.config['interval_formats'][interval_format]
        return sigma_levels

    def draw_single_data(self, ax, data: pd.DataFrame,
                         xattrib: str, yattrib: str,
                         zattrib: str = 'qmu',
                         styles: Optional[Dict] = None,
                         clabel_size=None, show_colormesh=False,
                         interval_format:str="one_two_three_sigma"):
        config = combine_dict(self.config)
        sigma_levels = self.get_sigma_levels(interval_format=interval_format)
        sigma_values = [self.coverage_proba_data[level]['qmu'] for level in sigma_levels]
        sigma_labels = [self.coverage_proba_data[level]['label'] for level in sigma_levels]
        sigma_colors = [self.coverage_proba_data[level]['color'] for level in sigma_levels]

        interpolate_method = config.get('interpolation', None)
        if interpolate_method is not None:
            from scipy import interpolate
            x, y, z = data[xattrib], data[yattrib], data[zattrib]
            n = config.get('num_grid_points', 500)
            X, Y = get_regular_meshgrid(x, y, n=n)
            Z = interpolate.griddata(np.stack((x, y), axis=1), z, (X, Y), interpolate_method)
        else:
            X_unique = np.sort(data[xattrib].unique())
            Y_unique = np.sort(data[yattrib].unique())
            X, Y = np.meshgrid(X_unique, Y_unique)
            Z = (data.pivot_table(index=xattrib, columns=yattrib, values=zattrib).T.values
                 - data[zattrib].min())
            
        if show_colormesh:
            cmap = config['cmap']
            im = ax.pcolormesh(X, Y, Z, cmap=cmap, shading='auto')
            import matplotlib.pyplot as plt
            self.cbar = plt.colorbar(im, ax=ax, **config['colorbar'])
            self.cbar.set_label(**config['colorbar_label'])
            
        if sigma_values:
            cp = ax.contour(X, Y, Z, levels=sigma_values, colors=sigma_colors,
                            **config['contour_styles'])
            if clabel_size is not None:
                ax.clabel(cp, inline=True, fontsize=clabel_size)
                
        line_styles = self._get_line_styles(config['contour_styles'])
        custom_handles = [Line2D([0], [0], color=color, label=label, **styles) \
                          for color, label, styles in zip(sigma_colors, sigma_labels, line_styles)]
        self.update_legend_handles(dict(zip(sigma_labels, custom_handles)))
        self.legend_order.extend(sigma_labels)
        return custom_handles
    
    def _get_line_styles(self, styles:Dict):
        style_key_map = {
            'linestyles': 'linestyle',
            'linewidths': 'linewidth'
        }
        new_styles = {new_name: styles[old_name] for old_name, new_name \
                      in style_key_map.items() if old_name in styles}
        sizes = []
        for style in new_styles.values():
            if (isinstance(style, Sequence)) and (not isinstance(style, str)):
                sizes.append(len(style))
            else:
                sizes.append(1)
        if not sizes:
            return repeat({})
        if not len(np.unique(sizes)) == 1:
            raise ValueError('contour line styles have inconsistent sizes')
        size = np.unique(sizes)[0]
        if size == 1:
            return repeat(new_styles)
        list_styles = []
        for i in range(size):
            styles_i = {key: value[i] for key, value in new_styles.items()}
            list_styles.append(styles_i)
        return list_styles

    def draw(self, xattrib:str, yattrib:str, zattrib:str='qmu', xlabel: Optional[str] = "",
             ylabel: Optional[str] = "", zlabel: Optional[str] = "$-2\Delta ln(L)$",
             ymax:Optional[float]=None, ymin:Optional[float]=None,
             xmin:Optional[float]=None, xmax:Optional[float]=None,
             clabel_size=None, draw_sm_line: bool = False, draw_bestfit:bool=True,
             show_colormesh=False, show_legend=True,
             interval_format:str="one_two_three_sigma"):
        self.reset_legend_data()
        ax = self.draw_frame()
        self.contours = {'keys': [], 'contours': [], 'levels': []}
        if isinstance(self.data_map, pd.DataFrame):
            self.draw_single_data(ax, self.data_map, xattrib=xattrib, yattrib=yattrib,
                                  zattrib=zattrib, styles=self.styles_map,
                                  clabel_size=clabel_size, show_colormesh=show_colormesh,
                                  interval_format=interval_format)
        else:
            raise ValueError("invalid data format")
            
        """
        elif isinstance(self.data_map, dict):
            if self.styles_map is None:
                styles_map = {k: None for k in self.data_map}
            else:
                styles_map = self.styles_map
            if self.label_map is None:
                label_map = {k: k for k in self.data_map}
            else:
                label_map = self.label_map
            if self.config_map is None:
                config_map = {k: k for k in self.data_map}
            else:
                config_map = self.config_map
                
            for key in self.data_map:
                self.contours['keys'].append(key)
                data = self.data_map[key]
                styles = styles_map.get(key, None)
                label = label_map.get(key, "")
                config = config_map.get(key, None)
                config = combine_dict(self.CONFIG, config)
                handle = self.draw_single_data(ax, data,
                                               xattrib=xattrib,
                                               yattrib=yattrib,
                                               zattrib=zattrib,
                                               styles=styles,
                                               config=config,
                                               show_colormesh=show_colormesh)
                         
        """
        
        highlight_index = 0
        
        if draw_bestfit and isinstance(self.data_map, pd.DataFrame):
            bestfit_idx = np.argmin(self.data_map[zattrib].values)
            bestfit_x   = self.data_map.iloc[bestfit_idx][xattrib]
            bestfit_y   = self.data_map.iloc[bestfit_idx][yattrib]
            highlight_data = {
                'x': bestfit_x,
                'y': bestfit_y,
                'label': self.config["bestfit_label"].format(x=bestfit_x, y=bestfit_y),
                'styles': self.config["bestfit_styles"]
            }
            self.draw_highlight(ax, highlight_data, highlight_index)
            highlight_index += 1
        
        if self.highlight_data is not None:
            for i, h in enumerate(self.highlight_data):
                self.draw_highlight(ax, h, highlight_index + i)

        if draw_sm_line:
            sm_line_styles = self.config['sm_line_styles']
            sm_values = self.config['sm_values']
            transform = create_transform(
                transform_y="axis", transform_x="data")
            ax.vlines(sm_values[0], ymin=0, ymax=1, zorder=0, transform=transform,
                      **sm_line_styles)
            transform = create_transform(
                transform_x="axis", transform_y="data")
            ax.hlines(sm_values[1], xmin=0, xmax=1, zorder=0, transform=transform,
                      **sm_line_styles)

        if show_legend:
            handles, labels = self.get_legend_handles_labels()
            ax.legend(handles, labels, **self.styles['legend'])

        self.draw_axis_components(ax, xlabel=xlabel, ylabel=ylabel)
        self.set_axis_range(ax, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)

        return ax

    def draw_highlight(self, ax, data, index=0):
        styles = data['styles']
        if styles is None:
            styles = self.config['highlight_styles']
        handle = ax.plot(data['x'], data['y'], label=data['label'], **styles)
        self.update_legend_handles({f'highlight_{index}': handle[0]})
        self.legend_order.append(f'highlight_{index}')

    def add_highlight(self, x: float, y: float, label: str = "SM prediction",
                      styles: Optional[Dict] = None):
        highlight_data = {
            'x': x,
            'y': y,
            'label': label,
            'styles': styles
        }
        self.highlight_data.append(highlight_data)
