
import dash
from dash import dcc, html  
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash(__name__)


data_url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
covid_data = pd.read_csv(data_url)

covid_data = covid_data[['location', 'date', 'total_cases', 'new_cases', 'total_deaths']]

covid_data['date'] = pd.to_datetime(covid_data['date'])

countries = covid_data['location'].unique()
dropdown_options = [{'label': country, 'value': country} for country in countries]


app.layout = html.Div([
    html.H1("Interactive COVID-19 Dashboard"),
    
    
    html.Label("Select a country to visualize COVID-19 data:"),
    dcc.Dropdown(
        id='country_dropdown',
        options=dropdown_options,
        value='United States', 
        multi=False
    ),
    
   
    dcc.Graph(id='covid_graph')
])



@app.callback(
    Output('covid_graph', 'figure'),
    [Input('country_dropdown', 'value')]
)
def update_graph(selected_country):
    """Filter data and update the graph dynamically."""

    country_data = covid_data[covid_data['location'] == selected_country]
    
   
    trace_total_cases = go.Scatter(
        x=country_data['date'],
        y=country_data['total_cases'],
        mode='lines',
        name="Total Cases"
    )
    
    trace_new_cases = go.Scatter(
        x=country_data['date'],
        y=country_data['new_cases'],
        mode='lines',
        name="New Cases"
    )
    
    trace_total_deaths = go.Scatter(
        x=country_data['date'],
        y=country_data['total_deaths'],
        mode='lines',
        name="Total Deaths"
    )
    

    layout = go.Layout(
        title=f"COVID-19 Data for {selected_country}",
        xaxis={"title": "Date"},
        yaxis={"title": "Count"},
        showlegend=True
    )
    

    fig = go.Figure(data=[trace_total_cases, trace_new_cases, trace_total_deaths], layout=layout)
    
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
