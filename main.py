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
						'atl':[33.74832,-84.39111],
						'nyc':[40.71455,-74.00714],
						'sf':[37.77713,-122.41964],
						'la':[34.05349,-118.24532]}

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


miami_search_df = pd.read_csv('https://raw.githubusercontent.com/tanvip/yelp-insights/master/tb_miami_search.csv')
atl_search_df = pd.read_csv('https://raw.githubusercontent.com/tanvip/yelp-insights/master/tb_atl_search.csv')
nyc_search_df = pd.read_csv('https://raw.githubusercontent.com/tanvip/yelp-insights/master/tb_nyc_search.csv')
sf_search_df = pd.read_csv('https://raw.githubusercontent.com/tanvip/yelp-insights/master/tb_sf_search.csv')
la_search_df = pd.read_csv('https://raw.githubusercontent.com/tanvip/yelp-insights/master/tb_la_search.csv')

miami_leads_df = pd.read_csv('https://raw.githubusercontent.com/tanvip/yelp-insights/master/tb_miami_leads.csv')
atl_leads_df = pd.read_csv('https://raw.githubusercontent.com/tanvip/yelp-insights/master/tb_atl_leads.csv')
nyc_leads_df = pd.read_csv('https://raw.githubusercontent.com/tanvip/yelp-insights/master/tb_nyc_leads.csv')
sf_leads_df = pd.read_csv('https://raw.githubusercontent.com/tanvip/yelp-insights/master/tb_sf_leads.csv')
la_leads_df = pd.read_csv('https://raw.githubusercontent.com/tanvip/yelp-insights/master/tb_la_leads.csv')

miami_locs_df = pd.read_csv('https://raw.githubusercontent.com/tanvip/yelp-insights/master/tb_miami_locs.csv')
atl_locs_df = pd.read_csv('https://raw.githubusercontent.com/tanvip/yelp-insights/master/tb_atl_locs.csv')
nyc_locs_df = pd.read_csv('https://raw.githubusercontent.com/tanvip/yelp-insights/master/tb_nyc_locs.csv')
sf_locs_df = pd.read_csv('https://raw.githubusercontent.com/tanvip/yelp-insights/master/tb_sf_locs.csv')
la_locs_df = pd.read_csv('https://raw.githubusercontent.com/tanvip/yelp-insights/master/tb_la_locs.csv')

map_dict = {
	'search':{
		'miami':miami_search_df,
		'atl':atl_search_df,
		'nyc':nyc_search_df,
		'sf':sf_search_df,
		'la':la_search_df
	},
	'leads':{
		'miami':miami_leads_df,
		'atl':atl_leads_df,
		'nyc':nyc_leads_df,
		'sf':sf_leads_df,
		'la':la_leads_df
	},
	'locs':{
		'miami':miami_locs_df,
		'atl':atl_locs_df,
		'nyc':nyc_locs_df,
		'sf':sf_locs_df,
		'la':la_locs_df
	}			
}

comp_bench_x = ['Taco Bell', 'Competitor 1', 'Competitor 2', 'Competitor 3', 'Competitor 4']

comp_benchmarking_dict = {
	'miami':[29,8,29,77,196],
	'atl':[21,7,27,72,63],
	'nyc':[45,10,49,94,401],
	'sf':[186,40,27,241,1969],
	'la':[139,42,170,240,1274]
}


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



