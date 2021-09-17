# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

# Read the airline data into pandas dataframe
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                  {"label": "All Sites", "value": "ALL"},
                                  {"label": "CCAFS LC-40", "value": "CCAFS LC-40"},
                                  {"label": "VAFB SLC-4E", "value": "VAFB SLC-4E"},
                                  {"label": "KSC LC-39A", "value": "KSC LC-39A"},
                                  {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"},
                                ],
                                value="ALL",
                                placeholder="Please Select a Launch Site Here, or choose to View All Sites",
                                searchable=True),
                                html.Br(),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                    min=0,
                                                    max=10000,
                                                    step=1000,
                                                    value=[min_payload,max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(site_dropdown):
    if site_dropdown == 'ALL':
        df = spacex_df[['Launch Site', 'class']]
        fig = px.pie(spacex_df, values='class',
        names='Launch Site',
        title="Successful launches Across Sites")
        return fig
    else:
        dfb=spacex_df[spacex_df['Launch Site']==site_dropdown]
        class_pie = dfb.groupby(['Launch Site','class']).size().reset_index(name='class count')
        title_pie = f"Successful Launches for {site_dropdown}"
        fig = px.pie(class_pie, values='class count', names='class', title = title_pie)
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
        Output(component_id='success-payload-scatter-chart',component_property='figure'),
        [Input(component_id='site-dropdown',component_property='value'),
        Input(component_id='payload-slider',component_property='value')])
def build_scatter(site_dropdown,slider_range):
    low,high = slider_range
    mask = (spacex_df['Payload Mass (kg)']>low)&(spacex_df['Payload Mass (kg)']<high)
    df_scatter=spacex_df[mask]
        
    if site_dropdown == "ALL":
        
        scatter_fig = px.scatter(df_scatter, x="Payload Mass (kg)", y="class", color="Booster Version Category", title="Payload vs. Outcome for All Sites")
    
    else:
        df_scatterb=df_scatter[df_scatter["Launch Site"] == site_dropdown]
        scatter_fig = px.scatter(df_scatterb, x="Payload Mass (kg)", y="class", color="Booster Version Category",
        title=f"Payload and Booster Versions for launches at {site_dropdown}")
        
    return scatter_fig
    
# Run the app
if __name__ == '__main__':
    app.run_server( )

