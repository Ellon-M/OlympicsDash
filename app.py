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
                        ),
                html.Div(
                    id="right-graph-content"
                        ),
                html.Div(
                    id="stats-content"
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

     
    if (('summer-btn.n_clicks' in changes) and 'winter-btn.n_clicks' not in changes):
        
         kv_sports = [{"label":str(sum_sport), "value": str(sum_sport)} for sum_sport in sum_sports_list]
         kv_sports.append({"label": "All", "value": "All"})

         kv_years = [{"label":str(sum_year), "value": str(sum_year)} for sum_year in sum_years]
         kv_years.append({"label": "All", "value": "All"})


         if (country != None and year != None and sport != None):
                 csys = country_summer.groupby(['Sport', 'Year', 'Event', 'Sex']).count()['ID'].to_frame().reset_index()
                 csys = csys.rename(columns={'ID': 'Athlete Count'})
 
                 country_summer_year_sport = csys.query('Sport == "{}" and Year == {}'.format(sport, year))
 
 
                 main_fig = px.bar(country_summer_year_sport, x = "Event", y="Athlete Count", text="Athlete Count",
                              hover_data=["Athlete Count"], color="Sex",
                              color_discrete_map={
                                  'M': '#DAA06D',
                                  'F': '#F89880'
                                 }
                              )
 
                 main_fig.update_layout(
                                      title="Summer Events in {}, {}".format(sport, year),
                                      paper_bgcolor='rgba(0,0,0,0)',
                                      plot_bgcolor='rgba(0,0,0,0)',
                                      font = dict(size=14),
                                      yaxis_title="Athlete count",
                                     )
        


         elif (country != None and year != None and sport == None):
             csy = country_summer.groupby(['Event', 'Year']).count().reset_index()
             csy = csy.rename(columns={'ID': 'Athlete-count'})
 
             country_summer_year = csy.query('Year == {}'.format(year))
 
             main_fig = px.bar(country_summer_year, x = "Event", y="Athlete-count", text = "Athlete-count",
                                     hover_data=["Athlete-count"], color="Athlete-count", color_continuous_scale="sunset")
 
             main_fig.update_layout(bargap=0.1,
                                      xaxis = dict(showticklabels=False),
                                      title="Summer Events, {}".format(year),
                                      paper_bgcolor='rgba(0,0,0,0)',
                                      plot_bgcolor='rgba(0,0,0,0)',
                                      font = dict(size=14),
                                   )


         elif (country != None and sport != None and year == None):

                   css = country_summer.groupby(['Event', 'Sport']).count().reset_index()
                   css = css.rename(columns={'ID': 'Athlete-count'})
 
                   country_summer_sp = css.query('Sport == "{}"'.format(sport))
 
 
                   main_fig = px.bar(country_summer_sp, x = "Event", y="Athlete-count", text="Athlete-count",
                                     hover_data=["Athlete-count"],
                                     color="Athlete-count", color_continuous_scale="sunset")
 
                   main_fig.update_layout(bargap=0.1,
                                          xaxis = dict(showticklabels=False),
                                          title="Summer Events, {}".format(sport),
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
                             colorscale='Burg',
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
        
        changes.clear()


        kv_sports = [{"label":str(win_sport), "value": str(win_sport)} for win_sport in win_sports]
        kv_sports.append({"label": "All", "value": "All"})

        kv_years = [{"label":str(win_year), "value": str(win_year)} for win_year in win_years]
        kv_years.append({"label": "All", "value": "All"})



        if (country != None and year != None and sport != None):
                  cwys = country_winter.groupby(['Sport', 'Year', 'Event', 'Sex']).count()['ID'].to_frame().reset_index()
                  cwys = cwys.rename(columns={'ID': 'Athlete Count'})
 
                  country_winter_year_sport = cwys.query('Sport == "{}" and Year == {}'.format(sport, year))
 
 
                  main_fig = px.bar(country_winter_year_sport, x = "Event", y="Athlete Count", text="Athlete Count",
                             hover_data=["Athlete Count"], color="Sex",
                             color_discrete_map={
                                               'M': '#1434A4',
                                               'F': '#088F8F'
                                              }
                             )
                  main_fig.update_layout(
                                     title="Winter Events in {}, {}".format(sport, year),
                                     paper_bgcolor='rgba(0,0,0,0)',
                                     plot_bgcolor='rgba(0,0,0,0)',
                                     font = dict(size=14),
                                     yaxis_title="Athlete count",
                                    )

            
        elif (country != None and sport != None and year == None):
                  cws = country_winter.groupby(['Event', 'Sport']).count().reset_index()
                  cws = cws.rename(columns={'ID': 'Athlete-count'})
 
                  country_winter_sp = cws.query('Sport == "{}"'.format(sport))
 
 
                  main_fig = px.bar(country_winter_sp, x = "Event", y="Athlete-count", text="Athlete-count",
                                    hover_data=["Athlete-count"],
                                    color="Athlete-count", color_continuous_scale="teal")
 
                  main_fig.update_layout(bargap=0.1,
                                         xaxis = dict(showticklabels=False),
                                         title="Winter Events, {}".format(sport),
                                         paper_bgcolor='rgba(0,0,0,0)',
                                         plot_bgcolor='rgba(0,0,0,0)',
                                         font = dict(size=14),
                                         )

        elif (country != None and year != None and sport == None):

                  cwy = country_winter.groupby(['Event', 'Year']).count().reset_index()
                  cwy = cwy.rename(columns={'ID': 'Athlete-count'})
 
                  country_winter_year = cwy.query('Year == {}'.format(year))
 
                  main_fig = px.bar(country_winter_year, x = "Event", y="Athlete-count", text="Athlete-count",
                                    hover_data=["Athlete-count"], color="Athlete-count", color_continuous_scale="teal")
 
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
                 cwys = country_winter.groupby(['Sport', 'Year', 'Event', 'Sex']).count()['ID'].to_frame().reset_index()
                 cwys = cwys.rename(columns={'ID': 'Athlete Count'})

                 country_winter_year_sport = cwys.query('Sport == "{}" and Year == {}'.format(sport, year))


                 main_fig = px.bar(country_winter_year_sport, x = "Event", y="Athlete Count", text="Athlete Count", 
                            hover_data=["Athlete Count"], color="Sex", 
                            color_discrete_map={
                                              'M': '#1434A4',
                                              'F': '#088F8F'
                                             }
                            )
                 main_fig.update_layout(
                                    title="Winter Events in {}, {}".format(sport, year),
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    font = dict(size=14),
                                    yaxis_title="Athlete count",
                                   )


             elif (country != None and year != None and sport == None):
                 cwy = country_winter.groupby(['Event', 'Year']).count().reset_index()
                 cwy = cwy.rename(columns={'ID': 'Athlete-count'})

                 country_winter_year = cwy.query('Year == {}'.format(year))
                
                 main_fig = px.bar(country_winter_year, x = "Event", y="Athlete-count", text="Athlete-count",
                                   hover_data=["Athlete-count"], color="Athlete-count", color_continuous_scale="teal")

                 main_fig.update_layout(bargap=0.1,
                                    xaxis = dict(showticklabels=False),
                                    title="Winter Events, {}".format(year),
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    font = dict(size=14),
                                    )
                


             elif (country != None and sport != None and year == None):
                 cws = country_winter.groupby(['Event', 'Sport']).count().reset_index()
                 cws = cws.rename(columns={'ID': 'Athlete-count'})

                 country_winter_sp = cws.query('Sport == "{}"'.format(sport))
                 

                 main_fig = px.bar(country_winter_sp, x = "Event", y="Athlete-count", text="Athlete-count",
                                   hover_data=["Athlete-count"], 
                                   color="Athlete-count", color_continuous_scale="teal")

                 main_fig.update_layout(bargap=0.1,
                                        xaxis = dict(showticklabels=False),
                                        title="Winter Events, {}".format(sport),
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
                csys = country_summer.groupby(['Sport', 'Year', 'Event', 'Sex']).count()['ID'].to_frame().reset_index()
                csys = csys.rename(columns={'ID': 'Athlete Count'})
 
                country_summer_year_sport = csys.query('Sport == "{}" and Year == {}'.format(sport, year))
 
 
                main_fig = px.bar(country_summer_year_sport, x = "Event", y="Athlete Count", text="Athlete Count",
                             hover_data=["Athlete Count"], color="Sex",
                             color_discrete_map={
                                 'M': '#DAA06D',
                                 'F': '#F89880'
                                }
                             )

                main_fig.update_layout(
                                     title="Summer Events in {}, {}".format(sport, year),
                                     paper_bgcolor='rgba(0,0,0,0)',
                                     plot_bgcolor='rgba(0,0,0,0)',
                                     font = dict(size=14),
                                     yaxis_title="Athlete count",
                                    )


            elif (country != None and year != None and sport == None):
                    
                  csy = country_summer.groupby(['Event', 'Year']).count().reset_index()
                  csy = csy.rename(columns={'ID': 'Athlete-count'})
 
                  country_summer_year = csy.query('Year == {}'.format(year))
 
                  main_fig = px.bar(country_summer_year, x = "Event", y="Athlete-count", text="Athlete-count",
                                    hover_data=["Athlete-count"], color="Athlete-count", color_continuous_scale="sunset")
 
                  main_fig.update_layout(bargap=0.1,
                                     xaxis = dict(showticklabels=False),
                                     title="Summer Events, {}".format(year),
                                     paper_bgcolor='rgba(0,0,0,0)',
                                     plot_bgcolor='rgba(0,0,0,0)',
                                     font = dict(size=14),
                                     )



            elif (country != None and sport != None and year == None):
                  css = country_summer.groupby(['Event', 'Sport']).count().reset_index()
                  css = css.rename(columns={'ID': 'Athlete-count'})
 
                  country_summer_sp = css.query('Sport == "{}"'.format(sport))
 

                  main_fig = px.bar(country_summer_sp, x = "Event", y="Athlete-count", text="Athlete-count",
                                    hover_data=["Athlete-count"],
                                    color="Athlete-count", color_continuous_scale="sunset")
 
                  main_fig.update_layout(bargap=0.1,
                                         xaxis = dict(showticklabels=False),
                                         title="Summer Events, {}".format(sport),
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


@app.callback(
    Output('right-graph-content', 'children'),
    inputs = [Input('countries-dropdown', 'value'),
              Input('year-dropdown', 'value'),
              Input('event-dropdown', 'value'),
              Input('summer-btn', 'n_clicks'),
              Input('winter-btn', 'n_clicks')
             ]
)
def getRightGraphs(country, year, sport, summerbtn, winterbtn):

     country_winter = df.query('Team == "{}" and Season == "Winter"'.format(country)).sort_values(by=['ID'], ascending=False)
     country_summer = df.query('Team == "{}" and Season == "Summer"'.format(country)).sort_values(by=['ID'], ascending=False)

     country_wint = country_winter.groupby(['Medal']).count().reset_index()
     country_summ = country_summer.groupby(['Medal']).count().reset_index()

     if (('summer-btn.n_clicks' in changes) and 'winter-btn.n_clicks' not in changes):
        
        country_summer_year = country_summer.query('Year == {}'.format(year))
        country_summ_year = country_summer_year.groupby(['Medal']).count().reset_index()

        if (country != None and year != None):
            csy = country_summer.query('Year == {}'.format(year))

            v_fig = px.violin(csy, y="Height", color="Sex",
                violinmode='overlay',
                hover_data=country_summer.columns,
                color_discrete_map={
                    "F": "#FFD580", "M": "#FF7518"
                },
                width=600, height=600,
               )

            v_fig.update_layout(
                title="Male and Female Heights in Summer {}".format(year),
                font=dict(
                    size=14,
                 ),
                title_x = 0.5,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )

            p_fig = px.pie(country_summ_year, values='ID', names='Medal', hole=.4, color="Medal",
             color_discrete_map={
                "Gold": "#FFD700", "Silver": "#c0c0c0", "Bronze": " #b08d57"
                },width=600, height=600)

            p_fig.update_layout(
                title="Medals Won, Summer {}".format(year),
                font=dict(
                    size=14,
                ),
                title_x = 0.5,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )


        elif (country != None and year == None and sport == None):
            v_fig = px.violin(country_summer, y="Height", color="Sex",
                violinmode='overlay',
                hover_data=country_summer.columns,
                color_discrete_map={
                    "F": "#FFD580", "M": "#FF7518"
                },
                width=600, height=600,
               )

            v_fig.update_layout(
                title="Male and Female Heights, Summer",
                font=dict(
                    size=14,
                ),
                title_x = 0.5,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )

            p_fig = px.pie(country_summ, values='ID', names='Medal', hole=.4, color="Medal",
             color_discrete_map={
                "Gold": "#FFD700", "Silver": "#c0c0c0", "Bronze": " #b08d57"
                },width=600, height=600)

            p_fig.update_layout(
                title="Medals Won, Summer",
                font=dict(
                    size=14,
                ),
                title_x = 0.5,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )


        else:
             raise ValueError("Incorrectly specified data")

     elif (('winter-btn.n_clicks' in changes)):

         country_winter_year = country_winter.query('Year == {}'.format(year))
         country_wint_year = country_winter_year.groupby(['Medal']).count().reset_index()

         if (country != None and year != None):
             cwy = country_winter.query('Year == {}'.format(year))
 
             v_fig = px.violin(cwy, y="Height", color="Sex",
                 violinmode='overlay',
                 hover_data=country_winter.columns,
                 color_discrete_map={
                 "F": "#ff6fff", "M": "#c84186"
                 },
                 width=600, height=600,
                )
 
             v_fig.update_layout(
                 title="Male and Female Heights in Winter {}".format(year),
                 font=dict(
                     size=14,
                  ),
                 title_x = 0.5,
                 paper_bgcolor='rgba(0,0,0,0)',
                 plot_bgcolor='rgba(0,0,0,0)'
             )

             p_fig = px.pie(country_wint_year, values='ID', names='Medal', hole=.4, color="Medal",
             color_discrete_map={
                "Gold": "#FFD700", "Silver": "#c0c0c0", "Bronze": " #b08d57"
                },width=600, height=600)

             p_fig.update_layout(
                title="Medals Won, Winter {}".format(year),
                font=dict(
                    size=14,
                ),
                title_x = 0.5,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
             )

 
         elif (country != None and year == None and sport == None):
             v_fig = px.violin(country_winter, y="Height", color="Sex",
                 violinmode='overlay',
                 hover_data=country_winter.columns,
                 color_discrete_map={
                 "F": "#ff6fff", "M": "#c84186"
                 },
                 width=600, height=600,
                )
 
             v_fig.update_layout(
                 title="Male and Female Heights, Winter",
                 font=dict(
                     size=14,
                 ),
                 title_x = 0.5,
                 paper_bgcolor='rgba(0,0,0,0)',
                 plot_bgcolor='rgba(0,0,0,0)'
             )

             p_fig = px.pie(country_wint, values='ID', names='Medal', hole=.4, color="Medal",
             color_discrete_map={
                "Gold": "#FFD700", "Silver": "#c0c0c0", "Bronze": " #b08d57"
                },width=600, height=600)

             p_fig.update_layout(
                title="Medals Won, Winter",
                font=dict(
                    size=14,
                ),
                title_x = 0.5,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
)

 
         else:
              raise ValueError("Incorrectly specified data")

     else:
        if (changes[-1:] == ["winter-btn.n_clicks"] or ["year-dropdown.value"] or ["event-dropdown.value"]):

          country_winter_year = country_winter.query('Year == {}'.format(year))
          country_wint_year = country_winter_year.groupby(['Medal']).count().reset_index()

          if (country != None and year != None):
              cwy = country_winter.query('Year == {}'.format(year))
 
              v_fig = px.violin(cwy, y="Height", color="Sex",
                  violinmode='overlay',
                  hover_data=country_winter.columns,
                  color_discrete_map={
                  "F": "#ff6fff", "M": "#c84186"
                  },
                  width=600, height=600,
                 )
 
              v_fig.update_layout(
                  title="Male and Female Heights in Winter {}".format(year),
                  font=dict(
                      size=14,
                   ),
                  title_x = 0.5,
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)'
              )

              p_fig = px.pie(country_wint_year, values='ID', names='Medal', hole=.4, color="Medal",
                    color_discrete_map={
                        "Gold": "#FFD700", "Silver": "#c0c0c0", "Bronze": " #b08d57"
                    },width=600, height=600)
 
              p_fig.update_layout(
                  title="Medals Won, Winter {}".format(year),
                  font=dict(
                      size=14,
                  ),
                  title_x = 0.5,
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)'
               )



 
          elif (country != None and year == None and sport == None):
                v_fig = px.violin(country_winter, y="Height", color="Sex",
                   violinmode='overlay',
                   hover_data=country_winter.columns,
                   color_discrete_map={
                     "F": "#ff6fff", "M": "#c84186"
                  },
                   width=600, height=600,
                 )
 
                v_fig.update_layout(
                   title="Male and Female Heights, Winter",
                   font=dict(
                      size=14,
                   ),
                   title_x = 0.5,
                   paper_bgcolor='rgba(0,0,0,0)',
                   plot_bgcolor='rgba(0,0,0,0)'
                )

                p_fig = px.pie(country_wint, values='ID', names='Medal', hole=.4, color="Medal",
                      color_discrete_map={
                          "Gold": "#FFD700", "Silver": "#c0c0c0", "Bronze": " #b08d57"
                      },width=600, height=600)
 
                p_fig.update_layout(
                    title="Medals Won, Winter",
                    font=dict(
                        size=14,
                    ),
                    title_x = 0.5,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )

 
          else:
               raise ValueError("Incorrectly specified data")
        
        else:
          
           country_summer_year = country_summer.query('Year == {}'.format(year))
           country_summ_year = country_summer_year.groupby(['Medal']).count().reset_index()

           if (country != None and year != None):
             csy = country_summer.query('Year == {}'.format(year))
 
             v_fig = px.violin(csy, y="Height", color="Sex",
                 violinmode='overlay',
                 hover_data=country_summer.columns,
                 color_discrete_map={
                  "F": "#FFD580", "M": "#FF7518"
                 },
                 width=600, height=600,
                )
 
             v_fig.update_layout(
                 title="Male and Female Heights in Summer {}".format(year),
                 font=dict(
                      size=14,
                  ),
                 title_x = 0.5,
                 paper_bgcolor='rgba(0,0,0,0)',
                 plot_bgcolor='rgba(0,0,0,0)'
             )

             p_fig = px.pie(country_summ_year, values='ID', names='Medal', hole=.4, color="Medal",
               color_discrete_map={
                  "Gold": "#FFD700", "Silver": "#c0c0c0", "Bronze": " #b08d57"
                  },width=600, height=600)
 
             p_fig.update_layout(
                  title="Medals Won, Summer {}".format(year),
                  font=dict(
                      size=14,
                  ),
                  title_x = 0.5,
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)'
             )

 
           elif (country != None and year == None and sport == None):
             v_fig = px.violin(country_summer, y="Height", color="Sex",
                 violinmode='overlay',
                 hover_data=country_summer.columns,
                 color_discrete_map={
                   "F": "#FFD580", "M": "#FF7518"
                 },
                 width=600, height=600,
                )
 
             v_fig.update_layout(
                 title="Male and Female Heights, Summer",
                 font=dict(
                     size=14,
                 ),
                 title_x = 0.5,
                 paper_bgcolor='rgba(0,0,0,0)',
                 plot_bgcolor='rgba(0,0,0,0)'
             )

             p_fig = px.pie(country_summ, values='ID', names='Medal', hole=.4, color="Medal",
               color_discrete_map={
                  "Gold": "#FFD700", "Silver": "#c0c0c0", "Bronze": " #b08d57"
                  },width=600, height=600)
 
             p_fig.update_layout(
                  title="Medals Won, Summer",
                  font=dict(
                      size=14,
                  ),
                  title_x = 0.5,
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)'
              )

 
           else:
              raise ValueError("Incorrectly specified data")

     return html.Div(
                id="right-container",
                children=dcc.Loading(
                  className="graph-wrapper",
                  children=[dcc.Graph(id="right-graph-violin", figure=v_fig),
                            dcc.Graph(id="right-graph-pie", figure=p_fig)]
                 ),

            )



