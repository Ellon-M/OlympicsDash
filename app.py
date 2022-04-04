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
                        html.Div(
                            id="buttons-wrap",
                            children = [
                                html.Button("Summer", 
                                    id="summer-btn",
                                    n_clicks=0),
                                html.Button("Winter",
                                    id="winter-btn",
                                    n_clicks=0)
                            ]
                        )
                    ]
                ),
                html.Div(
                    id="top-sec",
                    children = [
                        html.Div(
                            id="left-col",
                            children = [
                                html.Div(
                                    id="top-left-col",
                                ),
                                html.Div(
                                    id="flag-wrap",
                                ),
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
                                                "value": "United States"},
                                                {"label": "France",
                                                 "value": "France"},
                                                {"label": "Italy",
                                                 "value": "Italy"},
                                                 {"label": "Japan",
                                                 "value": "Japan"},
                                                 {"label": "Sweden",
                                                 "value": "Sweden"},
                                                 {"label": "Russia",
                                                 "value": "Russia"},
                                                 {"label": "Great Britain",
                                                 "value": "Great Britain"},
                                                 {"label": "Germany",
                                                 "value": "Germany"},
                                                 {"label": "China",
                                                 "value": "China"},
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
                    ]
                ),
                html.Div(
                    id="right-graph-content"
                        ),
                html.Div(
                    id="stats-content"
                        ),
                html.Div(
                    id="footer",
                    children = [
                        dcc.Link(
                            "Source",
                            href="#",
                            id="footer-link"
                        ),
                        html.P(
                          "Ellon Ⓒ 2022",
                            id="footer-copyright"
                        )
                    ]
                )
                ]
)

changes = []

@app.callback(
       output = [Output('refresh-btn', 'children'),
                 Output('year-dropdown', 'options'),
                 Output('event-dropdown', 'options'),
                 Output('graph-content', 'children'),
                 Output('top-left-col', 'children')],
       inputs = [Input('countries-dropdown', 'value'),
                 Input('year-dropdown', 'value'),
                 Input('event-dropdown', 'value'),
                 Input('summer-btn', 'n_clicks'),
                 Input('winter-btn', 'n_clicks')
                 ]
    )
