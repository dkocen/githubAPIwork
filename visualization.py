import pandas as pd

from bokeh.layouts import row, column
from bokeh.models import Select
from bokeh.palettes import Spectral5
from bokeh.plotting import curdoc, figure, ColumnDataSource

df = pd.read_csv('data_cleaned200repos_alldata.csv')
del df['Unnamed: 0']
del df['creation_date']

df['repo'] = [repo[0:30] for repo in df['repo']]

SIZES = list(range(6, 22, 3))
COLORS = Spectral5
N_SIZES = len(SIZES)
N_COLORS = len(COLORS)

source = ColumnDataSource(df)

columns = sorted(df.columns)
discrete = ['repo', 'language']
continuous = ['sentiment', 'subscribers', 'stars']

def create_figure():
    xs = df[x.value].values
    ys = df[y.value].values
    x_title = x.value.title()
    y_title = y.value.title()

    kw = dict()
    if x.value in discrete:
        kw['x_range'] = sorted(set(xs))
    if y.value in discrete:
        kw['y_range'] = sorted(set(ys))
    kw['title'] = "%s vs %s" % (x_title, y_title)

    tooltips = [
        ("Repo", "@repo"),
        (x_title, "$x{0,0.00}"),
        (y_title, "$y{0,0.00}")
    ]

    p = figure(plot_height=1000, plot_width=1000, tools='pan,box_zoom,hover,reset', tooltips=tooltips, **kw)
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    if x.value in discrete:
        p.xaxis.major_label_orientation = pd.np.pi / 4

    sz = 9
    if size.value != 'None':
        if len(set(df[size.value])) > N_SIZES:
            groups = pd.qcut(df[size.value].values, N_SIZES, duplicates='drop')
        else:
            groups = pd.Categorical(df[size.value])
        sz = [SIZES[xx] for xx in groups.codes]

    c = "#31AADE"
    if color.value != 'None':
        if len(set(df[color.value])) > N_COLORS:
            groups = pd.qcut(df[color.value].values, N_COLORS, duplicates='drop')
        else:
            groups = pd.Categorical(df[color.value])
        c = [COLORS[xx] for xx in groups.codes]

    # if x.value in discrete and y.value in continuous:
    #     p.vbar(x=xs, top=ys, width=sz, color=c)
    # elif y.value in discrete and x.value in continuous:
    #     p.hbar(y=ys, right=xs, height=sz, color=c)
    # else:
    p.circle(x=x.value, y=y.value, source=source, color=c, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)

    return p


def update(attr, old, new):
    layout.children[1] = create_figure()


x = Select(title='X-Axis', value='subscribers', options=columns)
x.on_change('value', update)

y = Select(title='Y-Axis', value='sentiment', options=columns)
y.on_change('value', update)

size = Select(title='Size', value='None', options=['None'] + continuous)
size.on_change('value', update)

color = Select(title='Color', value='None', options=['None'] + continuous)
color.on_change('value', update)

controls = column(x, y, color, size, width=200)
layout = row(controls, create_figure())

curdoc().add_root(layout)


