# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),])
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)

# Get unique launch sites from spacex_df
launch_sites = spacex_df['Launch Site'].unique().tolist()

# Create dropdown options
dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}]  # default "All Sites" option
dropdown_options += [{'label': site, 'value': site} for site in launch_sites]

# Add dropdown to layout
html.Div([
    html.Br(),
    dcc.Dropdown(
        id='site-dropdown',
        options=dropdown_options,
        value='ALL',  # default selection
        placeholder="Select a Launch Site here",
        searchable=True
    )
])


                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
import plotly.express as px

# Callback for pie chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Show total successful launches by site
        df_grouped = spacex_df[spacex_df['class'] == 1].groupby('Launch Site').size().reset_index(name='Successes')
        fig = px.pie(df_grouped, names='Launch Site', values='Successes',
                     title='Total Successful Launches by Site')
    else:
        # Show success vs failure counts for selected site
        df_site = spacex_df[spacex_df['Launch Site'] == selected_site]
        df_counts = df_site['class'].value_counts().reset_index()
        df_counts.columns = ['Class', 'Count']
        fig = px.pie(df_counts, names='Class', values='Count',
                     title=f'Success vs Failure for {selected_site}')
    return fig


                            
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
# Add slider to layout
dcc.RangeSlider(
    id='payload-slider',
    min=spacex_df['Payload Mass (kg)'].min(),
    max=spacex_df['Payload Mass (kg)'].max(),
    step=100,
    marks={0: '0', 1000:'1000', 2000:'2000', 3000:'3000', 4000:'4000'},
    value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]
)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                # CORRECT: decorator must start at the beginning of the line
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    # your function body
    ...

def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                             (spacex_df['Payload Mass (kg)'] <= high)]
    
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
    
    fig = px.scatter(
        filtered_df, x='Payload Mass (kg)', y='class',
        color='Booster Version Category',  # optional: show booster type
        title='Payload vs Launch Outcome'
    )
    return fig


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server() 