def display_graphs(country, year, sport, sumbtn, winbtn):
    
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
                                      font_family='Arial',
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
                                      font_family='Arial',
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
                                          title_text="Summer Events, {}".format(sport),
                                          paper_bgcolor='rgba(0,0,0,0)',
                                          plot_bgcolor='rgba(0,0,0,0)',
                                          font = dict(size=14),
                                          font_family='Arial',
                                           )


         elif (country != None and year == None and sport == None):
             country_summer_medals = country_summer[~country_summer['Medal'].isnull()]
             country_summer_medals_count = country_summer_medals.groupby(['Year']).count()['Medal'].to_frame().reset_index()
             
             main_fig = go.Figure(data=go.Scatter(
                             x = country_summer_medals_count['Year'],
                             y = country_summer_medals_count['Medal'],
                             mode='markers',
                             marker=dict(
                             size=20,
                             color= country_summer_medals_count['Medal'],
                             colorscale='Pinkyl',
                             showscale=True
                            )
                        ))  

             main_fig.update_layout(
                title_text="Summer Medal Count Over Time",
                title_x=0.5,
                title_y=0.8,
                xaxis_title="Years",
                yaxis_title="Medals",
                legend_title="Medal Count",
                font=dict(
                    size=14,
                ),
                font_family='Arial',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
             )
         else:
             pass
    
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
                                     font_family='Arial',
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
                                         font_family='Arial',
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
                                     font_family='Arial',
                                     )



        elif (country != None and year == None and sport == None):
             country_winter_medals = country_winter[~country_winter['Medal'].isnull()]
             country_winter_medals_count = country_winter_medals.groupby(['Year']).count()['Medal'].to_frame().reset_index()


             main_fig = go.Figure(data=go.Scatter(
                             x = country_winter_medals_count['Year'],
                             y = country_winter_medals_count['Medal'],
                             mode='markers',
                             marker=dict(
                             size=20,
                             color= country_winter_medals_count['Medal'],
                             colorscale='Purp',
                             showscale=True
                            )
             ))


             main_fig.update_layout(
                title_text="Winter Medal Count Over Time",
                title_x=0.5,
                title_y=0.8,
                xaxis_title="Years",
                yaxis_title="Medals",
                legend_title="Medal Count",
                font=dict(
                    size=14,
                ),
                font_family='Arial',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
             )
        else:
             pass

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
                                    font_family='Arial',
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
                                    font_family='Arial',
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
                                        font_family='Arial',
                                        )


             else:
                country_winter_medals = country_winter[~country_winter['Medal'].isnull()]
                country_winter_medals_count = country_winter_medals.groupby(['Year']).count()['Medal'].to_frame().reset_index()


                main_fig = go.Figure(data=go.Scatter(
                             x = country_winter_medals_count['Year'],
                             y = country_winter_medals_count['Medal'],
                             mode='markers',
                             marker=dict(
                             size=20,
                             color= country_winter_medals_count['Medal'],
                             colorscale='Purp',
                             showscale=True
                            )
                ))

                main_fig.update_layout(
                    title_text="Winter Medal Count Over Time",
                    title_x=0.5,
                    title_y=0.8,
                    xaxis_title="Years",
                    yaxis_title="Medals",
                    legend_title="Medal Count",
                    font=dict(
                        size=14,
                    ),
                    font_family='Arial',
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
                                     font_family='Arial',
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
                                     font_family='Arial',
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
                                         font_family='Arial',
                                         )




            elif (country != None and year == None and sport == None):
                 country_summer_medals = country_summer[~country_summer['Medal'].isnull()]
                 country_summer_medals_count = country_summer_medals.groupby(['Year']).count()['Medal'].to_frame().reset_index()

                 main_fig = go.Figure(data=go.Scatter(
                             x = country_summer_medals_count['Year'],
                             y = country_summer_medals_count['Medal'],
                             mode='markers',
                             marker=dict(
                             size=20,
                             color= country_summer_medals_count['Medal'],
                             colorscale='Pinkyl',
                             showscale=True
                            )
                        ))

                 main_fig.update_layout(
                    title_text="Summer Medal Count Over Time",
                    title_x=0.5,
                    title_y=0.8,
                    xaxis_title="Years",
                    yaxis_title="Medals",
                    legend_title="Medal Count",
                    font=dict(
                        size=14,
                    ),
                    font_family='Arial',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
            else:
                 pass

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
            html.H4(
                country,
                id="country-left-col"
            )

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
def get_right_graphs(country, year, sport, summerbtn, winterbtn):

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
                width=500, height=500,
               )

            v_fig.update_layout(
                title="Male and Female Heights in Summer {}".format(year),
                font=dict(
                    size=14,
                 ),
                font_family='Arial',
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
                font_family='Arial',
                title_x = 0.5,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                width=500, height=500
            )
        elif (country !=None and sport != None):
            v_fig = px.violin(country_summer, y="Height", color="Sex",
                violinmode='overlay',
                hover_data=country_summer.columns,
                color_discrete_map={
                    "F": "#FFD580", "M": "#FF7518"
                },
                width=500, height=500,
               )

            v_fig.update_layout(
                title="Male and Female Heights, Summer",
                font=dict(
                    size=14,
                ),
                font_family='Arial',
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
                font_family='Arial',
                title_x = 0.5,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                width=500, height=500
            )

        elif (country != None and year == None and sport == None):
            v_fig = px.violin(country_summer, y="Height", color="Sex",
                violinmode='overlay',
                hover_data=country_summer.columns,
                color_discrete_map={
                    "F": "#FFD580", "M": "#FF7518"
                },
                width=500, height=500,
               )

            v_fig.update_layout(
                title="Male and Female Heights, Summer",
                font=dict(
                    size=14,
                ),
                font_family='Arial',
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
                font_family='Arial',
                title_x = 0.5,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                width=500, height=500
            )


        else:
             #raise ValueError("Incorrectly specified data")
             pass

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
                 width=500, height=500,
                )
 
             v_fig.update_layout(
                 title="Male and Female Heights in Winter {}".format(year),
                 font=dict(
                     size=14,
                  ),
                 font_family='Arial',
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
                font_family='Arial',
                title_x = 0.5,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                width=500, height=500

             )
        
         elif (country != None and sport != None):
             v_fig = px.violin(country_winter, y="Height", color="Sex",
                 violinmode='overlay',
                 hover_data=country_winter.columns,
                 color_discrete_map={
                 "F": "#ff6fff", "M": "#c84186"
                 },
                 width=500, height=500,
                )
 
             v_fig.update_layout(
                 title="Male and Female Heights, Winter",
                 font=dict(
                     size=14,
                 ),
                 font_family='Arial',
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
                font_family='Arial',
                title_x = 0.5,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                width=500, height=500
            )
 
         elif (country != None and year == None and sport == None):
             v_fig = px.violin(country_winter, y="Height", color="Sex",
                 violinmode='overlay',
                 hover_data=country_winter.columns,
                 color_discrete_map={
                 "F": "#ff6fff", "M": "#c84186"
                 },
                 width=500, height=500,
                )
 
             v_fig.update_layout(
                 title="Male and Female Heights, Winter",
                 font=dict(
                     size=14,
                 ),
                 font_family='Arial',
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
                font_family='Arial',
                title_x = 0.5,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                width=500, height=500
            )

 
         else:
              #raise ValueError("Incorrectly specified data")
              pass

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
                  width=500, height=500,
                 )
 
              v_fig.update_layout(
                  title="Male and Female Heights in Winter {}".format(year),
                  font=dict(
                      size=14,
                   ),
                  font_family='Arial',
                  title_x = 0.5,
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)'
              )

              p_fig = px.pie(country_wint_year, values='ID', names='Medal', hole=.4, color="Medal",
                    color_discrete_map={
                        "Gold": "#FFD700", "Silver": "#c0c0c0", "Bronze": " #b08d57"
                    },width=500, height=500)
 
              p_fig.update_layout(
                  title="Medals Won, Winter {}".format(year),
                  font=dict(
                      size=14,
                  ),
                  font_family='Arial',
                  title_x = 0.5,
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
               )


          elif (country != None and year != None):
              v_fig = px.violin(country_winter, y="Height", color="Sex",
                   violinmode='overlay',
                   hover_data=country_winter.columns,
                   color_discrete_map={
                     "F": "#ff6fff", "M": "#c84186"
                  },
                   width=500, height=500,
                 )
 
              v_fig.update_layout(
                   title="Male and Female Heights, Winter",
                   font=dict(
                      size=14,
                   ),
                   font_family='Arial',
                   title_x = 0.5,
                   paper_bgcolor='rgba(0,0,0,0)',
                   plot_bgcolor='rgba(0,0,0,0)'
                )

              p_fig = px.pie(country_wint, values='ID', names='Medal', hole=.4, color="Medal",
                      color_discrete_map={
                          "Gold": "#FFD700", "Silver": "#c0c0c0", "Bronze": " #b08d57"
                      },width=500, height=500)
 
              p_fig.update_layout(
                    title="Medals Won, Winter",
                    font=dict(
                        size=14,
                    ),
                    font_family='Arial',
                    title_x = 0.5,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
              )

          elif (country != None and sport != None):
             v_fig = px.violin(country_winter, y="Height", color="Sex",
                   violinmode='overlay',
                   hover_data=country_winter.columns,
                   color_discrete_map={
                     "F": "#ff6fff", "M": "#c84186"
                  },
                   width=500, height=500,
                 )
 
             v_fig.update_layout(
                   title="Male and Female Heights, Winter",
                   font=dict(
                      size=14,
                   ),
                   font_family='Arial',
                   title_x = 0.5,
                   paper_bgcolor='rgba(0,0,0,0)',
                   plot_bgcolor='rgba(0,0,0,0)'
                )

             p_fig = px.pie(country_wint, values='ID', names='Medal', hole=.4, color="Medal",
                      color_discrete_map={
                          "Gold": "#FFD700", "Silver": "#c0c0c0", "Bronze": " #b08d57"
                      },width=500, height=500)
 
             p_fig.update_layout(
                    title="Medals Won, Winter",
                    font=dict(
                        size=14,
                    ),
                    font_family='Arial',
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
                   width=500, height=500,
                 )
 
                v_fig.update_layout(
                   title="Male and Female Heights, Winter",
                   font=dict(
                      size=14,
                   ),
                   font_family='Arial',
                   title_x = 0.5,
                   paper_bgcolor='rgba(0,0,0,0)',
                   plot_bgcolor='rgba(0,0,0,0)'
                )

                p_fig = px.pie(country_wint, values='ID', names='Medal', hole=.4, color="Medal",
                      color_discrete_map={
                          "Gold": "#FFD700", "Silver": "#c0c0c0", "Bronze": " #b08d57"
                      },width=500, height=500)
 
                p_fig.update_layout(
                    title="Medals Won, Winter",
                    font=dict(
                        size=14,
                    ),
                    font_family='Arial',
                    title_x = 0.5,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )

 
          else:
              # raise ValueError("Incorrectly specified data")
              pass
        
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
                 width=500, height=500,
                )
 
             v_fig.update_layout(
                 title="Male and Female Heights in Summer {}".format(year),
                 font=dict(
                      size=14,
                  ),
                 font_family='Arial',
                 title_x = 0.5,
                 paper_bgcolor='rgba(0,0,0,0)',
                 plot_bgcolor='rgba(0,0,0,0)'
             )

             p_fig = px.pie(country_summ_year, values='ID', names='Medal', hole=.4, color="Medal",
               color_discrete_map={
                  "Gold": "#FFD700", "Silver": "#c0c0c0", "Bronze": " #b08d57"
                  },width=500, height=500)
 
             p_fig.update_layout(
                  title="Medals Won, Summer {}".format(year),
                  font=dict(
                      size=14,
                  ),
                  font_family='Arial',
                  title_x = 0.5,
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)'
             )

            
           elif (country != None and sport != None):
              v_fig = px.violin(country_summer, y="Height", color="Sex",
                 violinmode='overlay',
                 hover_data=country_summer.columns,
                 color_discrete_map={
                   "F": "#FFD580", "M": "#FF7518"
                 },
                 width=500, height=500,
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
                  },width=500, height=500)
 
              p_fig.update_layout(
                  title="Medals Won, Summer",
                  font=dict(
                      size=14,
                  ),
                  font_family='Arial',
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
                 width=500, height=500,
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
                  },width=500, height=500)
 
             p_fig.update_layout(
                  title="Medals Won, Summer",
                  font=dict(
                      size=14,
                  ),
                  font_family='Arial',
                  title_x = 0.5,
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)'
              )

 
           else:
              #raise ValueError("Incorrectly specified data")
              pass

     return [html.Div(
                id="right-container-violin",
                children=dcc.Loading(
                  className="graph-wrapper",
                  children=[dcc.Graph(id="right-graph-violin", figure=v_fig),
                           ]
                 ),
            ),
            html.Div(
                id="right-container-pie",
                children=dcc.Loading(
                    className="graph-wrapper",
                    children=[dcc.Graph(id="right-graph-pie", figure=p_fig)]
                ),
            )]




