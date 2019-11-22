import pandas as pd

from bokeh.layouts import row, column
from bokeh.models import Select
from bokeh.plotting import curdoc, figure, ColumnDataSource
from bokeh.models import ColorBar, BasicTickFormatter
from bokeh.transform import linear_cmap, factor_cmap
from bokeh.palettes import Magma6, Magma256

df_normal = pd.read_csv('data_cleaned200repos_alldata.csv')
del df_normal['Unnamed: 0']
del df_normal['creation_date']

df_normal['repo'] = [repo[0:30] for repo in df_normal['repo']]

df_languages = df_normal.groupby(['language'], as_index=False).apply(
    lambda x: pd.Series({
        'language': x['language'].iloc[0],
        'comment count': x['comment count'].sum(),
        'mean sentiment': x['mean sentiment'].mean(),
        'stars': x['stars'].sum(),
        'subscribers': x['subscribers'].sum()
    })
)

SIZES = list(range(6, 22, 3))
N_SIZES = len(SIZES)

source_normal = ColumnDataSource(df_normal)
source_language = ColumnDataSource(df_languages)

columns = ['comment count', 'language', 'mean sentiment', 'stars', 'subscribers']
color_size_options = ['mean sentiment', 'subscribers', 'stars', 'comment count']

def create_figure():
    if x.value == 'language' or y.value == 'language':
        source = source_language
        df = df_languages

        if x.value == y.value:
            tooltips = [("language", "@language")]
        elif x.value == 'language':
            tooltips = [("language", "@language"),
                        (y.value, f'@{{{y.value}}}{{0.00}}')]
        else:
            tooltips = [("language", "@language"),
                        (x.value, f'@{{{x.value}}}{{0.00}}')]
    else:
        source = source_normal
        df = df_normal
        tooltips = [("repo", "@repo"),
                    (x.value, f'@{{{x.value}}}{{0.00}}'),
                    (y.value, f'@{{{y.value}}}{{0.00}}')]

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

    p = figure(plot_height=1000, plot_width=1000, tools='pan,box_zoom,hover,reset', tooltips=tooltips, **kw)
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    c = "#31AADE"
    if color.value == 'language':
        c = factor_cmap('language', palette=Magma6, factors=df.language.unique())
        if color.value != x.value and color.value != y.value:
            tooltips.append((color.value, '@language'))
    elif color.value != 'None':
        c = linear_cmap(field_name=color.value, palette=Magma256, low=min(df[color.value]), high=max(df[color.value]))
        formatter = BasicTickFormatter(use_scientific=False)
        color_bar = ColorBar(color_mapper=c['transform'], title=color.value,  width=8, location=(0, 0), formatter=formatter)
        p.add_layout(color_bar, 'right')
        if color.value != x.value and color.value != y.value:
            tooltips.append((color.value, f'@{{{color.value}}}{{0.00}}'))

    sz = 9
    if size.value != 'None':
        if len(set(df[size.value])) > N_SIZES:
            groups = pd.qcut(df[size.value].values, N_SIZES, duplicates='drop')
        else:
            groups = pd.Categorical(df[size.value])
        sz = [SIZES[xx] for xx in groups.codes]
        source.add(sz, name='size')
        sz = 'size'
        if size.value != x.value and size.value != y.value:
            tooltips.append((size.value, f'@{{{size.value}}}{{0.00}}'))

    if color.value == 'language':
        p.circle(x=x.value, y=y.value, source=source, color=c, size=sz, legend_field='language', line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)
    else:
        p.circle(x=x.value, y=y.value, source=source, color=c, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)


    return p


def update(attr, old, new):
    layout.children[1] = create_figure()


x = Select(title='X-Axis', value='subscribers', options=columns)
x.on_change('value', update)

y = Select(title='Y-Axis', value='mean sentiment', options=columns)
y.on_change('value', update)

size = Select(title='Size', value='None', options=['None'] + sorted(color_size_options))
size.on_change('value', update)

color = Select(title='Color', value='language', options=['None'] + sorted(['language'] + color_size_options))
color.on_change('value', update)

controls = column(x, y, color, size, width=200)
layout = row(controls, create_figure())

curdoc().add_root(layout)


