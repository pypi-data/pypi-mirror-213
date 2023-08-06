import warnings
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pandas.api.types import is_numeric_dtype
import pandas as pd


def import_style(filepath: str) -> None:
    """
    This function imports a style file for matplotlib plots.

    Args:
      filepath (str):   A string representing the file path of the style sheet to be imported. The style
                        sheet should be in the correct format for matplotlib to use.
    """
    plt.style.use(filepath)


def create_horizontal_barplot(
    data,
    x_var,
    y_var,
    x_label="",
    title="",
    titlefontsize=12,
    figsize=(10, 10),
    ax=None,
) -> plt.Axes:
    """
    This function creates a horizontal bar plot using the input data and variables.
    
    Args:
      data: The data to be plotted, in the form of a pandas DataFrame or a dictionary.
      x_var: The variable to be plotted on the x-axis.
      y_var: The variable used for the y-axis of the horizontal barplot.
      x_label: The label for the x-axis of the horizontal barplot.
      title: The title of the horizontal bar plot.
      titlefontsize: The font size of the title of the horizontal bar plot. Defaults to 12
      figsize: The size of the figure in inches (width, height).
      ax: The ax parameter is an optional parameter that allows the user to pass in an existing
    matplotlib Axes object to plot on. If this parameter is not provided, the function will create a new
    figure and Axes object to plot on.
    
    Returns:
      a matplotlib Axes object.
    """
    with plt.rc_context(
        {"axes.labelcolor": "black", "ytick.labelleft": True, "xtick.labelbottom": True}
    ):
        if ax is None:
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)
        y_pos = np.arange(len(data[y_var]))
        _ = ax.barh(y_pos, data[x_var], align="center")
        ax.set_yticks(y_pos)
        ax.set_yticklabels(data[y_var])
        ax.invert_yaxis()
        ax.set_xlabel(x_label)
        ax.set_title(title, fontsize=titlefontsize)
        return ax


def create_scatterplot(data, x_var, y_var, title="", titlefontsize=12, figsize=(10, 10), ax=None) -> plt.Axes:
    """
    This function creates a scatterplot with specified data, x and y variables, title, and axis
    parameters.
    
    Args:
      data: The dataset that contains the variables to be plotted.
      x_var: The name of the variable to be plotted on the x-axis of the scatterplot.
      y_var: The variable to be plotted on the y-axis of the scatterplot.
      title: The title of the scatterplot (default is an empty string).
      titlefontsize: The font size of the title of the scatterplot. Defaults to 12
      figsize: The size of the figure in inches (width, height).
      ax: The ax parameter is an optional parameter that allows the user to specify an existing
    matplotlib Axes object to plot the scatterplot on. If ax is not provided, a new figure and Axes
    object will be created.
    
    Returns:
      a matplotlib Axes object.
    """
    with plt.rc_context(
        {"axes.labelcolor": "black", "ytick.labelleft": True, "xtick.labelbottom": True}
    ):
        if ax is None:
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)
        ax.scatter(data[x_var], data[y_var])
        ax.set_xlabel(x_var)
        ax.set_ylabel(y_var)
        ax.set_title(title, fontsize=titlefontsize)
        return ax


def create_heatmap(
    data,
    complete=True,
    title="",
    titlefontsize=12,
    figsize=(10, 10),
    ax=None,
) -> plt.Axes:
    """
    This function creates a heatmap with customizable options using the Seaborn library in Python.
    
    Args:
      data: The data to be plotted in the heatmap. It should be a 2D array or a pandas DataFrame.
      complete: A boolean parameter that determines whether to show the complete heatmap or only the
    bottom half of it. If set to True, the complete heatmap will be shown. If set to False, only the
    bottom half of the heatmap will be shown. Defaults to True
      title: The title of the heatmap plot.
      titlefontsize: The font size of the title of the heatmap. Defaults to 12
      figsize: The size of the figure (width, height) in inches.
      ax: The matplotlib Axes object to plot the heatmap on. If None, a new figure and Axes object will
    be created.
    
    Returns:
      a matplotlib Axes object.
    """
    with plt.rc_context(
        {"axes.labelcolor": "black", "ytick.labelleft": True, "xtick.labelbottom": True}
    ):
        if complete:
            mask = None
        else:
            # only show the bottom half of the heatmap
            mask = np.triu(np.ones_like(data, dtype=bool))
        if ax is None:
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)
        sns.heatmap(
            data,
            ax=ax,
            mask=mask,
            vmax=1,
            vmin=-1,
            annot=True,
            xticklabels=1,
            yticklabels=1,
            center=0,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.5},
            cmap="coolwarm",
        )
        ax.set_title(title, fontsize=titlefontsize, y=1.0)
        return ax