@app.callback(
             Output('stats-content','children'),
    inputs = [Input('countries-dropdown', 'value'),
              Input('year-dropdown', 'value'),
              Input('event-dropdown', 'value'),
              Input('summer-btn', 'n_clicks'),
              Input('winter-btn', 'n_clicks')
             ]
)
def get_stats(country, year, sport, summerbtn, winterbtn):
     
     country_winter = df.query('Team == "{}" and Season == "Winter"'.format(country))
     country_summer = df.query('Team == "{}" and Season == "Summer"'.format(country))

    
     if (('summer-btn.n_clicks' in changes) and 'winter-btn.n_clicks' not in changes):
        # styles
        bg_color_rep = "#ede6b4"
        filter_rep = "#e8db7b"
        bg_color_dec = "#ffd494"
        filter_dec = "#ffc266"
        bg_color_ev_part = "#fffd8f"
        filter_ev_part = "#fffc6e"
        bg_color_ev_won = "#ffbea6"
        filter_ev_won = "#fa9069"

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
         # styles
         bg_color_rep = "#a7a7cf"
         filter_rep = ""
         bg_color_dec = "#ffbfd4"
         filter_dec = ""
         bg_color_ev_part = "#7fbedb"
         filter_ev_part = ""
         bg_color_ev_won = "#d9baff"
         filter_ev_won = ""



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
          # styles
          bg_color_rep = "#a7a7cf"
          filter_rep = ""
          bg_color_dec = "#ffbfd4"
          filter_dec = ""
          bg_color_ev_part = "#7fbedb"
          filter_ev_part = ""
          bg_color_ev_won = "#d9baff"
          filter_ev_won = ""

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
            # styles
            bg_color_rep = "#ede6b4"
            filter_rep = "#e8db7b"
            bg_color_dec = "#ffd494"
            filter_dec = "#ffc266"
            bg_color_ev_part = "#fffd8f"
            filter_ev_part = "#fffc6e"
            bg_color_ev_won = "#ffbea6"
            filter_ev_won = "#fa9069"


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
                    style={'backgroundColor': bg_color_rep},
                    children = [
                        html.P("Most Participations:(All Games)"),
                        html.Div(
                            className="bottom-stats",
                            children = [
                                html.H4(mr_ath['athlete'], id="bottom-stats-left-1"),
                                html.H4(str(mr_ath['reps']), id="bottom-stats-right-1"),
                            ]
                        )
                    ]
                ),
                html.Section(
                    id="dec-stats-card",
                    style={'backgroundColor': bg_color_dec},
                    children = [
                        html.P("Most Decorated Athlete:(All Games)"),
                        html.Div(
                            className="bottom-stats",
                            children = [   
                                html.H4(md_ath['athlete'], id="bottom-stats-left-2",),
                                html.H4(str(md_ath['decs']), id="bottom-stats-right-2",)
                            ]
                        )
                    ]
                ),
                html.Section(
                    id="ev-part-stats-card-sec",
                    style={'backgroundColor': bg_color_ev_part},
                    children = [
                        html.P("Most Participated Event, " + str(year) + ":" if year else "Most Participated Event" + ":"), 
                        html.Div(
                            className="bottom-stats",
                            children = [
                                html.H4(mp_ev['event'], id="bottom-stats-left-3"),
                                html.H4(str(mp_ev['participation']), id="bottom-stats-right-3")
                            ]
                        )
                    ]
                ),
                html.Section(
                    id="ev-won-stats-card-sec",
                    style={'backgroundColor': bg_color_ev_won},
                    children = [
                        html.P("Most Won Event, " + str(year) + ":" if year else "Most Won Event" + ":"),
                        html.Div(
                            className="bottom-stats",
                            children = [
                                html.H4(mw_ev['event'], id="bottom-stats-left-4"),
                                html.H5(str(mw_ev['won']), id="bottom-stats-right-4")
                            ]
                        )
                    ]
                ),
            ]
            )]


