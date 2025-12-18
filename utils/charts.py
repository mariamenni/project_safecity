import plotly.express as px

def map_choropleth(gdf_filtered):
    geojson = gdf_filtered.__geo_interface__

    fig = px.choropleth_mapbox(
        gdf_filtered,
        geojson=geojson,
        locations=gdf_filtered.index,
        color="taux_pour_100k",
        hover_name="nom",
        hover_data={
            "nombre": True,
            "population": True,
            "taux_pour_100k": True
        },
        color_continuous_scale="Reds",
        mapbox_style="carto-positron",
        zoom=4.0,                
        center={"lat": 46.5, "lon": 2.0},  
        opacity=0.7
    )

    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        coloraxis_colorbar=dict(
            title="Taux / 100k",
            ticks="outside"
        )
    )

    return fig

def evolution_nationale(df_history, delit):
    df_time = df_history.groupby("annee", as_index=False)["taux_pour_100k"].mean()
    fig = px.line(
        df_time,
        x="annee",
        y="taux_pour_100k",
        markers=True,
        color_discrete_sequence=["#FF4B4B"],
        title=f"Tendance nationale — {delit}"
    )
    fig.update_layout(xaxis_title="Année", yaxis_title="Taux / 100k")
    return fig

def comparateur_territorial(df_comp):
    df_comp = df_comp.sort_values(["nom", "annee"])
    df_comp["evolution_%"] = df_comp.groupby("nom")["taux_pour_100k"].pct_change() * 100
    fig = px.line(
        df_comp,
        x="annee",
        y="taux_pour_100k",
        color="nom",
        markers=True,
        title="Comparaison territoriale"
    )
    fig.update_layout(xaxis_title="Année", yaxis_title="Taux / 100k")
    return fig

def top5_departements(gdf_filtered):
    top5 = gdf_filtered.nlargest(5, "taux_pour_100k").sort_values("taux_pour_100k", ascending=True)
    fig = px.bar(
        top5,
        x="taux_pour_100k",
        y="nom",
        orientation='h',
        text="taux_pour_100k"
    )
    fig.update_traces(texttemplate='%{text:.1f}')
    fig.update_layout(xaxis_title="Taux / 100k", yaxis_title="Département")
    return fig
