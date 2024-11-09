import pandas as pd
import plotly.express as px
import numpy as np

# Load the dataset
data = pd.read_csv('Vehicle collision.csv')

# Clean and prepare the data
data['DATE'] = pd.to_datetime(data['DATE'], format='%m/%d/%y')
data['MONTH'] = data['DATE'].dt.month_name().str[:3]
data['MONTH'] = pd.Categorical(data['MONTH'], categories=['Jan', 'Feb', 'Mar', 'Apr'], ordered=True)
data['HOUR'] = pd.to_datetime(data['TIME'], format='%H:%M').dt.hour

# Group and aggregate the data for plotting
def create_hourly_data(df, start_hour):
    end_hour = start_hour + 6
    filtered_data = df[(df['HOUR'] >= start_hour) & (df['HOUR'] < end_hour)]
    summary = filtered_data.groupby(['MONTH', 'BOROUGH'], observed=False).agg(
        Num_Collisions=('UNIQUE KEY', 'count'),
        Total_Casualties=('PERSONS KILLED', 'sum'),
    ).reset_index()
    summary['Hour_Label'] = f'{start_hour}-{end_hour}'
    return summary

# Concatenate hourly data frames
hourly_frames = [create_hourly_data(data, i * 6) for i in range(4)]
final_data = pd.concat(hourly_frames)

# Use Plotly to create the interactive plots
fig = px.scatter(final_data, x='MONTH', y='Num_Collisions', color='BOROUGH',
                 size='Total_Casualties', hover_name='BOROUGH', facet_col='Hour_Label',
                 category_orders={'MONTH': ['Jan', 'Feb', 'Mar', 'Apr']},
                 labels={'Num_Collisions': 'Number of Collisions', 'Total_Casualties': 'Total Casualties', 'Hour_Label':'Collision from hours'},
                 title='NYC Vehicle Collisions by Time of Day and Borough',
                 size_max=50,
                 color_discrete_map={
                     'BROOKLYN': 'blue',
                     'QUEENS': 'green',
                     'MANHATTAN': 'red',
                     'STATEN ISLAND': 'purple',
                     'BRONX': 'orange'
                 }
                 )

# Update layout for bold axis titles and larger title size
fig.update_layout(
    title=dict(font=dict(size=24)),
    yaxis=dict(title=dict(text='Number of Collisions', font=dict(weight='bold', size=14))),
    legend_title_text='Borough',
    legend=dict(
        orientation="v",
        x=1.05,
        xanchor="left",
        y=1,
        yanchor="top",
        itemsizing='constant',
        bgcolor='rgba(255, 255, 255, 1)',
        bordercolor='gray',
        borderwidth=1,
        font=dict(size=10, weight='bold'),
    ),
    coloraxis_colorbar=dict(
        title='Casualties',
        tickvals=[0, 100, 500],
        ticktext=['Low', 'Medium', 'High'],
        len=0.5,
        thickness=15,
        x=1.05,  # Position to align with the borough legend
        xanchor='left',
        yanchor='bottom',
        y=0
    )
)
fig.update_xaxes(tickangle=-45)

# Show the figure
fig.show()
