import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, callback, Output, Input
import pandas as pd 
import altair as alt
import dash_vega_components as dvc
import plotly.express as px


# Initialize Dash app with Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Read processed data
data = pd.read_csv('data/processed/salaries.csv')

# Precompute salary ranges
def compute_salary_ranges(df):
    bins = [0, 50000, 100000, 150000, 200000, df["salary_in_usd"].max()]  
    labels = ["<50K", "50K-100K", "100K-150K", "150K-200K", ">200K"] 
    df["salary_range"] = pd.cut(df["salary_in_usd"], bins=bins, labels=labels, include_lowest=True)
    return df

data = compute_salary_ranges(data)

# Map Page Layout
map_layout = html.Div([
    html.H2("Salary Distribution Map", className="text-center my-4"),
    
    dcc.Graph(id="salary-map") 
])

# Dashboard page layout
dashboard_layout = dbc.Container([
    
    # Filters
    dbc.Row([
        dbc.Col(dcc.Dropdown(id='company-location', options=[], placeholder="Select Company Location"), width=4),
        dbc.Col(dcc.Dropdown(id='experience-level', options=[], placeholder="Select Experience Level"), width=4),
        dbc.Col(dcc.Dropdown(id='employment-type', options=[], placeholder="Select Employment Type"), width=4),
    ], className="mb-4"),

    # Salary Card & Line Chart
    dbc.Row([
        dbc.Col([
            dbc.Card([            
                dbc.CardBody([
                    html.H4("Average Salary (Filtered)", className="card-title"),
                    html.H2(id='filtered-average-salary', className="card-text"),
                ])
                ], className="shadow p-3"
            ), 
            dbc.Card([            
                dbc.CardBody([
                    html.H4("Overall Average Salary", className="card-title"),
                    html.H2(id='overall-average-salary', className="card-text"),
                ])
                ], className="shadow p-3"
            )],
            width=4
        ),

        dbc.Col(
            html.Div([
                html.H4("Salary Over 4 Years", className="text-center"),
                dvc.Vega(id='line-chart', className="border p-3")
            ]), width=8
        )
    ]),

    # Bar charts
    dbc.Row([
        #dbc.Col(
            #dbc.Card([
            
        #], className="shadow p-3"), width=4),

        dbc.Col(html.Div([
            html.H4("Overall Salary by Company Size", className="text-center"),
            dvc.Vega(id='bar-company-size', className="border p-3")  # Placeholder
        ]), width=6),
        
        dbc.Col(html.Div([
            html.H4("Overall Salary by Top 10 Job Title", className="text-center"),
            dvc.Vega(id='bar-job-title', className="border p-3")  # Placeholder
        ]), width=6),

    ], className="mb-4"),

    dbc.Row([
        dbc.Col(html.Div([
            html.H4("Overall Salary by Employment Type", className="text-center"),
            dvc.Vega(id='bar-employment-type', className="border p-3")
            ]), width=6),
        
        dbc.Col(html.Div([
            html.H4("Overall Salary by Experience Level", className="text-center"),
            dvc.Vega(id='bar-experience-level', className="border p-3")
        ]), width=6),
        
    ], className="mb-4"),

    # description

    html.H1(' '),
    html.P('The Salary Dashboard provides an interactive analysis of Data Science job salaries. The dashboard highlights average salaries while enabling dynamic exploration of salary trends across different roles and employment structures. Users can gain insights into job market patterns, helping them compare salaries and make informed career decisions.'),
    html.P("Author: Zhengling Jiang, Kexin Shi, Jingyuan Wang, Tengwei Wang"),
    html.A(
        "Github repo",
        href="https://github.com/UBC-MDS/DSCI-532_2025_21_DS_Salaries",
        target="_blank"  # Opens in a new tab
    ),
    html.P("Latest update on March 1, 2025.")
    
], fluid=True)

# Define App Layout (Navigation + Page Content)
app.layout = dbc.Container([
    # Top Section: Title & Navigation Buttons (Fixed)
    dbc.Row([
        dbc.Col(html.H1("Data Science Salaries Tracker", className="my-2"), width="auto"), 
        dbc.Col(
            dbc.ButtonGroup([
                dbc.Button("Analytics Page", id="btn-dashboard", color="primary", className="me-2 px-4 py-2"),
                dbc.Button("Map Page", id="btn-map", color="primary", className="px-4 py-2")  
            ], className="ml-auto"), width="auto", className="d-flex align-items-center ms-3"
        )
    ], className="d-flex align-items-center mb-4"),

    # Main Content (Changes with Page)
    html.Div(id="page-content")
], fluid=True)

