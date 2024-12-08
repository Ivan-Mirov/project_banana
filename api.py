import io

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import plotly

import plotly.graph_objs as go

import plotly.express as px

from plotly.subplots import make_subplots



import numpy as np
# Load dataset
df = pd.read_csv("banana_quality_dataset.csv")

# Initialize FastAPI
app = FastAPI()

# Data model for POST request
class NewEntry(BaseModel):
    country: str
    type: str
    quality_category: str
    ripeness_index: float

@app.get("/get_df")
def get_df():
    result = df.head(10)
    return result.to_dict()

@app.get("/mean")
def get_df():
    result = df[['quality_score', 'length_cm', 'rainfall_mm']].mean()
    return result.to_dict()

@app.get("/median")
def get_df():
    result = df[['quality_score', 'length_cm', 'rainfall_mm']].median()
    return result.to_dict()

@app.get("/std")
def get_df():
    result = df[['quality_score', 'length_cm', 'rainfall_mm']].std()
    return result.to_dict()

@app.get("/info")
def get_df():
    buffer = io.StringIO()
    df.info(buf=buffer)
    return buffer.getvalue()

@app.get("/nan")
def get_df():
    result = df.isnull().sum()
    return result.to_dict()

@app.get("/box1")
def get_df():
    fig = go.Figure()
    fig.add_trace(go.Box(y=df['quality_score'], marker_color='#FECB52'))
    fig.add_trace(go.Box(y=df['ripeness_index'], marker_color='#FBE426'))

    return JSONResponse(content=fig.to_json())

@app.get("/analys1")
def get_df():
    result = df[df['quality_score'] < 1.2]
    return result.to_dict()

@app.get("/change")
def get_df():
    df['quality_number'] = df['quality_category'].map({'Unripe': 1, 'Processing': 2, 'Good': 3, 'Premium': 4})
    df['sugar_g'] = (df['sugar_content_brix'] / 100) * df['weight_g']
    return df.to_dict()

@app.get("/corr1")
def get_df():
    res = df[['quality_score','ripeness_index','sugar_content_brix','firmness_kgf','length_cm','weight_g','tree_age_years','altitude_m','rainfall_mm','soil_nitrogen_ppm', 'quality_number', 'sugar_g']].corr()
    return res.to_dict()

@app.get("/analys2")
def get_df():
    result = df[['quality_score','ripeness_index','sugar_content_brix','firmness_kgf','length_cm','weight_g','tree_age_years','altitude_m','rainfall_mm','soil_nitrogen_ppm']].corr()
    return result.to_dict()
@app.get("/data3")
def get_df():
    result = df[['quality_score','ripeness_index','sugar_content_brix','firmness_kgf','length_cm','weight_g','tree_age_years','altitude_m','rainfall_mm','soil_nitrogen_ppm']].corr()
    return result.to_dict()

@app.get("/diff_plot")
def get_df():
    df_var = df[['variety', 'quality_score']]
    df_var_c = df_var.groupby(['variety']).agg(amount=('quality_score', 'count'))
    var = list(df_var_c.index)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=var,
        y=df_var_c['amount'],
        name='amount of bananas',
        marker_color='#FBE426'
    ))

    fig.update_layout(barmode='group')
    return JSONResponse(content=fig.to_json())

@app.get("/hypo")
def get_df():
    fig = px.scatter_3d(df, x='ripeness_index', y='sugar_content_brix', z='quality_number', color='quality_category',
                        category_orders={"quality_category": ["Premium", "Good", "Processing", "Unripe"]})
    #   color='quality_category'

    return JSONResponse(content=fig.to_json())

@app.get("/hypo2")
def get_df():
    fig = px.scatter(df, x="ripeness_index", y="sugar_content_brix", color='quality_category',
                     category_orders={"quality_category": ["Premium", "Good", "Processing", "Unripe"]})

    return JSONResponse(content=fig.to_json())

@app.get("/diff_plot2")
def get_df():
    df_reg = df[['region', 'quality_score']]
    df_reg_c = df_reg.groupby(['region']).agg(amount = ('quality_score', 'count'))
    reg = list(df_reg_c.index)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=reg,
        y=df_reg_c['amount'],
        name='amount of bananas',
        marker_color='#FBE426'
    ))

    fig.update_layout(barmode='group')
    return JSONResponse(content=fig.to_json())