review_analysis_dict = {
	'service': {
		'pos':90,
		'neg':51.7,
	},
	'price': {
		'pos':19,
		'neg':7,
	},
	'cleanliness': {
		'pos':34,
		'neg':12,
	},
	'speed': {
		'pos':96,
		'neg':51,
	},
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

impossible_burger_df = pd.read_csv('https://raw.githubusercontent.com/spencerlawrence36/basic/master/insights_dash_data/food_trends/impossible_burger_trend.csv')
brisket_df = pd.read_csv('https://raw.githubusercontent.com/spencerlawrence36/basic/master/insights_dash_data/food_trends/brisket_trend.csv')
ghee_df = pd.read_csv('https://raw.githubusercontent.com/spencerlawrence36/basic/master/insights_dash_data/food_trends/ghee_trend.csv')

mezcal_df = pd.read_csv('https://raw.githubusercontent.com/spencerlawrence36/basic/master/insights_dash_data/mezcal_trend.csv')
bourbon_df = pd.read_csv('https://raw.githubusercontent.com/spencerlawrence36/basic/master/insights_dash_data/food_trends/bourbon_trend.csv')
cold_brew_df = pd.read_csv('https://raw.githubusercontent.com/spencerlawrence36/basic/master/insights_dash_data/cold_brew_trend.csv')

pick_up_df = pd.read_csv('https://raw.githubusercontent.com/spencerlawrence36/basic/master/insights_dash_data/food_trends/pick_up_trend.csv')
apple_pay_df = pd.read_csv('https://raw.githubusercontent.com/spencerlawrence36/basic/master/insights_dash_data/food_trends/apple_pay_trend.csv')
 

impossible_burger_count = impossible_burger_df['count'].tolist()
brisket_count = brisket_df['count'].tolist()
ghee_count = ghee_df['count'].tolist()

mezcal_count = mezcal_df['count'].tolist()
bourbon_count = bourbon_df['count'].tolist()
cold_brew_count = cold_brew_df['count'].tolist()

pick_up_count = pick_up_df['count'].tolist()
apple_pay_count = apple_pay_df['count'].tolist()

#normalize this
impossible_burger_norm = [number/la.norm(impossible_burger_count) for number in impossible_burger_count]
brisket_norm = [number/la.norm(brisket_count) for number in brisket_count]
ghee_norm = [number/la.norm(ghee_count) for number in ghee_count]

mezcal_norm = [number/la.norm(mezcal_count) for number in mezcal_count]
bourbon_norm = [number/la.norm(bourbon_count) for number in bourbon_count]
cold_brew_norm = [number/la.norm(cold_brew_count) for number in cold_brew_count]

pick_up_norm = [number/la.norm(pick_up_count) for number in pick_up_count]
apple_pay_norm = [number/la.norm(apple_pay_count) for number in apple_pay_count]

impossible_burger_norm = impossible_burger_norm[:-1]
brisket_norm = brisket_norm[:-1]
ghee_norm = ghee_norm[:-1]

mezcal_norm = mezcal_norm[:-1]
bourbon_norm = bourbon_norm[:-1]

cold_brew_norm = cold_brew_norm[:-1]
pick_up_norm = pick_up_norm[:-1]
apple_pay_norm = apple_pay_norm[:-1]

impossible_burger_norm_max = max(impossible_burger_norm)
brisket_norm_max = max(brisket_norm)
ghee_norm_max = max(ghee_norm)
mezcal_norm_max = max(mezcal_norm)
bourbon_norm_max = max(bourbon_norm)
cold_brew_norm_max = max(cold_brew_norm)
pick_up_norm_max = max(pick_up_norm)
apple_pay_norm_max = max(apple_pay_norm)

food_trend_max_list = [impossible_burger_norm_max,
							brisket_norm_max,
							ghee_norm_max]

drink_trend_max_list = [mezcal_norm_max,
							bourbon_norm_max,
							cold_brew_norm_max]

experience_trend_max_list = [pick_up_norm_max,
							apple_pay_norm_max]

raw_months = impossible_burger_df['month'].tolist()

trend_months = [x[:-3] for x in raw_months]
trend_months = trend_months[:-1]

trend_dict = {
	'food':[('Impossible Burger', 'rgba(13,40,66,0.7)', impossible_burger_norm),
			('Brisket', 'rgba(168,71,24,0.7)', brisket_norm),
			('Ghee', 'rgba(255,203,9,0.7)', ghee_norm)],
	
	'drinks':[('Mezcal', 'rgba(97,55,169,0.7)', mezcal_norm),
			('Bourbon', 'rgba(45,95,1280,0.7)', bourbon_norm),
			('Cold Brew', 'rgba(45,45,45,0.7)', cold_brew_norm)],

	'experience':[('Apple Pay', 'rgba(0,141,233,0.7)', apple_pay_norm),
			('Pick Up', 'rgba(42,126,57,0.7)', pick_up_norm)]	
	}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

app.layout = html.Div(

	style={'font-family':'Helvetica Neue',
		  'color':'#4D4D4D',
		  'font-size':'18px'},
	children=[ #main div 
	#'https://preview.ibb.co/bucGBy/Screen_Shot_2018_07_21_at_6_49_56_AM.png',
	#https://ibb.co/gJsm8o"><img src="https://preview.ibb.co/b1VHET/logo_2.png
	html.Div([ #logo div 
		html.Img(id='ib-logo',
	    src='https://preview.ibb.co/b1VHET/logo_2.png',
	    style={'height':'150px',
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

			    html.Div(id='small-div', children=[html.Div(id='drop-comp-div', children=[html.Div(
					style={'marginTop': '36px'},
					children=[ #this is the div under tabs - should be variable
					dcc.Dropdown(
				        id='dma-drop',
				        value='la',
				        options=[
				            {'label': 'Atlanta', 'value': 'atl'},
				            {'label': 'Miami', 'value': 'miami'},
				            {'label': 'New York City', 'value': 'nyc'},
				            {'label': 'San Francisco', 'value': 'sf'},
							{'label': 'Los Angeles', 'value': 'la'},  
							        ]
							    )]

						),
					html.Div([
						dcc.Checklist(
							id='show-locs-check',
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
						dcc.Graph(id='comp-benchmarking')
						])

					]),])

				], className = 'three columns'),

		html.Div(id='main-div')
		],
		className='row'
	),
    
    html.Div(id='tab-output'),
    
])])

