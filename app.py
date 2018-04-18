import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_table_experiments as dt
import plotly 
from flask import Flask

plotly.tools.set_credentials_file(username='erikscalfaro', api_key='p4kq3JiCPXMHZ9yfA45y')

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

app.scripts.config.serve_locally=True


# Dataframe filtered with days >-20 
df= pd.read_csv('LiftOFFV2.csv')
del df['Unnamed: 0']
del df['F-Type']

############ Kap-20 not working to create 6 dayaframes
kap=pd.read_csv('KaplanSJSCases.csv')

df2 = df[df.CaseName == 'C001']
df3 = df[df.CaseName == 'C002']
df4 = df[df.CaseName == 'C003']
df5 = df[df.CaseName == 'C004']
df6 = df[df.CaseName == 'C005']
df7 = df[df.CaseName == 'C006']


sorted(df.columns)

def get_data_object(case_selection):
    """
    For case selections, return the relevant in-memory data frame.
    """
    return df[df.CaseName == case_selection]

BACKGROUND =  'rgb(230, 230, 230)'

COLORSCALE = [ [0, "rgb(244,236,21)"], [0.3, "rgb(249,210,41)"], [0.4, "rgb(134,191,118)"],
                [0.5, "rgb(37,180,167)"], [0.65, "rgb(17,123,215)"], [1, "rgb(54,50,153)"] ]

def scatter_plot01(   
        markers = [],
        plot_type = 'scatter',
        x=df2['DaysToEvent'],
        y=df2['F-Count'],
        size = df2['F-Weight'],
        color = df2['F-Weight'],
        xlabel = 'Days Before Event identification',
        ylabel = 'Feature count in previous cases'):
    
    def axis_template_2d(title):
        return dict(
            xgap = 10, ygap = 10,
            backgroundcolor = BACKGROUND,
            gridcolor = 'rgb(255, 255, 255)',
            title = title,
            zerolinecolor = 'rgb(255, 255, 255)',
            color = '#444'
            ) 
    
    data = [ dict(
        x = x,
        y = y,
        mode = 'markers',
        marker = dict(
                colorscale = COLORSCALE,
                colorbar = dict( title = "Feature<br>Weight" ),
                line = dict( color = '#444' ),
                reversescale = True,
                sizeref = 0.005,
                sizemode = 'diameter',
                opacity = 0.6,
                size = size,
                color = color,
            ),
        text = df2['FeatureName'],
        type = plot_type,
        ) ]
            
            
    layout = dict(
        font = dict( family = 'Raleway', size = 17 ),
        title = 'Case Features',
        hovermode = 'closest',
        margin = dict( r=110, t=50, l=57, b=60),
        showlegend = False,
        scene = dict(
            xaxis = axis_template_2d( xlabel ),
            yaxis = axis_template_2d( ylabel )
            )
        )

        
    if plot_type in ['scatter']:
        layout['xaxis'] = axis_template_2d(xlabel)
        layout['yaxis'] = axis_template_2d(ylabel)
        layout['plot_bgcolor'] = BACKGROUND
        layout['paper_bgcolor'] = BACKGROUND
        del layout['scene']
        
  
    #asd = dict(data = data, layout = layout)
    #print(asd['data'])
    return dict(data = data, layout = layout ) 


