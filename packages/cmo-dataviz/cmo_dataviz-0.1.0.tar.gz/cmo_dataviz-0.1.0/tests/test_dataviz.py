import pytest
from pydataset import data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cmo_dataviz as dv

df = data("iris")
df_summary = (
    df.groupby("Species")
    .agg(
        {
            "Sepal.Length": "mean",
            "Sepal.Width": "sum",
            "Petal.Length": "mean",
            "Petal.Width": "sum",
        }
    )
    .reset_index()
)

# import_style


@pytest.mark.mpl_image_compare
def test_create_horizontal_barplot():
    fig, ax = plt.subplots()
    dv.create_horizontal_barplot(
        data=df_summary,
        x_var="Sepal.Width",
        y_var="Species",
        x_label="",
        title="",
        ax=ax,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_create_scatterplot():
    fig, ax = plt.subplots()
    dv.create_scatterplot(
        data=df, x_var="Sepal.Width", y_var="Sepal.Length", title="", ax=ax
    )
    return fig


@pytest.mark.mpl_image_compare
def test_create_heatmap():
    fig, ax = plt.subplots()
    dv.create_heatmap(
        data=df.select_dtypes(include=np.number).corr(),
        complete=True,
        figsize=(10, 10),
        title="",
        ax=ax,
    )
    return fig


# make_barplot_labels()

# make_boxplot_labels()


@pytest.mark.mpl_image_compare
def test_create_boxplot():
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 10))
    dv.create_boxplot(
        data=df, x_var="Petal.Length", y_var="Species", color_by=None, ax=ax, title=""
    )
    return fig


@pytest.mark.mpl_image_compare
def test_create_swarmplot():
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 10))
    dv.create_swarmplot(
        data=df, x_var="Sepal.Width", y_var=None, color_by="Species", ax=ax
    )
    return fig


@pytest.mark.mpl_image_compare
def test_create_histogram():
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 10))
    dv.create_histogram(
        data=df,
        var="Petal.Width",
        color_by="Species",
        bins=10,
        max_categories=50,
        ax=ax,
        title="",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_create_confusion_matrix_heatmap():
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 10))
    dv.create_confusion_matrix_heatmap(
        conf_matrix=df[["Sepal.Width", "Sepal.Length"]]
        .select_dtypes(include=np.number)
        .corr(),
        model_accuracy=0.8,
        figsize=(5, 5),
        ax=ax,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_create_tableplot():
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 10))
    dv.create_tableplot(data=df_summary, colLabels=None, ax=ax)
    return fig


@pytest.mark.mpl_image_compare
def test_create_single_tableplot():
    return dv.create_single_tableplot(data=df_summary, colLabels=None)


@pytest.mark.mpl_image_compare
def test_create_pairplot():
    return dv.create_pairplot(data=df, figtitle="")


@pytest.mark.mpl_image_compare
def test_create_barplot():
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 10))
    dv.create_barplot(
        data=df_summary,
        x_var="Species",
        y_var="Sepal.Length",
        add_value_labels=True,
        x_label="",
        title="",
        ax=ax,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_create_stacked_barplot():
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 10))
    dv.create_stacked_barplot(
        data=df_summary,
        x_var="Species",
        y_var="Sepal.Length",
        color_by="Sepal.Width",
        x_label="",
        title="",
        ax=ax,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_create_lineplot():
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 10))
    dv.create_lineplot(
        data=df,
        x_var="Sepal.Width",
        y_var="Sepal.Length",
        color_by="Species",
        x_label="",
        title="",
        ax=ax,
    )
    return fig
