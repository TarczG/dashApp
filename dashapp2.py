from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd


df1 = pd.read_csv('life_expectancy.csv') #Source: https://data.worldbank.org/indicator/SP.DYN.LE00.IN?locations=1W&start=1984&view=chart
df2=pd.read_csv('poverty.csv') #Source:https://data.worldbank.org/indicator/SI.POV.DDAY?locations=1W&start=1984&view=chart
df3=pd.read_csv('population.csv') #Source: https://data.worldbank.org/indicator/SP.POP.TOTL
df4=pd.read_csv('continents_country.csv') #Source: https://worldpopulationreview.com/country-rankings/list-of-countries-by-continent


# one observation = one row. Divide data accorduing to this idea
df1=pd.melt(frame=df1, id_vars=['Country Name'], value_vars=['1995','2000','2005','2010','2015','2020'],value_name='lifeExpectation',var_name='year')
df2=pd.melt(frame=df2, id_vars=['Country Name'], value_vars=['1995','2000','2005','2010','2015','2020'],value_name='poverty',var_name='year')
df3=pd.melt(frame=df3, id_vars=['Country Name'], value_vars=['1995','2000','2005','2010','2015','2020'],value_name='population',var_name='year')



#deleting records with NaN 
df1=df1.dropna()
df2=df2.dropna()
df3=df3.dropna()

#merging data - part 1
life_poverty = pd.merge(df1,df2,
                                   left_on=['Country Name','year'],
                                   right_on=['Country Name','year']
                                   )
life_poverty_population = pd.merge(life_poverty,df3,
                                   left_on=['Country Name','year'],
                                   right_on=['Country Name','year']
                                   )
#merging data - part 2 - by vlookup
life_poverty_population_continent = pd.merge(life_poverty_population,df4[["Country Name","continent"]],on = "Country Name", how="left")
#changing type of vlues
life_poverty_population_continent.year = pd.to_numeric(life_poverty_population_continent.year)

#display data - thanks to dash library
app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        life_poverty_population_continent['year'].min(),
        life_poverty_population_continent['year'].max(),
        step=None,
        value=life_poverty_population_continent['year'].min(),
        marks={str(year): str(year) for year in life_poverty_population_continent['year'].unique()},
        id='year-slider'
    )
],style= {'width':'90%'})


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = life_poverty_population_continent[life_poverty_population_continent.year == selected_year]

    fig = px.scatter(filtered_df, x="poverty", y="lifeExpectation",
                     size="population", color="continent", hover_name="Country Name",
                     log_x=True, size_max=55,labels={
                        "poverty" : "poverty (% of population) ",
                        "lifeExpectation" : "life  expectation (years)"},
                        title="Impact of poverty on life expectancy")

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

x=input('zakoncz')