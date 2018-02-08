import json
import requests
from datetime import datetime

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter, DatetimeTickFormatter
from bokeh.models.widgets import Panel, Tabs
from bokeh.tile_providers import CARTODBPOSITRON
from bokeh.palettes import Viridis6 as palette

#globals
global_settings = {
    'tools': 'wheel_zoom, reset, save',
}

def bar_chart():
    r = requests.get('https://raw.githubusercontent.com/FreeCodeCamp/ProjectReferenceData/master/GDP-data.json')
    data = json.loads(r.text)

    chart_data = {
        'date': [datetime.strptime(a[0], '%Y-%m-%d') for a in data['data']],
        'gdp': [a[1] for a in data['data']],
    }

    source = ColumnDataSource(chart_data)
    hover = HoverTool(
        tooltips=[
            ('GDP', '@gdp{$0,0.00}'),
            ('Date', '@date{%Y - %B}'),
        ],
        formatters={
            'date' : 'datetime',
        }
    )

    bar = figure(x_axis_type='datetime',
                 plot_height=750,
                 plot_width=1000,
                 tools='wheel_zoom, reset, save',
                 title=data['source_name'])
    bar.vbar(x='date', top='gdp', width=0.9, source=source)
    bar.add_tools(hover)

    #visual settings

    # bar.xaxis.formatter = DatetimeTickFormatter(milliseconds = ['%Y'])
    bar.xaxis.major_label_orientation = 'vertical'
    bar.xaxis.minor_tick_line_color = None
    bar.xgrid.grid_line_color = None

    bar.yaxis.formatter = NumeralTickFormatter(format='$0,0.00')
    bar.ygrid.grid_line_color = None

    return bar

def scatterplot():
    r = requests.get('https://raw.githubusercontent.com/FreeCodeCamp/ProjectReferenceData/master/cyclist-data.json')
    data = json.loads(r.text)

    chart_data = {
        'place': [a['Place'] for a in data],
        'time': [a['Seconds'] * 1000 for a in data],
        'name': [a['Name'] for a in data],
        'year': [a['Year'] for a in data],
        'nationality': [a['Nationality'] for a in data],
        'charges': [a['Doping'] for a in data],
    }
    source = ColumnDataSource(chart_data)
    hover = HoverTool(
        tooltips=[
            ('Name', '@name'),
            ('Year', '@year'),
            ('Nationality', '@nationality'),
            ('Charges', '@charges'),
            ('Time', '@time{%M:%S}')
        ],
        formatters = {
            'time': 'datetime',
        }
    )

    p = figure(tools=global_settings['tools'],
               x_axis_type="datetime",
               plot_height=750,
               plot_width=1000,
               title="Doping in Professional Bicycle Racing")
    p.add_tools(hover)

    p.xaxis.axis_label = "Time Up Alpe d'Huez"
    p.yaxis.axis_label = "Ranking"

    p.square('time', 'place', size=20, source=source, color='red', alpha=0.5)
    p.xaxis.formatter = DatetimeTickFormatter(milliseconds = ['%M:%S'])

    return p

def heat_map():
    r = requests.get('https://raw.githubusercontent.com/FreeCodeCamp/ProjectReferenceData/master/global-temperature.json')
    data = json.loads(r.text)

    chart_data = {
        'year': [a['monthlyVariance']['year'] for a in data],
        'month': [a['monthlyVariance']['month'] for a in data],
        'variance': [a['monthlyVariance']['variance'] for a in data],
    }

    colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
    mapper = LinearColorMapper(palette=colors, low=df.rate.min(), high=df.rate.max())

    source = ColumnDataSource(chart_data)
    bound = 20000000  # meters
    p = figure(title="Visualize Data with a Heat Map",
               x_range=years, y_range=months,
               x_axis_location="above", plot_width=1000, plot_height=750,
               tools=global_settings['tools'], toolbar_location='below')
    p.rect(x="Year", y="Month", width=1, height=1,
           source=source,
           fill_color={'field': 'rate', 'transform': mapper},
           line_color=None)

    p.axis.visible = False

    #map background
    p.add_tile(CARTODBPOSITRON)

    return p

def world_map():
    r = requests.get('https://raw.githubusercontent.com/FreeCodeCamp/ProjectReferenceData/master/meteorite-strike-data.json')
    data = json.loads(r.text)
    a = 0

    chart_data = {
        'x-coords': [a['geometry']['coordinates'][0] for a in data['features']],
        'y-coords': [a['geometry']['coordinates'][1] for a in data['features']],
        'name': [a['properties']['name'] for a in data['features']],
        'year': [a['properties']['year'] for a in data['features']],
        'mass': [a['properties']['mass'] for a in data['features']],
    }

    source = ColumnDataSource(chart_data)
    bound = 20000000  # meters
    p = figure(tools=global_settings['tools'], x_range=(-bound, bound), y_range=(-bound, bound), plot_height=750,
               plot_width=1000)
    p.square('x-coords', 'y-coords', size=20, source=source, color='red', alpha=0.5)

    p.axis.visible = False

    #map background
    p.add_tile(CARTODBPOSITRON)

    return p

def display_plots():
    page1 = Panel(child=bar_chart(), title='FCC Bar Chart')
    page2 = Panel(child=scatterplot(), title='FCC Scatterplot Graph')
    # page4 = Panel(child=world_map(), title='FCC Map Data Across the Globe')

    show(Tabs(tabs=[page1, page2, page3]))

if __name__ == "__main__":
    display_plots()


