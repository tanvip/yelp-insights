import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import pandas as pd 
import numpy as np
from datetime import datetime
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import *
import dash_auth
import copy
import scipy.linalg as la

mapbox_access_token = 'pk.eyJ1Ijoic3BlbmNlcmxhd3JlbmNlIiwiYSI6ImNqYnhxdjFxdTJyOW8zM21ud3Z6M3EzbHUifQ.fAFNQd2KwHb2NG-cWA04jA'

#app = dash.Dash('auth')
app = dash.Dash()#'auth')
server = app.server
app.title = 'Yelp Insights'
app.config['suppress_callback_exceptions']=True
dma_options_dict = {'miami':[25.7616798,-80.1917902],
						'atlanta':[33.74832,-84.39111],
						'nyc':[40.71455,-74.00714],
						'san-francisco':[37.77713,-122.41964],
						'los-angeles':[34.05349,-118.24532]}

same_session_comp = ["McDonald's",
						"Subway",
						"Wendy's",
						"Chick-fil-A",
						"Domino's Pizza",
						"Five Guys",
						"Burger King",
						"Chipotle",
						"Panera Bread",
						"Pizza Hut"]

same_session_comp.reverse()

same_session_comp_views = [6937,
								9934,
								10459,
								12904,
								15143,
								16156,
								17426,
								20496,
								23235,
								27549]
demand_dropdown_options = [
			            {'label': 'Atlanta', 'value': 'atlanta'},
			            {'label': 'Miami', 'value': 'miami'},
			            {'label': 'New York City', 'value': 'nyc'},
						{'label': 'Los Angeles', 'value': 'los-angeles'}]
compset_dropdown_options = [
			            {'label': 'Atlanta', 'value': 'atlanta'},
			            {'label': 'Miami', 'value': 'miami'},
			            {'label': 'New York City', 'value': 'nyc'},
						{'label': 'Los Angeles', 'value': 'los-angeles'}]
app.layout = html.Div(

	style={'font-family':'Helvetica Neue',
		  'color':'#4D4D4D',
		  'font-size':'18px'},
	children=[ #main div 
	
	html.Div([ #logo div 
		html.Img(id='ib-logo',
	    src='https://preview.ibb.co/bucGBy/Screen_Shot_2018_07_21_at_6_49_56_AM.png',
	    style={'height':'100px',
	    	   'marginBottom': '23px'}),]),
	
	html.Div([
		html.Div([
			html.Div([
				dcc.Tabs(
			        tabs=[
			            {'label': 'Consumer Demand', 'value': 'demand'},
			        	{'label': 'Competitive Set', 'value': 'comp-set'},
			        	{'label': 'Review Insights', 'value': 'reviews'},
			        	{'label': 'Industry Trends', 'value': 'trends'}
			        ],
			        value='demand',
			        id='tabs',
			        style={'marginBottom': '36px'},
			        vertical=True
			    ),
			    html.Div(
			    	id="dropdown-div",
			    	children=[
				    	dcc.Dropdown(
			                id='dropdown',
			                value='atlanta')]),
			    html.Div(id='small-div')
			], className = 'three columns'),		

		html.Div(id='main-div')
		],
		className='row'
	),
    
    html.Div(id='tab-output'),
    
])])

@app.callback(Output('main-div', 'children'),  #main div callback
				[Input('tabs', 'value'),
				Input('dropdown','value')])
def main_div(tab_value, dropdown_value):
	if tab_value == 'demand':

		center_list = dma_options_dict[dropdown_value]
		data = [{'lat': 25.7616798,
		        'lon': -80.1917902,
		        'mode': 'markers',
		        'hoverinfo': 'none',
		        'marker': {
		            'size':12,
		            'color':'#d32323'
		        },
		        'type': 'scattermapbox',
		        'name': 'SEARCH ME'
		    },

		]

		layout = Layout(
		    autosize=True,
		    height=800,
		    #margin=Margin(l=500, r=100, t=100, b=50),
		    mapbox={
		        'accesstoken': mapbox_access_token,
		        'bearing':0,
		        'center': {
		            'lat':center_list[0],
		            'lon':center_list[1] 
		        },
		        'pitch':0,
		        'zoom':12,
		        'style':'light'#mapbox://styles/spencerlawrence/cjd379wln431d2sp3545c1w9u'
		    },
		    title= 'SEARCH',

		)
		   
		figure = dict(data=data, layout=layout) 

		children=[
			html.Div([
				dcc.Graph(id='demand-map',
					figure=figure),
				],
				className = 'nine columns'),

			]

		return children

	elif tab_value == 'comp-set':

		children = [				
				html.Div([
					dcc.Graph(id='same-session-view',
						figure = go.Figure(
								data = [go.Bar(
									x = same_session_comp,
									y = same_session_comp_views,
									name = 'Same Session User Views',
									marker = go.Marker(
										color='rgba(0,104,178,0.54)',
						        		line=dict(
						            		color='rgba(0,104,178,0.81)',
						            		width=2.1),
										)
									)],

						        layout= go.Layout(
						        	height=800,
						            yaxis={
						                'title': 'User Views',
						                'range': [0,(max(same_session_comp_views)*1.05)],
						            	'showline':True,
						        		'showticklabels':True
						            },
						            xaxis={'tickangle':-45},
						            title= 'Same Session User Views',
						            titlefont={
						                'color':'#000000', 
						                'size':14,
						                'family':'Helvetica'},
						            margin=Margin(l=100, r=0, t=54, b=200)
						        	)
							))
					], className = 'nine columns')]

		return children 

@app.callback(Output('dropdown-div', 'style'), # show/hide the dropdown element
			[Input('tabs','value')])
def show_hide_dropdown(value):
	if value == 'demand':
		return {'display': 'block'}
	elif value == 'comp-set':
		return {'display': 'block'}
	else:
		return {'display': 'none'}


@app.callback(Output('dropdown', 'options'),  # change the dropdown options
			[Input('tabs','value')])
def change_dropdown_options(value):
	if value == 'demand':
		return  demand_dropdown_options
	elif value == 'comp-set':
		return  compset_dropdown_options
	else:
		return []

@app.callback(Output('small-div', 'children'),  #main div callback
				[Input('tabs', 'value')])

def small_div_content(value):
	if value == 'demand':
		children=[html.Div([
					dcc.Checklist(
					    options=[
					        {'label': 'Show Locations', 'value': 'show-locs'},
					    ],
					    values=[]
					)
				],
				style={
					'marginTop': '12px'
				}),
				html.Div([
					dcc.Graph(id='comp-benchmarking',
						figure = go.Figure(
								data = [go.Bar(
									x = ['Taco Bell', 'Competitor 1', 'Competitor 2', 'Competitor 3'],
									y = [10, 30, 50, 200],
									name = 'Competitor Benchmarking: User Views',
									marker = go.Marker(
										color='rgba(205,31,32,0.54)',
						        		line=dict(
						            		color='rgba(205,31,32,0.81)',
						            		width=2.1),
										)
									)],

						        layout= go.Layout(
						            yaxis={
						                'title': 'User Views',
						                'range': [0,210],
						            	'showline':True,
						        		'showticklabels':True
						            },
						            xaxis={'tickangle':-45},
						            title= 'Competitor Benchmarking: User Views',
						            titlefont={
						                'color':'#000000', 
						                'size':14,
						                'family':'Helvetica'},
						            margin=Margin(l=54, r=0, t=81, b=100)
						        	)
							))
					])

				]
	else:
		children=[html.Div(
			style={'marginTop': '36px','display': 'none'},
			children=[ #this is the div under tabs - should be variable
			])
			]
	return children

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)