@app.callback(
             Output('stats-content','children'),
    inputs = [Input('countries-dropdown', 'value'),
              Input('year-dropdown', 'value'),
              Input('event-dropdown', 'value'),
              Input('summer-btn', 'n_clicks'),
              Input('winter-btn', 'n_clicks')
             ]
)
def getStats(country, year, sport, summerbtn, winterbtn):
     
     country_winter = df.query('Team == "{}" and Season == "Winter"'.format(country))
     country_summer = df.query('Team == "{}" and Season == "Summer"'.format(country))

    
     if (('summer-btn.n_clicks' in changes) and 'winter-btn.n_clicks' not in changes):
        # most repped
        athletes = country_summer.Name.value_counts().to_frame()
        athletes = athletes.rename(columns={'Name': 'reps'})
        athlete_df = country_summer.query("""Name == '{}'""".format(athletes.index[0])).reset_index()
        games_athlete = athlete_df.groupby(['Games']).count()
        mr_ath = {"athlete": athletes.index[0], "Sex": athlete_df.Sex[0],  "reps": athletes.reps[0], "Games": games_athlete.index.values}

        # most decorated
        country_sum_med = country_summer[~country_summer['Medal'].isnull()]
 
        decorated = country_sum_med.Name.value_counts().to_frame()
        decorated = decorated.rename(columns={'Name':'Dec'})
        dec_df = country_summer.query("""Name == '{}'""".format(decorated.index[0]))
        dec_df_gold = dec_df[dec_df.Medal == "Gold"]
        dec_df_sil = dec_df[dec_df.Medal == "Silver"]
        dec_df_br = dec_df[dec_df.Medal == "Bronze"]
        dec_gold = len(dec_df_gold)
        dec_silver = len(dec_df_sil)
        dec_bronze = len(dec_df_br)
        md_ath = {"athlete": decorated.index[0], "decs": decorated.Dec[0], "gold": dec_gold, "silver": dec_silver, "bronze": dec_bronze}

        if (country != None and year != None):
            # most participated event
            country_summer_year = country_summer.query('Year == {}'.format(year))
            country_ev = country_summer_year.groupby('Event').count().sort_values(by=['ID'], ascending=False)
            mp_ev = {"event": country_ev.index[0], "participation": country_ev.Name[0]}

            # most won event
            country_sum_med_yr = country_summer_year[~country_summer_year['Medal'].isnull()]
            country_won = country_sum_med_yr.Event.value_counts().to_frame()
            country_won = country_won.rename(columns={"Event": "Won"})
            mw_ev = {"event": country_won.index[0], "won": country_won.Won[0]}
        
        else:
             # most participated event
             country_ev = country_summer.groupby('Event').count().sort_values(by=['ID'], ascending=False)
             mp_ev = {"event": country_ev.index[0], "participation": country_ev.Name[0]}

             # most won event 
             country_won = country_sum_med.Event.value_counts().to_frame()
             country_won = country_won.rename(columns={"Event": "Won"})
             mw_ev = {"event": country_won.index[0], "won": country_won.Won[0]}

     elif (('winter-btn.n_clicks' in changes)):  
         # most repped
         athletes = country_winter.Name.value_counts().to_frame()
         athletes = athletes.rename(columns={'Name': 'reps'})
         athlete_df = country_winter.query("""Name == '{}'""".format(athletes.index[0])).reset_index()
         games_athlete = athlete_df.groupby(['Games']).count()
         mr_ath = {"athlete": athletes.index[0], "Sex": athlete_df.Sex[0],  "reps": athletes.reps[0], "Games": games_athlete.index.values}
 
         # most decorated
         country_win_med = country_winter[~country_winter['Medal'].isnull()]
         decorated = country_win_med.Name.value_counts().to_frame()
         decorated = decorated.rename(columns={'Name':'Dec'})
         dec_df = country_winter.query("""Name == '{}'""".format(decorated.index[0]))
         dec_df_gold = dec_df[dec_df.Medal == "Gold"]
         dec_df_sil = dec_df[dec_df.Medal == "Silver"]
         dec_df_br = dec_df[dec_df.Medal == "Bronze"]
         dec_gold = len(dec_df_gold)
         dec_silver = len(dec_df_sil)
         dec_bronze = len(dec_df_br)
         md_ath = {"athlete": decorated.index[0], "decs": decorated.Dec[0], "gold": dec_gold, "silver": dec_silver, "bronze": dec_bronze}

         if (country != None and year != None):
             # most participated event
             country_winter_year = country_winter.query('Year == {}'.format(year))
             country_ev = country_winter_year.groupby('Event').count().sort_values(by=['ID'], ascending=False)
             mp_ev = {"event": country_ev.index[0], "participation": country_ev.Name[0]}
 
             # most won event
             country_win_med_yr = country_winter_year[~country_winter_year['Medal'].isnull()]
             country_won = country_win_med_yr.Event.value_counts().to_frame()
             country_won = country_won.rename(columns={"Event": "Won"})
             mw_ev = {"event": country_won.index[0], "won": country_won.Won[0]}
 
         else:
              # most participated event
              country_ev = country_winter.groupby('Event').count().sort_values(by=['ID'], ascending=False)
              mp_ev = {"event": country_ev.index[0], "participation": country_ev.Name[0]}
 
              # most won event 
              country_won = country_win_med.Event.value_counts().to_frame()
              country_won = country_won.rename(columns={"Event": "Won"})
              mw_ev = {"event": country_won.index[0], "won": country_won.Won[0]}
       
     else:
       if (changes[-1:] == ["winter-btn.n_clicks"] or ["year-dropdown.value"] or ["event-dropdown.value"]):
          # most repped
          athletes = country_winter.Name.value_counts().to_frame()
          athletes = athletes.rename(columns={'Name': 'reps'})
          athlete_df = country_winter.query("""Name == '{}'""".format(athletes.index[0])).reset_index()
          games_athlete = athlete_df.groupby(['Games']).count()
          mr_ath = {"athlete": athletes.index[0], "Sex": athlete_df.Sex[0],  "reps": athletes.reps[0], "Games": games_athlete.index.values}
 
          # most decorated
          country_win_med = country_winter[~country_winter['Medal'].isnull()]
          decorated = country_win_med.Name.value_counts().to_frame()
          decorated = decorated.rename(columns={'Name':'Dec'})
          dec_df = country_winter.query("""Name == '{}'""".format(decorated.index[0]))
          dec_df_gold = dec_df[dec_df.Medal == "Gold"]
          dec_df_sil = dec_df[dec_df.Medal == "Silver"]
          dec_df_br = dec_df[dec_df.Medal == "Bronze"]
          dec_gold = len(dec_df_gold)
          dec_silver = len(dec_df_sil)
          dec_bronze = len(dec_df_br)
          md_ath = {"athlete": decorated.index[0], "decs": decorated.Dec[0], "gold": dec_gold, "silver": dec_silver, "bronze": dec_bronze}
 
          if (country != None and year != None):
              # most participated event
              country_winter_year = country_winter.query('Year == {}'.format(year))
              country_ev = country_winter_year.groupby('Event').count().sort_values(by=['ID'], ascending=False)
              mp_ev = {"event": country_ev.index[0], "participation": country_ev.Name[0]}
 
              # most won event
              country_win_med_yr = country_winter_year[~country_winter_year['Medal'].isnull()]
              country_won = country_win_med_yr.Event.value_counts().to_frame()
              country_won = country_won.rename(columns={"Event": "Won"})
              mw_ev = {"event": country_won.index[0], "won": country_won.Won[0]}
 
          else:
               # most participated event
               country_ev = country_winter.groupby('Event').count().sort_values(by=['ID'], ascending=False)
               mp_ev = {"event": country_ev.index[0], "participation": country_ev.Name[0]}
 
               # most won event 
               country_won = country_win_med.Event.value_counts().to_frame()
               country_won = country_won.rename(columns={"Event": "Won"})
               mw_ev = {"event": country_won.index[0], "won": country_won.Won[0]}
   
       else:
            # most repped
            athletes = country_summer.Name.value_counts().to_frame()
            athletes = athletes.rename(columns={'Name': 'reps'})
            athlete_df = country_summer.query("""Name == '{}'""".format(athletes.index[0])).reset_index()
            games_athlete = athlete_df.groupby(['Games']).count()
            mr_ath = {"athlete": athletes.index[0], "Sex": athlete_df.Sex[0],  "reps": athletes.reps[0], "Games": games_athlete.index.values}
    
            # most decorated
            country_sum_med = country_summer[~country_summer['Medal'].isnull()]
            decorated = country_sum_med.Name.value_counts().to_frame()
            decorated = decorated.rename(columns={'Name':'Dec'})
            dec_df = country_summer.query("""Name == '{}'""".format(decorated.index[1]))
            dec_df_gold = dec_df[dec_df.Medal == "Gold"]
            dec_df_sil = dec_df[dec_df.Medal == "Silver"]
            dec_df_br = dec_df[dec_df.Medal == "Bronze"]
            dec_gold = len(dec_df_gold)
            dec_silver = len(dec_df_sil)
            dec_bronze = len(dec_df_br)
            md_ath = {"athlete": decorated.index[0], "decs": decorated.Dec[0], "gold": dec_gold, "silver": dec_silver, "bronze": dec_bronze}
    
            if (country != None and year != None):
                # most participated event
                country_summer_year = country_summer.query('0Year == {}'.format(year))
                country_ev = country_summer_year.groupby('Event').count().sort_values(by=['ID'], ascending=False)
                mp_ev = {"event": country_ev.index[0], "participation": country_ev.Name[0]}
    
                # most won event
                country_sum_med_yr = country_summer_year[~country_summer_year['Medal'].isnull()]
                country_won = country_sum_med_yr.Event.value_counts().to_frame()
                country_won = country_won.rename(columns={"Event": "Won"})
                mw_ev = {"event": country_won.index[0], "won": country_won.Won[0]}
    
            else:
                 # most participated event
                 country_ev = country_summer.groupby('Event').count().sort_values(by=['ID'], ascending=False)
                 mp_ev = {"event": country_ev.index[0], "participation": country_ev.Name[0]}
    
                 # most won event 
                 country_won = country_sum_med.Event.value_counts().to_frame()
                 country_won = country_won.rename(columns={"Event": "Won"})
                 mw_ev = {"event": country_won.index[0], "won": country_won.Won[0]}
    
     return [html.Div(
            id="stats-inner",
            children = [
                html.Section(
                    id="rep-stats-card-sec",
                    children = [
                        html.H2("Most Participations: " + mr_ath['athlete']),
                        html.H5("Representations: " + str(mr_ath['reps'])),
                        html.P(mr_ath['Sex'])
                    ]
                ),
                html.Section(
                    id="dec-stats-card",
                    children = [
                        html.H2("Most Decorated Athlete: " + md_ath['athlete']),
                        html.H5("Medals: " + str(md_ath['decs'])),
                    ]
                ),
                html.Section(
                    id="ev-part-stats-card-sec",
                    children = [
                        html.H2("Most Participated Event: " + mp_ev['event']),
                        html.H5("Participation: " + str(mp_ev['participation']))
                    ]
                ),
                html.Section(
                    id="ev-won-stats-card-sec",
                    children = [
                        html.H2(mw_ev['event']),
                        html.H5("Most Won Event: " + str(mw_ev['won']))
                    ]
                ),
            ]
            )]


if __name__ == '__main__':
    app.run_server(debug=True)