@app.callback(
    output = [Output('left-col', 'style'),
               Output('summer-btn', 'style'),
               Output('winter-btn', 'style')],
    inputs = [Input('summer-btn', 'n_clicks'),
              Input('winter-btn', 'n_clicks')]
)
def get_theme(summer_btn, winter_btn):
     if (('summer-btn.n_clicks' in changes) and 'winter-btn.n_clicks' not in changes):
         bg_left_col = "#fff8db"
         bg_summer_btn = "#fff8db"
         bg_winter_btn = "transparent"
     
     elif (('winter-btn.n_clicks' in changes)):
         bg_left_col = "#d9f3ff"
         bg_summer_btn = "transparent"
         bg_winter_btn = "#d9f3ff"
     else:
        if (changes[-1:] == ["winter-btn.n_clicks"] or ["year-dropdown.value"] or ["event-dropdown.value"]):
            bg_left_col = "#d9f3ff"
            bg_summer_btn = "transparent"
            bg_winter_btn = "#d9f3ff"
        else:
            bg_left_col = "#fff8db"
            bg_summer_btn = "#fff8db"
            bg_winter_btn = "transparent"
        
     return [ 
         {'backgroundColor': bg_left_col},
         {'backgroundColor': bg_summer_btn},
         {'backgroundColor': bg_winter_btn}
     ]


