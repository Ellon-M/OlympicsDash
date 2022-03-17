import time
from threading import Timer
import pandas as pd
import numpy as np
from dash import Dash, html, dcc, Input, Output, callback_context
from utils import *
import plotly.graph_objects as go
import plotly.express as px
from dash.exceptions import PreventUpdate

app = Dash(
        __name__
        )

df = pd.read_csv('./Olympics Dataset.csv') 

def generate_seasons(season):
        if season == "Summer":
            summ = df.query('Season == "Summer"')
            summ = summ.reset_index()
           
            return summ

        elif season == "Winter":
            win = df.query('Season == "Winter"')
            win = win.reset_index()

            return win

        else:
            raise ValueError('Incorrectly specified data.')




app.layout = html.Div(
            className="container",
            children = [
                html.Div(
                    id="top-dropdown",
                    children = [
                        html.Div(
                            id="refresh-btn",
                            ),
                        html.Button("Summer", 
                                    id="summer-btn",
                                    n_clicks=0),
                        html.Button("Winter",
                                    id="winter-btn",
                                    n_clicks=0)
                    ]
                ),
                html.Div(
                    id="left-col",
                    children = [
                        html.Section(
                            className="country-dropdown-sec",
                            children = [
                                 NamedDropdown(
                                     name = "Select Country:",
                                    id = "countries-dropdown",
                                    options = [
                                        {"label": "Canada",
                                        "value": "Canada"},
                                        {"label": "United States",
                                        "value": "United States"}
                                        ],
                                    clearable = False,
                                    searchable = False,
                                    value="Canada",
                                    )
                                 ]
                             ),
                         html.Section(
                             className = "year-dropdown-sec",
                             children = [
                                NamedDropdown(
                                    name = "Select Year:",
                                     id = "year-dropdown",
                                     clearable = False,
                                     searchable = False,
                                    ),
                                    
                                ]
                            ),
                          html.Section(
                              className="sport-dropdown-sec",
                              children = [
                                NamedDropdown(
                                    name = "Select Sport:",
                                     id = "event-dropdown",
                                     clearable = False,
                                     searchable = False,
                                )
                            ]
                        ),
                    ]
                ),
                html.Div(
                        id="graph-content",
                        )
                ]
)

changes = []

@app.callback(
       output = [Output('refresh-btn', 'children'),
                 Output('year-dropdown', 'options'),
                 Output('event-dropdown', 'options'),
                 Output('graph-content', 'children')],
       inputs = [Input('countries-dropdown', 'value'),
                 Input('year-dropdown', 'value'),
                 Input('event-dropdown', 'value'),
                 Input('summer-btn', 'n_clicks'),
                 Input('winter-btn', 'n_clicks')
                 ]
    )
