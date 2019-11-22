import pandas as pd

from bokeh.layouts import row, column
from bokeh.models import Select
from bokeh.plotting import curdoc, figure, ColumnDataSource
from bokeh.models import ColorBar
from bokeh.transform import linear_cmap, factor_cmap
from bokeh.palettes import Magma6, Magma256

df = pd.read_csv('data_cleaned200repos_alldata.csv')
del df['Unnamed: 0']
del df['creation_date']

df['repo'] = [repo[0:30] for repo in df['repo']]

SIZES = list(range(6, 22, 3))
N_SIZES = len(SIZES)

source = ColumnDataSource(df)

columns = ['comment_count', 'language', 'sentiment', 'stars', 'subscribers']
color_size_options = ['sentiment', 'subscribers', 'stars', 'comment_count']

def create_figure():
    xs = df[x.value].values
    ys = df[y.value].values
    x_title = x.value.title()
    y_title = y.value.title()

    kw = dict()
    if x.value == 'language':
        kw['x_range'] = sorted(set(xs))
    if y.value == 'language':
        kw['y_range'] = sorted(set(ys))
    kw['title'] = f'{x_title} vs {y_title}'

    tooltips = [
        ("Repo", "@repo"),
        (x.value, f'@{x.value}{{0.00}}'),
        (y.value, f'@{y.value}{{0.00}}')
    ]

    p = figure(plot_height=1000, plot_width=1000, tools='pan,box_zoom,hover,reset', tooltips=tooltips, **kw)
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    c = "#31AADE"
    if color.value == 'language':
        mapper = factor_cmap('language', palette=Magma6, factors=df.language.unique())
        tooltips.append((color.value, '@language'))
    elif color.value != 'None':
        mapper = linear_cmap(field_name=color.value, palette=Magma256, low=min(df[color.value]), high=max(df[color.value]))
        color_bar = ColorBar(color_mapper=mapper['transform'], title=color.value, width=8, location=(0, 0))
        p.add_layout(color_bar, 'right')
        tooltips.append((color.value, f'@{color.value}{{0.00}}'))
    else:
        mapper = c

    sz = 9
    if size.value != 'None':
        if len(set(df[size.value])) > N_SIZES:
            groups = pd.qcut(df[size.value].values, N_SIZES, duplicates='drop')
        else:
            groups = pd.Categorical(df[size.value])
        sz = [SIZES[xx] for xx in groups.codes]
        source.add(sz, name='size')
        sz = 'size'
        tooltips.append((size.value, f'@{size.value}{{0.00}}'))

    # if x.value in discrete and y.value in continuous:
    #     p.vbar(x=xs, top=ys, width=sz, color=c)
    # elif y.value in discrete and x.value in continuous:
    #     p.hbar(y=ys, right=xs, height=sz, color=c)
    # else:

    if x.value == 'language':
        p.xaxis.major_label_orientation = pd.np.pi / 4


    elif color.value == 'language':
        p.circle(x=x.value, y=y.value, source=source, color=mapper, size=sz, legend_field='language', line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)
    else:
        p.circle(x=x.value, y=y.value, source=source, color=mapper, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)


    return p


def update(attr, old, new):
    layout.children[1] = create_figure()


x = Select(title='X-Axis', value='subscribers', options=columns)
x.on_change('value', update)

y = Select(title='Y-Axis', value='sentiment', options=columns)
y.on_change('value', update)

size = Select(title='Size', value='None', options=['None'] + sorted(color_size_options))
size.on_change('value', update)

color = Select(title='Color', value='language', options=['None'] + sorted(['language'] + color_size_options))
color.on_change('value', update)

controls = column(x, y, color, size, width=200)
layout = row(controls, create_figure())

curdoc().add_root(layout)