@app.callback(
    Output('flag-wrap', 'children'),
    Input('countries-dropdown', 'value')
)
def get_flags(country):
    if country == 'United States':
        flag = 'https://res.cloudinary.com/denphvygd/image/upload/v1649079182/olympicsdash/United.jpg'

    elif country == 'Canada':
        flag = 'https://res.cloudinary.com/denphvygd/image/upload/v1649079181/olympicsdash/Flag-Canada_ley2ci.webp'

    elif country == 'Italy':
        flag = 'https://res.cloudinary.com/denphvygd/image/upload/v1649079180/olympicsdash/italian_flag_colors-300x200_vcgxi9.webp'

    elif country == 'Russia':
        flag = 'https://res.cloudinary.com/denphvygd/image/upload/v1649079181/olympicsdash/Flag-Russia_npxqmb.jpg'

    elif country == 'Japan':
        flag = 'https://res.cloudinary.com/denphvygd/image/upload/v1649079180/olympicsdash/800px-Flag_of_Japan.svg_nhd1iy.png'

    elif country == 'Germany':
        flag = 'https://res.cloudinary.com/denphvygd/image/upload/v1649079180/olympicsdash/1200px-Flag_of_Germany.svg_fjl8xt.webp'

    elif country == 'Great Britain':
        flag = 'https://res.cloudinary.com/denphvygd/image/upload/v1649079180/olympicsdash/1200px-Flag_of_the_United_Kingdom.svg_dlsoqx.webp'        

    elif country == 'Sweden':
        flag = 'https://res.cloudinary.com/denphvygd/image/upload/v1649079180/olympicsdash/2560px-Flag_of_Sweden.svg_eoqlv0.png'

    elif country == 'China':
        flag = 'https://res.cloudinary.com/denphvygd/image/upload/v1649079181/olympicsdash/Flag-China_fs95w0.webp'

    elif country == 'France':
        flag = 'https://res.cloudinary.com/denphvygd/image/upload/v1649079181/olympicsdash/Flag-France_mgfqtk.jpg'

    else:
        pass

    return html.Img(
        src=flag,
        width=75,
        height=50,
        style={'borderRadius': '75px',
               'textAlign': 'center',
                'marginBottom': '6vh',
                'float': 'right'}
        )



if __name__ == '__main__':
    app.run_server(debug=False)
