# Cmotions Dataviz

cmo_dataviz is a Python library created by [The Analytics Lab](https://www.theanalyticslab.nl/), which is powered by [Cmotions](https://cmotions.nl/). This library makes it easy for us to create graphs in our prefered styling and using Cmotions colors by default. Nothing fancy, but very useful for our consultants. Mostly since this package is used in other packages, which makes our workflow simpler and more efficient.

Since we love to share what we do, why not also do that with our packages, that is why we've decided to make (almost) all of our packages open source, this way we hope to give back to the community that brings us so much. Enjoy!

## Installation
Install cmo_dataviz using pip
```bash
pip install cmo-dataviz
```

If you want to be able to use the tutorial notebook or the code below, you also need to install pydataset using pip
```bash
pip install pydataset
```

## Usage
```python
from pydataset import data
import cmo_dataviz as dv
import matplotlib.pyplot as plt

# import your own stylesheet if relevant
dv.import_style('mydocuments/mystylesheet.mplstyle')

df = data("iris")
df_summary = df.groupby('Species').agg({'Sepal.Length': 'mean','Sepal.Width': 'sum', 'Petal.Length': 'mean', 'Petal.Width': 'sum'}).reset_index()

# create a single plot with default settings for size and so on
dv.create_horizontal_barplot(data=df_summary, x_var='Sepal.Width', y_var='Species', x_label="", title="", ax=None)
plt.show()

# adjust the size (or other settings) of the plot
fig, ax = plt.subplots(figsize=(5,5))
dv.create_horizontal_barplot(data=df_summary, x_var='Sepal.Width', y_var='Species', x_label="", title="", ax=ax)
plt.show()

# combine multiple graphs in a single plot
fig, ax = plt.subplots(2, 2, figsize=(10,7))
dv.create_histogram(data=df, var="Petal.Width", color_by="Species", bins=10, max_categories=50, ax=ax[0,0], title="our histogram")
dv.create_scatterplot(data=df, x_var="Sepal.Width", y_var="Sepal.Length", title="our scatterplot", ax=ax[0,1])
dv.create_boxplot(data=df, x_var="Petal.Length", y_var="Species", color_by=None, ax=ax[1,0], title="our boxplot")
dv.create_swarmplot(data=df, x_var="Sepal.Width", y_var=None, color_by= "Species", ax=ax[1,1])
plt.show()
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)

## Contributors
Jeanine Schoonemann<br>
[Contact us](mailto:info@theanalyticslab.nl)