# Callback to handle page navigation
@app.callback(
    Output("page-content", "children"),
    [Input("btn-dashboard", "n_clicks"),
     Input("btn-map", "n_clicks")]
)
def display_page(btn_dashboard, btn_map):
    ctx = dash.callback_context

    # Default Page
    if not ctx.triggered:
        return dashboard_layout
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "btn-map":
        return map_layout
    else:
        return dashboard_layout
    
# Callback to Generate the Map
@app.callback(
    Output("salary-map", "figure"),
    Input("salary-map", "id")  # Dummy input to trigger rendering
)
def generate_salary_map(_):

    if "company_location" not in data.columns or "salary_in_usd" not in data.columns:
        return px.scatter_mapbox(title="No Data Available")

    # Compute average salary per region
    avg_salary_by_location = data.groupby("company_location")["salary_in_usd"].mean().reset_index()

    # Choropleth Map
    fig = px.choropleth(
        avg_salary_by_location,
        locations="company_location", 
        locationmode="country names", 
        color="salary_in_usd",
        color_continuous_scale="Viridis",
        title="Average Salary by Company Location",
        labels={"salary_in_usd": "Average Salary (USD)"},
    )

    fig.update_geos(showcoastlines=True, showland=True, fitbounds="locations")
    fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})

    return fig

# Calculate the overall average salary
overall_avg_salary = data['salary_in_usd'].mean()

# Callback to update the card of overall average salary
@callback(
    Output('overall-average-salary', 'children'),
    Input('overall-average-salary', 'id')  
)
def update_overall_salary(_):
    return f"${overall_avg_salary:,.2f}"

# Callback: Get options for dropdown of company location
@app.callback(
    Output('company-location', 'options'),
    Input('company-location', 'id') 
)
def set_company_location_options(_):
    unique_locations = sorted(data['company_location'].dropna().unique())
    options = [{'label': location, 'value': location} for location in unique_locations]
    return options
    
# Callback: Get options for dropdown of experience level
@app.callback(
    Output('experience-level', 'options'),
    Input('experience-level', 'id') 
)
def set_experience_level_options(_):
    unique_experience_levels = sorted(data['experience_level'].dropna().unique())
    return [{'label': level, 'value': level} for level in unique_experience_levels]

# Callback: Get options for dropdown of exployment type
@app.callback(
    Output('employment-type', 'options'),
    Input('employment-type', 'id')
)
def set_employment_type_options(_):
    unique_employment_types = sorted(data['employment_type'].dropna().unique())
    return [{'label': emp_type, 'value': emp_type} for emp_type in unique_employment_types]

# Callback to update the card, line charts based on the results of filters
@app.callback(
	Output('filtered-average-salary', 'children'),
    Output('line-chart', 'spec'),
    Input('company-location', 'value'),
    Input('experience-level', 'value'),
    Input('employment-type', 'value')
)
def update_dashboard(location, experience, employment):
    # filter
    filtered_df = data.copy()
    
    if location:
        filtered_df = filtered_df[filtered_df["company_location"] == location]
    if experience:
        filtered_df = filtered_df[filtered_df["experience_level"] == experience]
    if employment:
        filtered_df = filtered_df[filtered_df["employment_type"] == employment]

    # Calculate average salary based on the outputs of filters
    avg_salary = filtered_df["salary_in_usd"].mean()
    avg_salary_text = f"${avg_salary:,.0f}" if not pd.isna(avg_salary) else "N/A"

    # generate line chart
    line_chart_data = (
        filtered_df.groupby("work_year")["salary_in_usd"]
        .mean()
        .reset_index()
    )

    line_chart = alt.Chart(line_chart_data).mark_line(point=True).encode(
        x=alt.X("work_year:O", title="Year"),
        y=alt.Y("salary_in_usd:Q",
                scale=alt.Scale(nice=True),
                axis=alt.Axis(format="$~s")),
        tooltip=["work_year", "salary_in_usd"]
    ).properties(
        width=800,
        height=100
    ).interactive()

    return avg_salary_text, line_chart.to_dict()

# Callback to update the employment_type Bar Chart based on the results of filters
@app.callback(
    Output('bar-employment-type', 'spec'),
    Input('company-location', 'value'),
    Input('experience-level', 'value'),
    Input('employment-type', 'value')
)
def update_bar_chart_employment_type(location, experience, employment):
    # Filter
    filtered_df = data.copy()
    
    if location:
        filtered_df = filtered_df[filtered_df["company_location"] == location]
    if experience:
        filtered_df = filtered_df[filtered_df["experience_level"] == experience]
    if employment:
        filtered_df = filtered_df[filtered_df["employment_type"] == employment]

    # Calculate average salary based on the outputs of filters
    employment_chart_data = (
        filtered_df.groupby("employment_type", as_index=False)["salary_in_usd"].mean()
    )

    if employment_chart_data .empty:
        return html.P("No data available.")

    # Create Altair Bar Chart
    employment_chart = alt.Chart(employment_chart_data).mark_bar().encode(
        x=alt.X("salary_in_usd:Q",
                title="Average Salary (K USD)", 
                scale=alt.Scale(domain=[0, employment_chart_data["salary_in_usd"].max()]),  
                axis=alt.Axis(format="~s")),
        y=alt.Y("employment_type:N", sort="-x"),
        tooltip=["employment_type", "salary_in_usd"]
    ).properties(
        width=500,
        height=200
    )

    return employment_chart.to_dict()