@app.callback(Output('comp-benchmarking', 'figure'),  #main div callback
				[Input('dma-drop', 'value')])

def update_bar(dma_value):
	y = comp_benchmarking_dict[dma_value]
	max_y = max(y) * 1.1

	trace1 = go.Bar(
					x = comp_bench_x,
					y = y,
					name = 'Competitor Benchmarking: User Views',
					marker = go.Marker(
						color=['rgba(107,67,176,0.54)',
								'rgba(169,216,244,0.54)',
								'rgba(169,216,244,0.54)',
								'rgba(169,216,244,0.54)',
								'rgba(169,216,244,0.54)'],
		        		line=dict(
		            		color=['rgba(107,67,176,0.54)',
								'rgba(169,216,244,0.54)',
								'rgba(169,216,244,0.54)',
								'rgba(169,216,244,0.54)',
								'rgba(169,216,244,0.54)'],
		            		width=2.1),
						)
					)
	trace2 =  go.Bar(
					x = comp_bench_x[1:],
					y = y[1:],
					name = 'Competitor Benchmarking: User Views',
					marker = go.Marker(
						color='rgba(169,216,244,0.54)',
		        		line=dict(
		            		color='rgba(169,216,244,0.81)',
		            		width=2.1),
						)
					)

	figure = go.Figure(
				data = [trace1],

		        layout= go.Layout(
		            yaxis={
		                'title': 'User Views',
		                'range': [0,max_y],
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
			)
	return figure

@app.callback(Output('main-div', 'children'),  #main div callback
				[Input('tabs', 'value'),
				Input('dma-drop', 'value'),
				Input('show-locs-check', 'values')])

def main_div(tab_value, dma_value, show_locs_values):
	if tab_value == 'demand':
		df = map_dict['search'][dma_value]
		center_list = dma_options_dict[dma_value]
		
		data = [{'lat': df['latitude'].head((df.shape[0]/7)).tolist(),
		        'lon': df['longitude'].head((df.shape[0]/7)).tolist(),
		        'mode': 'markers',
		        'hoverinfo': 'none',
		        'marker': {
		            'size':6,
		            'color':'#092D4B'
		        },
		        'type': 'scattermapbox',
		        'name': 'Searches'
		    },

			]   
		if show_locs_values != []:
			df2 = map_dict['locs'][dma_value]
			loc_markers = {'lat': df2['business_latitude'].tolist(),
		        'lon': df2['business_longitude'].tolist(),
		        'mode': 'markers',
		        'hoverinfo': 'none',
		        'marker': {
		            'size':42,
		            'color':'rgba(107,67,176,0.54)'
		        },
		        'type': 'scattermapbox',
		        'name': 'Taco Bell Locations'
		    }

			data.append(loc_markers)

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
		    title= 'Fast Food Search - Single Day | 1 dot = 1 search',

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
				dcc.Graph(
							id='comp-set-sankey',
							style={
					            'height': 800
					        },
							figure = dict(
								data = [dict(
								    type='sankey',
								    hoverinfo=None,
								    node = dict(
								      pad = 15,
								      thickness = 20,
								      line = dict(
								        color = "black",
								        width = 0.1
								      ),
								      label = ["McDonald's - 12.1%", #0
								      			"In-N-Out Burger - 4.4%", #1
								      			"Wendy's - 4.2%", #2 
								      			"Chick-fil-A - 4%", #3
								      			"Del Taco - 4%", #4
								      			"Subway - 2.8%", #5
								      			"Burger King - 2.8%", #6
								      			"Popeyes Louisiana Kitchen - 2.3%", #7
								      			"KFC - 2.3%", #8
								      			"Chipotle - 2%", #9
								      			"None - Started on Taco Bell - 59.1%", #10

								      			"Taco Bell", #11

								      			"McDonald's - 10.1%", #12
								      			"Del Taco - 4.1%", #13
								      			"Wendy's - 3.6%", #14
								      			"Burger King - 2.9%", #15
								      			"In-N-Out Burger - 2.7%", #16
								      			"Subway - 2.5%", #17
								      			"KFC - 2.2%", #18
								      			"Jack in the Box - 1.9%", #19 
								      			"Chick-fil-A - 1.8%", #20 
			      								"Chipotle - 1.6%", #21

								      			"None - Ended on Taco Bell - 66.6%"], #20

								      color = ["rgba(250,192,48,0.7)", #0 McDonald's
								      			"rgba(235,95,31,0.7)", #1 In-N-Out
								      			"rgba(169,216,244,0.7)", #2 Wendy's
								      			"rgba(206,44,44,0.7)", #3 CFA
								      			"rgba(238,189,125,0.7)", #4 Del Taco
								      			"rgba(57,135,67,0.7)", #5 Subway
								      			"rgba(173,82,35,0.7)", #6 Burger King
								      			"rgba(250,147,75,0.7)", #7 Popeyes
								      			"rgba(236,95,84,0.7)", #8 KFC
								      			"rgba(117,29,8,0.7)", #9 Chipotle

								      			"rgba(107,67,176,0.7)", #center
			      								"rgba(107,67,176,0.7)", #center

			      								"rgba(250,192,48,0.7)", #11 McDonald's
								      			"rgba(238,189,125,0.7)", #12 Del Taco
								      			"rgba(169,216,244,0.7)", #13 Wendy's
								      			"rgba(173,82,35,0.7)", #14 Burger King
								      			"rgba(235,95,31,0.7)", #15 In-N-Out
								      			"rgba(57,135,67,0.7)", #16 Subway
								      			"rgba(236,95,84,0.7)", #17 KFC
								      			"rgba(250,147,75,0.7)", #18 Jack in the Box
								      			"rgba(206,44,44,0.7)", #19 CFA
								      			"rgba(117,29,8,0.7)", #20 Chipotle
								      			]
								    ),

								    link = dict(
								      source = [0,1,2,3,4,5,6,7,8,9,10,11,11,11,11,11,11,11,11,11,11,11,11],
								      target = [11,11,11,11,11,11,11,11,11,11,11,12,13,14,15,16,17,18,19,20,21,22],
								      value = [ 12.1, 4.4, 4.2, 4, 4, 2.8, 2.8, 2.3, 2.3, 2, 59.1,10.1, 4.1, 3.6, 2.9, 2.7, 2.5, 2.2, 1.9, 1.8, 1.6, 66.6],
								      color = ["rgba(107,67,176,0.7)", #Taco Bell
								      			"rgba(250,192,48,0.7)", #0 McDonald's
								      			"rgba(235,95,31,0.7)", #1 In-N-Out
								      			"rgba(169,216,244,0.7)", #2 Wendy's
								      			"rgba(206,44,44,0.7)", #3 CFA
								      			"rgba(238,189,125,0.7)", #4 Del Taco
								      			"rgba(57,135,67,0.7)", #5 Subway
								      			"rgba(173,82,35,0.7)", #6 Burger King
								      			"rgba(250,147,75,0.7)", #7 Popeyes
								      			"rgba(236,95,84,0.7)", #8 KFC
								      			"rgba(117,29,8,0.7)", #9 Chipotle
								      			
								      			"rgba(250,192,48,0.7)", #11 McDonald's
								      			"rgba(238,189,125,0.7)", #12 Del Taco
								      			"rgba(169,216,244,0.7)", #13 Wendy's
								      			"rgba(173,82,35,0.7)", #14 Burger King
								      			"rgba(235,95,31,0.7)", #15 In-N-Out
								      			"rgba(57,135,67,0.7)", #16 Subway
								      			"rgba(236,95,84,0.7)", #17 KFC
								      			"rgba(250,147,75,0.7)", #18 Jack in the Box
								      			"rgba(206,44,44,0.7)", #19 CFA
								      			"rgba(117,29,8,0.7)" #20 Chipotle
			      								"rgba(107,67,176,0.7)", #Taco Bell
								      			]
								  ))],
								layout =  dict(
								    title = "Consumer Flow<br>10% of consumers visiting Taco Bell's Yelp page left for a McDonald's page",
								    font = dict(
								      size = 14
								    )
								    
								  
								)
													))

					], className = 'nine columns')]

		return children 

	elif tab_value == 'reviews':
		children=[
			html.Div([
				dcc.Graph(id='review-analysis',
					figure = go.Figure(
					data=[
					go.Bar(
						    x=['Service', 'Price', 'Cleanliness', 'Speed'],
						    y=[review_analysis_dict['service']['pos'],
						    	review_analysis_dict['price']['pos'],
						    	review_analysis_dict['cleanliness']['pos'],
						    	review_analysis_dict['speed']['pos']],
						    name='Positive Reviews',
						    marker = go.Marker(
								color='rgba(205,31,32,0.54)',
				        		line=dict(
				            		color='rgba(205,31,32,0.81)',
				            		width=2.1))
						),
						go.Bar(
						    x=['Service', 'Price', 'Cleanliness',  'Speed'],
						    y=[review_analysis_dict['service']['neg'],
						    	review_analysis_dict['price']['neg'],
						    	review_analysis_dict['cleanliness']['neg'],
						    	review_analysis_dict['speed']['neg']],
						    name='Negative Reviews',
						    marker = go.Marker(
								color='rgba(250,192,48,0.54)',
				        		line=dict(
				            		color='rgba(250,192,48,0.81)',
				            		width=2.1))
						)
						],

						layout = go.Layout(
							yaxis={
				                'title': "Percent of Reviews Mentioning Term",
				                'range': [0,100],
				            	'showline':True,
				        		'showticklabels':True
				            },
				            xaxis={'tickangle':-45},
				            title= "90% of Taco Bell's positive reviews mention the service",
				            titlefont={
				                'color':'#000000', 
				                'size':18,
				                'family':'Helvetica'},
				            margin=Margin(l=200, r=0, t=81, b=100),
						    barmode='group'
						)
						)


					)], className = 'nine columns')]

		return children

	elif tab_value == 'trends':

		data=[
			{
				'x': trend_months,
	            'y': impossible_burger_norm,
	            'type': 'line',
	            'line': {
	                'color': '#008de9',
	                'width': 4
	            },
	            'name': 'Impossible Burger',
	            'hoverinfo': 'none'
					},

			{
				'x': trend_months,
	            'y': bourbon_norm,
	            'type': 'line',
	            'line': {
	                'color': '#ad5223',
	                'width': 4
	            },
	            'name': 'Bourbon',
	            'hoverinfo': 'none'
					},
			{
				'x': trend_months,
	            'y': mezcal_norm,
	            'type': 'line',
	            'line': {
	                'color': '#0d2842',
	                'width': 4
	            },
	            'name': 'Mezcal',
	            'hoverinfo': 'none'
					},

				]

        layout = go.Layout(
        	height=800,
            yaxis={
                'title': 'Search Demand',
                'range': [0,1],
            	'showline':False,
        		'showticklabels':False
            },
			title= 'Food Trends',
            titlefont={
                'color':'#000000', 
                'size':18,
                'family':'Helvetica'},
            margin=Margin(l=100, r=100, t=50, b=100)
        
        ),

        children = [html.Div(
        				id='trends',
        				children=[
        				dcc.Graph(id='trend', figure = dict(data=data, layout=layout)),
        				html.P('Since Yelp is the #1 place to find local restaurants, we can identify emerging food trends before they are widely known.  In this case, "Impossible Burger" and other "impossible" meats are becoming incredibly popular.')
        				],className = 'nine columns')]

        return children


@app.callback(Output('drop-comp-div', 'style'),  #main div callback
				[Input('tabs', 'value')])
def show_hide_drop(value):
	if value =='demand':
		style={}
	
	elif value != 'demand':
		style={'display':'none'}
	return style

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)