def make_barplot_labels(ax, rects) -> None:
    """
    The function adds labels to a barplot with the height of each bar.

    Args:
      ax:       The ax parameter is a matplotlib Axes object, which represents the plot on which the barplot
                is being drawn. It is used to add text labels to the bars in the plot.
      rects:    A list of Rectangle objects representing the bars in a bar plot.
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(
            rect.get_x() + rect.get_width() / 2.0,
            1.05 * height,
            "%d" % int(height),
            ha="center",
            va="bottom",
            color="blue",
            backgroundcolor="lightgrey",
        )


def make_boxplot_labels(ax, boxplot) -> None:
    """
    This function creates labels for a boxplot with information on the median, percentiles, caps, and
    fliers.

    Args:
      ax:       The matplotlib Axes object on which the boxplot is plotted.
      boxplot:  A dictionary containing the components of a boxplot (e.g. boxes, whiskers, medians, caps,
                fliers) as Line2D instances.
    """
    # Grab the relevant Line2D instances from the boxplot dictionary
    iqr = boxplot["boxes"][0]
    caps = boxplot["caps"]
    med = boxplot["medians"][0]
    fly = boxplot["fliers"][0]
    # The x position of the median line
    xpos = med.get_xdata()
    # Lets make the text have a horizontal offset which is some
    # fraction of the width of the box
    xoff = 0.10 * (xpos[1] - xpos[0])
    # The x position of the labels
    xlabel = xpos[1] + xoff
    # The median is the y-position of the median line
    median = med.get_ydata()[1]
    # The 25th and 75th percentiles are found from the
    # top and bottom (max and min) of the box
    pc25 = iqr.get_ydata().min()
    pc75 = iqr.get_ydata().max()
    # The caps give the vertical position of the ends of the whiskers
    capbottom = caps[0].get_ydata()[0]
    captop = caps[1].get_ydata()[0]
    # Make some labels on the figure using the values derived above
    ax.text(xlabel, median, "median: {:6.3g}".format(median), va="center")
    ax.text(xlabel, pc25, "25th percentile: {:6.3g}".format(pc25), va="center")
    ax.text(xlabel, pc75, "75th percentile: {:6.3g}".format(pc75), va="center")
    ax.text(xlabel, capbottom, "bottom cap: {:6.3g}".format(capbottom), va="center")
    ax.text(xlabel, captop, "top cap: {:6.3g}".format(captop), va="center")
    # Many fliers, so we loop over them and create a label for each one
    for flier in fly.get_ydata():
        ax.text(1 + xoff, flier, "{:6.3g}".format(flier), va="center")


def create_boxplot(
    data,
    x_var,
    y_var=None,
    color_by=None,
    title="",
    titlefontsize=12,
    figsize=(10, 10),
    ax=None,
) -> plt.Axes:
    """
    This function creates a boxplot using seaborn library with optional parameters for color and title.

    Args:
      data:     The dataset to be used for creating the boxplot.
      x_var:    The variable to be plotted on the x-axis of the boxplot.
      y_var:    The variable to be plotted on the y-axis of the boxplot. It is optional and can be left as
                None if only one variable is being plotted.
      color_by: The parameter "color_by" is an optional parameter that allows the user to specify a
                categorical variable to color the boxplots by. If this parameter is not specified, the boxplots will
                not be colored by any variable.
      ax:       The ax parameter is an optional parameter that allows the user to specify the axes on which
                the boxplot will be plotted. If ax is not specified, a new figure and axes will be created.
      title:    The title of the boxplot.

    Returns:
      the axis object (ax) after creating a boxplot using the input data and parameters.
    """
    with plt.rc_context(
        {"axes.labelcolor": "black", "ytick.labelleft": True, "xtick.labelbottom": True}
    ):
        if ax is None:
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)
        sns.boxplot(x=x_var, y=y_var, hue=color_by, data=data, ax=ax)
        ax.set_title(title, fontsize=titlefontsize)
    return ax


def create_swarmplot(
    data,
    x_var,
    y_var=None,
    color_by=None,
    title="",
    titlefontsize=12,
    figsize=(10, 10),
    ax=None,
) -> plt.Axes:
    """
    This function creates a swarmplot using seaborn library with customizable parameters.
    
    Args:
      data: The dataset that contains the variables to be plotted.
      x_var: The variable to be plotted on the x-axis of the swarmplot.
      y_var: The variable to be plotted on the y-axis. It is optional and can be left as None if only
    the x-axis variable is to be plotted.
      color_by: The variable used to color the points in the swarmplot. If not specified, all points
    will have the same color.
      title: The title of the plot.
      titlefontsize: The font size of the title of the plot. Defaults to 12
      figsize: The size of the figure in inches (width, height).
      ax: The ax parameter is an optional parameter that allows the user to specify the matplotlib Axes
    object on which the swarmplot will be drawn. If ax is not provided, a new figure and Axes object
    will be created.
    
    Returns:
      a matplotlib Axes object.
    """
    with plt.rc_context(
        {"axes.labelcolor": "black", "ytick.labelleft": True, "xtick.labelbottom": True}
    ):
        if ax is None:
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)
        with warnings.catch_warnings(record=True):
            sns.swarmplot(
                x=x_var,
                y=y_var,
                hue=color_by,
                dodge=True,
                data=data,
                alpha=0.8,
                s=4,
                ax=ax,
            )
        ax.set_title(title, fontsize=titlefontsize)
    return ax


def create_histogram(
    data,
    var,
    color_by=None,
    bins=10,
    max_categories=50,
    title="",
    titlefontsize=12,
    figsize=(10, 10),
    ax=None,
) -> plt.Axes:
    """
    The function creates a histogram plot of a given variable in a dataset, with options for
    color-coding and binning.
    
    Args:
      data: The input data for creating the histogram.
      var: The variable/column name from the input data that will be used to create the histogram.
      color_by: The variable to use for coloring the histogram bars or stacking them. If None or the
    same as the variable being plotted, the bars will not be colored or stacked.
      bins: The number of bins to use for the histogram. Defaults to 10
      max_categories: The maximum number of categories allowed in the histogram. If the number of
    categories exceeds this value, an option to replace the longtail into "OTHER" is created. Defaults
    to 50
      title: The title of the histogram plot.
      titlefontsize: The font size of the title of the histogram. Defaults to 12
      figsize: The size of the figure in inches (width, height).
      ax: The matplotlib Axes object to plot the histogram on. If None, a new figure and Axes object
    will be created.
    
    Returns:
      a matplotlib Axes object.
    """
    with plt.rc_context(
        {"axes.labelcolor": "black", "ytick.labelleft": True, "xtick.labelbottom": True}
    ):
        if ax is None:
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)

        if is_numeric_dtype(data[var]):
            if (color_by is None) | (color_by == var):
                plotdata = data[var]
                stacked = False
            else:
                plotdata = [
                    data[data[color_by] == x][var] for x in data[color_by].unique()
                ]
                stacked = True
            ax.hist(plotdata, bins=bins, stacked=stacked)
        else:
            nr_cats = data[var].nunique()
            if nr_cats > max_categories:
                pass
                # create an option here later on, by replacing the longtail into OTHER
            if (color_by is None) | (color_by == var):
                plotdata = (
                    data[var].value_counts(dropna=False).sort_index(ascending=True)
                )
                ax.bar(
                    x=plotdata.index.astype("str"),
                    height=plotdata,
                )
                highest_value = max(plotdata)
            else:
                plotdata = (
                    data.groupby([color_by, var])
                    .size()
                    .unstack(fill_value=0)
                    .transpose()
                )
                for ind, col in enumerate(plotdata.columns):
                    if ind == 0:
                        ax.bar(
                            x=plotdata[col].index.astype("str"), height=plotdata[col]
                        )
                        barheight = plotdata[col]
                    else:
                        ax.bar(
                            x=plotdata[col].index.astype("str"),
                            height=plotdata[col],
                            bottom=barheight,
                        )
                    barheight.add(plotdata[col], fill_value=0)
                highest_value = plotdata.sum(axis=1).max()
            ax.set_ylim([None, highest_value * 1.25])
            ax.tick_params(axis="x", labelrotation=45)
        ax.set_title(title, fontsize=titlefontsize)
        return ax


def create_confusion_matrix_heatmap(
    conf_matrix, model_accuracy=None, figsize=(10, 10), ax=None
) -> plt.Axes:
    """
    This function creates a heatmap of a confusion matrix with optional model accuracy score.
    
    Args:
      conf_matrix: The confusion matrix to be visualized as a heatmap.
      model_accuracy: The accuracy score of the model, expressed as a percentage. It is an optional
    parameter that can be used to add a title to the heatmap.
      figsize: The size of the figure in inches (width, height).
      ax: An optional parameter that specifies the matplotlib Axes object to plot the heatmap on. If not
    provided, a new figure and Axes object will be created.
    
    Returns:
      a matplotlib Axes object.
    """
    if ax is None:
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
    sns.heatmap(
        conf_matrix,
        annot=True,
        fmt=".0f",
        linewidths=0.5,
        square=True,
        cmap="Blues_r",
        ax=ax,
    )
    plt.ylabel("Actual label")
    plt.xlabel("Predicted label")
    if model_accuracy is not None:
        all_sample_title = "Accuracy Score: {0} %".format(
            round(model_accuracy * 100, 2)
        )
        plt.title(all_sample_title, size=15)
    return ax


def create_tableplot(data, colLabels=None, figsize=(10, 10), ax=None) -> plt.Axes:
    """
    The function creates a table plot using the given data and column labels.
    
    Args:
      data: a pandas DataFrame containing the data to be plotted in the table
      colLabels: A list of column labels for the tableplot. If not provided, the column labels will be
    the column names of the input data.
      figsize: The size of the figure in inches (width, height).
      ax: An optional parameter that specifies the matplotlib Axes object to plot the table on. If it is
    not provided, a new figure and Axes object will be created.
    
    Returns:
      a matplotlib Axes object.
    """
    if ax is None:
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
    if colLabels is None:
        colLabels = data.columns
    tableplot = ax.table(cellText=data.values, colLabels=colLabels, loc="center")
    tableplot.scale(1, 2)
    ax.axis("off")
    return ax


def create_single_tableplot(data, colLabels=None):
    """
    The function creates a table plot with given data and column labels.
    
    Args:
      data: a pandas DataFrame containing the data to be plotted in a table format
      colLabels: A list of column labels for the table. If not provided, the column labels will be the
    column names of the input data.
    
    Returns:
      a matplotlib figure object.
    """
    if colLabels is None:
        colLabels = data.columns
    if len(data) + 1 > len(colLabels):
        nrows, ncols = len(data) + 1, len(colLabels)
    else:
        ncols, nrows = len(data) + 1, len(colLabels)
    fig = plt.figure(figsize=(ncols, nrows))
    ax = fig.add_subplot(111)
    ax.axis("off")
    tableplot = ax.table(cellText=data.values, colLabels=colLabels, loc="center")
    tableplot.set_fontsize(14)
    tableplot.scale(2, 2)
    return fig


def create_pairplot(data, figtitle=""):
    """
    This function creates a pairplot using seaborn library with customized settings and a given title.
    
    Args:
      data: The data to be plotted in the pairplot.
      figtitle: The title of the figure. It is an optional parameter and if not provided, the figure
    will not have a title.
    
    Returns:
      a matplotlib figure object.
    """
    with plt.rc_context(
        {
            "axes.labelcolor": "black",
            "ytick.labelleft": True,
            "xtick.labelbottom": True,
            "axes.linewidth": 1.0,
        }
    ):
        fig_pairplot = sns.pairplot(
            data,
            corner=True,
            plot_kws=dict(color="#003D7C"),
            diag_kws={"color": "#003D7C"},
        )
        fig = fig_pairplot.fig
        fig.suptitle(figtitle, fontsize=12, y=1.0)
        return fig


def create_barplot(
    data,
    x_var,
    y_var,
    add_value_labels=True,
    x_label="",
    title="",
    figsize=(10, 10),
    ax=None,
) -> plt.Axes:
    """
    The function creates a bar plot with optional value labels and customizable labels and title.
    
    Args:
      data: The data to be plotted in the barplot.
      x_var: The variable to be plotted on the x-axis of the barplot.
      y_var: The variable used for the height of the bars in the barplot.
      add_value_labels: A boolean parameter that determines whether or not to add labels to the top of
    each bar in the barplot indicating the height of the bar. Defaults to True
      x_label: The label for the x-axis of the barplot.
      title: The title of the barplot.
      figsize: The size of the figure (width, height) in inches.
      ax: The ax parameter is an optional parameter that allows the user to pass in an existing
    matplotlib Axes object to plot on. If this parameter is not provided, a new figure and Axes object
    will be created.
    
    Returns:
      a matplotlib Axes object.
    """
    with plt.rc_context(
        {"axes.labelcolor": "black", "ytick.labelleft": True, "xtick.labelbottom": True}
    ):
        if ax is None:
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)
        barplot = ax.bar(x=data[x_var], height=data[y_var], align="center")
        _ = ax.set_xlabel(x_label)
        _ = ax.set_xticks(
            ax.get_xticks(), ax.get_xticklabels(), rotation=45, ha="right"
        )
        _ = ax.set_title(title)
        if add_value_labels:
            for p in barplot:
                height = p.get_height()
                ax.annotate(
                    "{}".format(height),
                    xy=(p.get_x() + p.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                )
        return ax


def create_stacked_barplot(
    data, x_var, y_var, color_by, x_label="", title="", figsize=(10, 10), ax=None
) -> plt.Axes:
    """
    This function creates a stacked barplot with multiple categories and colors based on a given
    dataset.
    
    Args:
      data: The input data for the plot.
      x_var: The variable to be plotted on the x-axis.
      y_var: The variable to be plotted on the y-axis of the stacked barplot.
      color_by: The variable used to determine the color of the bars in the stacked barplot.
      x_label: The label for the x-axis of the plot.
      title: The title of the stacked barplot.
      figsize: The size of the figure (width, height) in inches.
      ax: The ax parameter is an optional parameter that allows the user to specify the matplotlib Axes
    object on which to draw the plot. If it is not specified, a new Axes object will be created.
    
    Returns:
      a matplotlib Axes object.
    """
    categories = data[color_by].unique()
    init_data = pd.DataFrame(data[x_var].unique(), columns=[x_var]).sort_values(
        by=x_var
    )
    init_data[y_var] = 0
    bottom = np.zeros(init_data.shape[0])

    with plt.rc_context(
        {"axes.labelcolor": "black", "ytick.labelleft": True, "xtick.labelbottom": True}
    ):
        if ax is None:
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)

        _ = ax.bar(
            x=init_data[x_var],
            height=init_data[y_var],
            bottom=bottom,
            label=None,
            align="center",
        )

        for cat in categories:
            data_cat = (
                init_data[[x_var]]
                .merge(data[data[color_by] == cat], on=x_var, how="left")
                .fillna(0)
            )
            _ = ax.bar(
                x=data_cat[x_var],
                height=data_cat[y_var],
                label=cat,
                bottom=bottom,
                align="center",
            )
            bottom += data_cat[y_var]
        _ = ax.set_xlabel(x_label)
        _ = ax.set_xticks(
            ax.get_xticks(), ax.get_xticklabels(), rotation=45, ha="right"
        )
        _ = ax.set_title(title)
        _ = ax.legend(loc="upper right", ncol=len(categories))
        return ax


def create_lineplot(
    data, x_var, y_var, color_by=None, x_label="", title="", figsize=(10, 10), ax=None
) -> plt.Axes:
    """
    This function creates a line plot with optional color grouping based on a specified data set and
    variables.
    
    Args:
      data: The data to be plotted in the line plot.
      x_var: The variable to be plotted on the x-axis of the line plot.
      y_var: The variable to be plotted on the y-axis of the line plot.
      color_by: The variable used to color the lines in the line plot. If this parameter is not
    specified, all lines will have the same color.
      x_label: The label for the x-axis of the line plot.
      title: The title of the line plot.
      figsize: The size of the figure in inches (width, height).
      ax: The ax parameter is an optional parameter that allows the user to pass in an existing
    matplotlib Axes object to plot the lineplot on. If ax is not provided, a new figure and Axes object
    will be created.
    
    Returns:
      a matplotlib Axes object.
    """
    categories = data[color_by].unique()

    with plt.rc_context(
        {"axes.labelcolor": "black", "ytick.labelleft": True, "xtick.labelbottom": True}
    ):
        if ax is None:
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)

        for cat in categories:
            data_cat = data[data[color_by] == cat].sort_values(x_var)
            _ = ax.plot(data_cat[x_var], data_cat[y_var], label=cat, linewidth=1)
        _ = ax.set_xlabel(x_label)
        _ = ax.set_xticks(
            ax.get_xticks(), ax.get_xticklabels(), rotation=45, ha="right"
        )
        _ = ax.set_title(title)
        _ = ax.legend(loc="upper right", ncol=len(categories))
        return ax