@app.get("/boxx2")
def get_df():
    df_regq = df.groupby(['region', 'quality_category'], as_index=False).agg(amount=('quality_score', 'count'))
    fig = px.bar(df_regq, x='region', y='amount', color='quality_category', barmode='group',
                 category_orders={'quality_category': ['Unripe', 'Processing', 'Good', 'Premium']})

    return JSONResponse(content=fig.to_json())

@app.get("/boxx3")
def get_df():
    df_varq = df.groupby(['variety', 'quality_category'], as_index=False).agg(amount=('quality_score', 'count'))
    fig = px.bar(df_varq, x='variety', y='amount', color='quality_category', barmode='group',
                 category_orders={'quality_category': ['Unripe', 'Processing', 'Good', 'Premium']})
    return JSONResponse(content=fig.to_json())

@app.get("/scatter")
def get_df():
    fig = px.scatter(df, x="ripeness_index", y="quality_score", color_discrete_sequence=['#FECB52'])
    return JSONResponse(content=fig.to_json())

@app.get("/scatter2")
def get_df():
    fig = px.scatter(df, x="ripeness_index", y="quality_score", color='quality_category',
                     color_discrete_sequence=px.colors.sequential.deep,
                     category_orders={"quality_category": ["Premium", "Good", "Processing", "Unripe"]})

    return JSONResponse(content=fig.to_json())

@app.get("/scatter3")
def get_df():
    fig = px.scatter(df, x="sugar_content_brix", y="quality_score", color='quality_category')
    return JSONResponse(content=fig.to_json())

@app.get("/box2")
def get_df():
    fig = go.Figure()
    fig.add_trace(go.Box(y=df['firmness_kgf'], marker_color='#FECB52'))

    return JSONResponse(content=fig.to_json())


@app.get("/box3")
def get_df():
    fig = go.Figure()
    fig.add_trace(go.Box(y=df['sugar_content_brix'], marker_color='#FECB52'))
    fig.add_trace(go.Box(y=df['length_cm'], marker_color='#FBE426'))

    return JSONResponse(content=fig.to_json())


@app.get("/box4")
def get_df():
    fig = go.Figure()
    fig.add_trace(go.Box(y=df['weight_g'], marker_color='#FECB52'))
    fig.add_trace(go.Box(y=df['soil_nitrogen_ppm'], marker_color='#FBE426'))
    return JSONResponse(content=fig.to_json())


@app.get("/box5")
def get_df():
    fig = go.Figure()
    fig.add_trace(go.Box(y=df['tree_age_years'], marker_color='#FECB52'))
    return JSONResponse(content=fig.to_json())


@app.get("/box6")
def get_df():
    fig = go.Figure()
    fig.add_trace(go.Box(y=df['altitude_m'], marker_color='#FECB52'))
    fig.add_trace(go.Box(y=df['rainfall_mm'], marker_color='#FBE426'))
    return JSONResponse(content=fig.to_json())

@app.get("/hist")
def get_df():
    fig = go.Figure(data=[go.Histogram(x=df.length_cm, xbins=go.histogram.XBins(size=1), marker=dict(color='#FECB52'))])
    return JSONResponse(content=fig.to_json())

@app.get("/filter")
def query_data(country: str, type: str):# = Query(..., ge=0)):
    """
    Get entries filtered by city and minimum age.
    """
    result = df[(df["region"] == country) & (df["variety"] == type)]
    return df.fillna("").to_dict()#orient="records")

@app.post("/add")
def add_data(entry: NewEntry):
    """
    Add a new entry to the dataset.
    """
    global df
    #print("ASDF")
    new_id = df["sample_id"].max() + 1
    new_row = {"sample_id": int(new_id), "region": entry.country, "variety": entry.type,
               "quality_category": entry.quality_category, "ripeness_index": entry.ripeness_index}
    #print(new_row)
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    #df.to_csv("data.csv", index=False)
    return df.fillna("").tail().to_dict()