# Callback to update the Bar Chart for Salary by Experience Level based on the filter results
@app.callback(
    Output('bar-experience-level', 'spec'),
    Input('company-location', 'value'),
    Input('experience-level', 'value'),
    Input('employment-type', 'value')
)
def update_bar_chart_experience_level(location, experience, employment):
    # Filter
    filtered_df = data.copy()
    
    if location:
        filtered_df = filtered_df[filtered_df["company_location"] == location]
    if experience:
        filtered_df = filtered_df[filtered_df["experience_level"] == experience]
    if employment:
        filtered_df = filtered_df[filtered_df["employment_type"] == employment]

    # Calculate average salary based on the outputs of filters
    experience_chart_data = (
        filtered_df.groupby("experience_level", as_index=False)["salary_in_usd"].mean()
    )

    if experience_chart_data.empty:
        return html.P("No data available.")

    # Create Altair Bar Chart
    experience_chart = alt.Chart(experience_chart_data).mark_bar().encode(
        x=alt.X("salary_in_usd:Q",
                title="Average Salary (K USD)", 
                scale=alt.Scale(domain=[0, experience_chart_data["salary_in_usd"].max()]),  
                axis=alt.Axis(format="~s")),
        y=alt.Y("experience_level:N", sort="-x"),
        tooltip=["experience_level", "salary_in_usd"]
    ).properties(
        width=500,
        height=200
    )

    return experience_chart.to_dict()


# Callback to generate the Salary by Company Size based on filter results

@app.callback(
    Output('bar-company-size',"spec"),
    Input('company-location', 'value'),
    Input('experience-level', 'value'),
    Input('employment-type', 'value')
)
def show_salary_by_size_bar(location, experience, employment):
    # Filter
    filtered_df = data.copy()
    
    if location:
        filtered_df = filtered_df[filtered_df["company_location"] == location]
    if experience:
        filtered_df = filtered_df[filtered_df["experience_level"] == experience]
    if employment:
        filtered_df = filtered_df[filtered_df["employment_type"] == employment]

    # Calculate average salary based on the outputs of filters
    salary_by_size = (
        filtered_df.groupby("company_size", as_index=False)["salary_in_usd"].mean()
    )

    if salary_by_size.empty:
        return html.P("No data available.")
    
     # Create Altair Bar Chart
    size_bar_chart = alt.Chart(salary_by_size).mark_bar().encode(
        x=alt.X("salary_in_usd:Q",
                title="Average Salary (K USD)", 
                scale=alt.Scale(domain=[0, salary_by_size["salary_in_usd"].max()]),  
                axis=alt.Axis(format="~s")),
        y=alt.Y("company_size:N",sort="-x"),
        tooltip=["company_size", "salary_in_usd"]
    ).properties(
        width=500,
        height=200
    )
    return size_bar_chart.to_dict()
    

# Callback to generate bar chart for Overall Top 10 Job Title by Salary based on filtered results
@app.callback(
    Output('bar-job-title',"spec"),
    Input('company-location', 'value'),
    Input('experience-level', 'value'),
    Input('employment-type', 'value')
)
def show_salary_by_title(location, experience, employment):
     # Filter
    filtered_df = data.copy()
    
    if location:
        filtered_df = filtered_df[filtered_df["company_location"] == location]
    if experience:
        filtered_df = filtered_df[filtered_df["experience_level"] == experience]
    if employment:
        filtered_df = filtered_df[filtered_df["employment_type"] == employment]

    # Calculate average salary based on the outputs of filters and choose top 10
    salary_by_title = (
        filtered_df.groupby("job_title", as_index=False)["salary_in_usd"].mean()
    )

    if salary_by_title.empty:
        return html.P("No data available.")

    top10_salary_by_title = salary_by_title.nlargest(10, "salary_in_usd")

    title_bar_chart = alt.Chart(top10_salary_by_title).mark_bar().encode(
        x=alt.X("salary_in_usd:Q",
                title="Average Salary (K USD)", 
                scale=alt.Scale(domain=[0, top10_salary_by_title["salary_in_usd"].max()]),  
                axis=alt.Axis(format="~s")),
        y=alt.Y("job_title:N",sort="-x"),
        tooltip=["job_title", "salary_in_usd"]
    ).properties(
        width=500,
        height=200
    )
    return title_bar_chart.to_dict()


# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
