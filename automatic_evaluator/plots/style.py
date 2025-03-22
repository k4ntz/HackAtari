import seaborn as sns   

STYLE = {
    # Figure dimensions
    "figure_size": (12, 6),
    "tall_figure_size": (12, 8),
    
    # Font sizes
    "title_fontsize": 16,
    "axis_label_fontsize": 12,
    "legend_fontsize": 10,
    
    # Color settings
    "palette": "husl",
    
    # Legend configuration
    "legend": {
        "bbox_to_anchor": (1.05, 1),
        "loc": "upper left",
        "title": "Modifications",
        "frameon": True,
        "edgecolor": "black",
        "facecolor": "white",
        "framealpha": 1.0,
        "fancybox": False,
        "legend_fontsize": 10
    },
    
    # Grid styling
    "grid": {
        "alpha": 0.3,
        "linestyle": "--"
    },
    
    # Zero line styling
    "zero_line": {
        "color": "black",
        "linestyle": "--",
        "linewidth": 1
    },
    
    # Plot margins
    "subplots_adjust_right": 0.75,

    # Add palette color access
    "palette_colors": sns.color_palette("husl"),
    
    # Boxplot specific styling
    "boxplot": {
        "linewidth": 1.5,
        "width": 0.3,
        "flierprops": {
            "marker": "o",
            "markersize": 4,
            "markerfacecolor": "black"
        }
    },

    "flierprops": {
        'marker': 'o',
        'markersize': 4,
        'markerfacecolor': 'black',
        'markeredgecolor': 'black'
    },

    "scatter": {
        "alpha": 0.7,
        "edgecolor": "white",
        "s": 40 
    }
}