app.layout = html.Div([
    # Row 1: Header and Intro text
    
    html.Div([
        html.Img(src="https://photos.smugmug.com/My-First-Gallery/i-Q7PH3TS/0/fc7fa527/X2/Medic-Alert-X2.jpg",
                style={
                    'height': '100px',
                    'float': 'right',
                    'position': 'relative',
                    'bottom': '2px',
                    'left': '2px'
                },
                ),
          html.H2('SEPTA',
                style={
                    'position': 'relative',
                    'top': '0px',
                    'left': '27px',
                    'font-family': 'Dosis',
                    'display': 'inline',
                    'font-size': '5.0rem',
                    'color': '#4D637F'
                }),    
        html.H2('-',
                style={
                    'position': 'relative',
                    'top': '0px',
                    'left': '27px',
                    'font-family': 'Dosis',
                    'display': 'inline',
                    'font-size': '4.5rem',
                    'color': '#4D637F'
                }),
      
        html.H2('Side Effect Predictive Timely Analysis',
                style={
                    'position': 'relative',
                    'top': '0px',
                    'left': '27px',
                    'font-family': 'Dosis',
                    'display': 'inline',
                    'font-size': '4.5rem',
                    'color': '#4D637F'
                }),
    ], className='row twelve columns', style={'position': 'relative', 'right': '15px'}),

    html.Div([
        html.Div([
            html.Div([
                html.Br(),
                 html.H2('CLICK a feature in the bottom graph to highlight it in the table - ',
                style={
                    'position': 'relative',
                    'top': '0px',
                    'right': '0px',
                    'font-family': 'Dosis',
                    'display': 'inline',
                    'font-size': '1.5rem',
                    'color': '#0361a0',
                    'float':'left'},
                        ),
            ], style={'margin-left': '10px'}),
            ], className='twelve columns' )
          
    ], className='row' ),
            
            
            
    
    
    ##### Prediction Model Information: 
    html.Div([
            html.H2('- HOVER over points to see exact values',
                style={
                    'position': 'relative',
                    'top': '0px',
                    'right': '0px',
                    'font-family': 'Dosis',
                    'display': 'inline',
                    'font-size': '1.5rem',
                    'color': '#0361a0',
                    'float':'left'},
                        ),
            html.H2('WARNING Algorithm Identified Steven Johnson Syndrome',
                style={
                    'position': 'relative',
                    'top': '0px',
                    'right': '80px',
                    'font-family': 'Dosis',
                    'display': 'inline',
                    'font-size': '2.0rem',
                    'color': '#c11a03',
                    'float':'right'},
                        ),
                                  
        ]),
       
        

    html.Div([
         html.Div([
        dcc.Dropdown(
            id='drop',
            options=[
                    {'label': 'Patient Case 02', 'value': 'C002'},
                    {'label': 'Patient Case 03', 'value': 'C003'},
                    {'label': 'Patient Case 04', 'value': 'C004'},
                    {'label': 'Patient Case 05', 'value': 'C005'},
                    {'label': 'Patient Case 06', 'value': 'C006'}
                    ],
            value='C002'
            ),
            ]),

    html.Div([
            
        html.Br(),
        
        dt.DataTable(
        # Initialise the rows
            rows=df.to_dict('records'),
            columns=df.columns,
            row_selectable=True,
            filterable=True,
            sortable=False,
            min_height = 1000,
            min_width = 1000,
            selected_row_indices=[],
            id='table'
            ),
        ],style={'width': '50%', 'float': 'right', 'display': 'inline-block',}),

    html.Div([ 
        dcc.Graph(id='survival-graph')
         ]),

    html.Div([
    html.Div([
        

        dcc.Graph(id='feature-graph',
                    style=dict(width='965px', height = '430px'),
                    hoverData=dict( points=[dict(pointNumber=0)]),
                    clickData={'points': [{"text": "Fenetylline"}]},
                    figure=scatter_plot01()) 
            ],style={'width': '50%', 'float': 'left', 'display': 'inline'})
        
                ])])
])

@app.callback(
    Output('table', 'selected_row_indices'),
    [Input('feature-graph', 'clickData')],
    [State('table','selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    print('FINALLY')
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices


@app.callback(
    Output('table', 'rows'),
    [Input('drop', 'value')])
def update_table(case_selection):
    """
    For case selection, return the relevant table
    """
    df = get_data_object(case_selection)
    return df.to_dict('records')

@app.callback(
        Output('survival-graph', 'figure'),
        [Input('drop','value')])
def survival_graph (identifier):
    dff = kap.filter(items=['Days', identifier])
    traces = []
    for i in dff:
        traces.append(go.Scatter(
                    x=dff['Days'],
                    y=dff[identifier],
                    mode='lines+markers',
                    opacity=0.8,
                    marker={
                        'opacity': 0.9,
                        'size': 10,
                        'line': {'width': 0.5, 'color': 'white'},
                        'symbol': 'circle-open'
                    },
                    name = i,
                    showlegend = False,
                    connectgaps = True,
                    hoverinfo = 'y',
                    line = {
                            'shape': "spline", 
                            'width': 1.5
                            }, 
                ),)
    return {
        'data': traces,
        'layout':  go.Layout(
                xaxis={'title': 'Days Before Event Identification', 
                       'autorange': True,
                       'fixedrange': True, 
                       'range': [-15.9355677692, 0.935567769163], 
                       'showspikes': False,
                       'type': "linear"
                       },
                yaxis={'title': '1-Probability of Event in Time', 
                        'autorange': True, 
                        'fixedrange': True, 
                        'range': [-0.0598992197659, 0.934899219766], 
                        'showspikes': False,
                        'type': "linear"
                           },
                hovermode='closest',
                legend={
                        "x": 0.02, 
                        "y": 1, 
                        "font": {"size": 11}
                        }, 
                margin= {
                            "r": 45, 
                            "t": 50, 
                            "b": 50, 
                            "l": 45, 
                            "pad": 0
                        }, 
                        
                paper_bgcolor = "rgb(255, 255, 255)", 
                plot_bgcolor = "rgb(244, 235, 235)", 
                showlegend = True, 
                title= "<b>Steven Johnson Syndrome Case Analysis</b>", 
                titlefont= {"size": 20, "family" : 'Raleway'}, 
                width= 900, 
                autosize= False, 
                font = {"size": 17, "family" : 'Raleway'},
                height= 500
            )
        }

@app.callback(
    Output('feature-graph', 'figure'),
    [Input('drop', 'value')])
def featuresgrapher(drop_value):
    if drop_value == 'C002':
        return scatter_plot01(drop_value)
 

if __name__ == '__main__':
    app.run_server(debug=True)
    