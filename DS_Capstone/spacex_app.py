# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Your app code here
# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
# Get unique launch sites

launch_sites = spacex_df['Launch Site'].unique()

# Convert to dropdown options
options = [{'label': site, 'value': site} for site in launch_sites]
min_value = 0
max_value = 10000
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=options,
                                    # value=launch_sites[0] if launch_sites else None,
                                    placeholder="Select a Launch Site",
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the
                                # site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),

                                # TASK 3: Add a slider to select payload range
                                # dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    marks={0: '0', 1000: '1000', 2000: '2000', 3000: '3000', 4000: '4000',
                                           5000: '5000', 6000: '6000', 7000: '7000', 8000: '8000', 9000: '9000',
                                           10000: '10000'},
                                    value=[min_value, max_value]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_graph(selected_site):
    if selected_site == 'ALL' or not selected_site:
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]

    fig = px.pie(filtered_df, names='class', title='Total Success Launches for site {}'.format(selected_site))

    return fig


# app callback for payload slider



# TASK 4:

# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    # Output('success-payload-scatter-chart', 'figure'),
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]

)
def update_scatter_chart(selected_site, payload_range):
    # Filter based on the selected site
    if selected_site == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]

    # Further filter based on the selected payload range
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_range[0]) &
                              (filtered_df['Payload Mass (kg)'] <= payload_range[1])]

    # Create a scatter chart
    fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",  # Replace with actual column names
                     color="Booster Version Category", title="Payload vs. Outcome for Selected Site and Payload Range")

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')