def displayGraphs(country, year, sport, sumbtn, winbtn):
    
    country_winter = df.query('Team == "{}" and Season == "Winter"'.format(country))
    country_summer = df.query('Team == "{}" and Season == "Summer"'.format(country))
    win_sports = pd.Series(country_winter.Sport.unique()).sort_values(ascending=False)
    win_sports_list = win_sports.tolist()
    win_years = pd.Series(country_winter.Year.unique()).sort_values(ascending=False)
    win_years_list = win_years.tolist()
    sum_sports = pd.Series(country_summer.Sport.unique()).sort_values(ascending=False)
    sum_sports_list = sum_sports.tolist()
    sum_years = pd.Series(country_summer.Year.unique()).sort_values(ascending=False)
    sum_years_list = sum_years.tolist()
    changed = callback_context.triggered
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]

    if 'winter-btn' in changed_id:
         changes.append(changed_id)
         refresh = html.Meta(httpEquiv="refresh",content="0")
    elif 'summer-btn' in changed_id:
         changes.append(changed_id)
         refresh = html.Meta(httpEquiv="refresh",content="0")
    elif 'event-dropdown' in changed_id:
        changes.append(changed_id)
        refresh = None
    elif 'year-dropdown' in changed_id:
        changes.append(changed_id)
        refresh = None
    else:
        refresh = None
        pass
    
    print(changes)

     
    if (('summer-btn.n_clicks' in changes) and 'winter-btn.n_clicks' not in changes):
        

         print('sum')
         kv_sports = [{"label":str(sum_sport), "value": str(sum_sport)} for sum_sport in sum_sports_list]
         kv_sports.append({"label": "All", "value": "All"})


         kv_years = [{"label":str(sum_year), "value": str(sum_year)} for sum_year in sum_years]
         kv_years.append({"label": "All", "value": "All"})


         if (country != None and year != None and sport != None):

        
            country_summer_year_sport = country_summer.query('Sport == "{}" and Year == {}'.format(sport, year))
             

            main_fig = px.bar(country_summer_year_sport, x = "Event")
            main_fig.update_layout(
                                title="Summer Events in {}, {}".format(sport, year),
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font = dict(size=14),
                                )


         elif (country != None and year != None and sport == None):

            country_summer_year = country_summer.query('Year == {}'.format(year))

            main_fig = px.histogram(country_summer_year, x = "Event")
            main_fig.update_layout(bargap=0.1,  
                                   xaxis = dict(showticklabels=False),
                                   title="Summer Events, {}".format(year), 
                                   paper_bgcolor='rgba(0,0,0,0)',
                                   plot_bgcolor='rgba(0,0,0,0)',
                                   font = dict(size=14),
                                   )   



         elif (country != None and sport != None and year == None):

            country_summer_year = country_summer.query('Sport == {}'.format(year))
             
            main_fig = px.histogram(country_summer_year, x = "Event")
            main_fig.update_layout(bargap=0.1,
                                    xaxis = dict(showticklabels=False),
                                    title="Summer Events, {}".format(year),
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    font = dict(size=14),
                                   )



         elif (country != None and year == None and sport == None):
             country_summer_medals = country_summer[~country_summer['Medal'].isnull()]
             country_summer_medals_count = country_summer_medals.groupby(['Year']).count()['Medal'].to_frame().reset_index()
             
             main_fig = go.Figure(data=go.Scatter(
                             x = country_summer_medals_count['Year'],
                             y = country_summer_medals_count['Medal'],
                             mode='markers',
                             marker=dict(
                             size=18,
                             color= country_summer_medals_count['Medal'],
                             colorscale='magenta',
                             showscale=True
                            )
                        ))  

             main_fig.update_layout(
                title="Summer Medal Count Over Time",
                xaxis_title="Years",
                yaxis_title="Medals",
                legend_title="Medal Count",
                font=dict(
                    size=14,
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
             )
         else:
             raise ValueError("Incorrectly specified data")
    


    elif (('winter-btn.n_clicks' in changes)):
        #print('win') 
        last_change = changes[-1:]
        clicks_change = ['year-dropdown.value', 'event-dropdown.value', 'summer-btn.n_clicks']
        
        #for click in clicks_change:
        #    if click in changes:
        #       changes.remove(click)
        changes.clear()


        kv_sports = [{"label":str(win_sport), "value": str(win_sport)} for win_sport in win_sports]
        kv_sports.append({"label": "All", "value": "All"})

        kv_years = [{"label":str(win_year), "value": str(win_year)} for win_year in win_years]
        kv_years.append({"label": "All", "value": "All"})




        if (country != None and year != None and sport != None):

             country_winter_year_sport = country_winter.query('Sport == "{}" and Year == {}'.format(sport, year))

             main_fig = px.bar(country_winter_year_sport, x = "Event")
             main_fig.update_layout(
                                    title="Winter Events in {}, {}".format(sport, year),
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    font = dict(size=14),
                        )

        elif (country != None and sport != None and year == None):

             country_winter_year = country_winter.query('Sport == {}'.format(year))

             main_fig = px.histogram(country_winter_year, x = "Event")

             main_fig.update_layout(bargap=0.1,
                                    xaxis = dict(showticklabels=False),
                                    title="Winter Events, {}".format(year),
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    font = dict(size=14),
                                   )
        elif (country != None and year != None and sport == None):

             country_winter_year = country_winter.query('Year == {}'.format(year))

             main_fig = px.histogram(country_winter_year, x = "Event")

             main_fig.update_layout(bargap=0.1,
                                    xaxis = dict(showticklabels=False),
                                    title="Winter Events, {}".format(year),
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    font = dict(size=14),
                                   )



        elif (country != None and year == None and sport == None):
             country_winter_medals = country_winter[~country_winter['Medal'].isnull()]
             country_winter_medals_count = country_winter_medals.groupby(['Year']).count()['Medal'].to_frame().reset_index()


             main_fig = go.Figure(data=go.Scatter(
                             x = country_winter_medals_count['Year'],
                             y = country_winter_medals_count['Medal'],
                             mode='markers',
                             marker=dict(
                             size=18,
                             color= country_winter_medals_count['Medal'],
                             colorscale='magenta',
                             showscale=True
                            )
             ))


             main_fig.update_layout(
                title="Winter Medal Count Over Time",
                xaxis_title="Years",
                yaxis_title="Medals",
                legend_title="Medal Count",
                font=dict(
                    size=14,
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
             )
        else:
             raise ValueError("Incorrectly specified data")

    else:
         kv_sports = [{"label":str(sum_sport), "value": str(sum_sport)} for sum_sport in sum_sports_list]
         kv_sports.append({"label": "All", "value": "All"})


         kv_years = [{"label":str(sum_year), "value": str(sum_year)} for sum_year in sum_years]
         kv_years.append({"label": "All", "value": "All"})
         
         
         if (changes[-1:] == ["winter-btn.n_clicks"] or ["year-dropdown.value"] or ["event-dropdown.value"]):

             kv_sports = [{"label":str(win_sport), "value": str(win_sport)} for win_sport in win_sports]
             kv_sports.append({"label": "All", "value": "All"})

             kv_years = [{"label":str(win_year), "value": str(win_year)} for win_year in win_years]
             kv_years.append({"label": "All", "value": "All"})


             print('changes', changes)

             if (country != None and year != None and sport != None):
                 country_winter_year_sport = country_winter.query('Sport == "{}" and Year == {}'.format(sport, year))


                 main_fig = px.bar(country_winter_year_sport, x = "Event")
                 main_fig.update_layout(
                                    title="Winter Events in {}, {}".format(sport, year),
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    font = dict(size=14),
                                   )



             elif (country != None and year != None):
                country_winter_year = country_winter.query('Year == {}'.format(year))

                main_fig = px.histogram(country_winter_year, x = "Event")
                main_fig.update_layout(bargap=0.1,
                                    xaxis = dict(showticklabels=False),
                                    title="Winter Events, {}".format(year),
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    font = dict(size=14),
                                    )

             elif (country != None and sport != None):
                 country_winter_year = country_winter.query('Sport == {}'.format(year))

                 main_fig = px.histogram(country_winter_year, x = "Event")
                 main_fig.update_layout(bargap=0.1,
                                    xaxis = dict(showticklabels=False),
                                    title="Summer Events, {}".format(year),
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    font = dict(size=14),
                                   )
             else:
                country_winter_medals = country_winter[~country_winter['Medal'].isnull()]
                country_winter_medals_count = country_winter_medals.groupby(['Year']).count()['Medal'].to_frame().reset_index()


                main_fig = go.Figure(data=go.Scatter(
                             x = country_winter_medals_count['Year'],
                             y = country_winter_medals_count['Medal'],
                             mode='markers',
                             marker=dict(
                             size=18,
                             color= country_winter_medals_count['Medal'],
                             colorscale='magenta',
                             showscale=True
                            )
                ))


                main_fig.update_layout(
                    title="Winter Medal Count Over Time",
                    xaxis_title="Years",
                    yaxis_title="Medals",
                    legend_title="Medal Count",
                    font=dict(
                        size=14,
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )


         else:
            
            if (country != None and year != None and sport != None):
                 country_summer_year_sport = country_summer.query('Sport == "{}" and Year == {}'.format(sport, year))


                 main_fig = px.bar(country_summer_year_sport, x = "Event")
                 main_fig.update_layout(
                                    title="xummer Events in {}, {}".format(sport, year),
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    font = dict(size=14),
                                   )



            elif (country != None and year != None):
                country_summer_year = country_summer.query('Year == {}'.format(year))

                main_fig = px.histogram(country_summer_year, x = "Event")
                main_fig.update_layout(bargap=0.1,
                                    xaxis = dict(showticklabels=False),
                                    title="xummer Events, {}".format(year),
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    font = dict(size=14),
                                    )

            elif (country != None and sport != None):
                 country_summer_year = country_summer.query('Sport == {}'.format(year))

                 main_fig = px.histogram(country_summer_year, x = "Event")
                 main_fig.update_layout(bargap=0.1,
                                    xaxis = dict(showticklabels=False),
                                    title="xummer Events, {}".format(year),
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    font = dict(size=14),
                                   )



            elif (country != None and year == None and sport == None):
                 country_summer_medals = country_summer[~country_summer['Medal'].isnull()]
                 country_summer_medals_count = country_summer_medals.groupby(['Year']).count()['Medal'].to_frame().reset_index()

                 main_fig = go.Figure(data=go.Scatter(
                             x = country_summer_medals_count['Year'],
                             y = country_summer_medals_count['Medal'],
                             mode='markers',
                             marker=dict(
                             size=18,
                             color= country_summer_medals_count['Medal'],
                             colorscale='magenta',
                             showscale=True
                            )
                        ))

                 main_fig.update_layout(
                    title="xummer Medal Count Over Time",
                    xaxis_title="Years",
                    yaxis_title="Medals",
                    legend_title="Medal Count",
                    font=dict(
                        size=14,
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
            else:
                 raise ValueError("Incorrectly specified data")

    return [refresh,
            kv_years,
            kv_sports,
            html.Div(
             id="graph-container",
             children=dcc.Loading(
                className="graph-wrapper",
                children=dcc.Graph(id="graph-main", figure=main_fig),
                ),
            ),
          ]


if __name__ == '__main__':
    app.run_server(debug=True)


                                     

                            


                        



