# --------------------------------------------
# Imports at the top - PyShiny EXPRESS VERSION
# --------------------------------------------

# From shiny, import just reactive and render
from shiny import reactive, render

# From shiny.express, import just ui and inputs if needed
from shiny.express import ui

import random
from datetime import datetime,timedelta
from collections import deque
import pandas as pd
import plotly.express as px
from shinywidgets import render_plotly
from scipy import stats

# --------------------------------------------
# Import icons as you like
# --------------------------------------------

# https://fontawesome.com/v4/cheatsheet/
from faicons import icon_svg

# --------------------------------------------
# Shiny EXPRESS VERSION
# --------------------------------------------

# --------------------------------------------
# First, set a constant UPDATE INTERVAL for all live data
# Constants are usually defined in uppercase letters
# Use a type hint to make it clear that it's an integer (: int)
# --------------------------------------------

UPDATE_INTERVAL_SECS: int = 3

# --------------------------------------------
# Initialize a REACTIVE VALUE with a common data structure
# The reactive value is used to store state (information)
# Used by all the display components that show this live data.
# This reactive value is a wrapper around a DEQUE of readings
# --------------------------------------------

DEQUE_SIZE: int = 5
reactive_value_wrapperday = reactive.value(deque(maxlen=DEQUE_SIZE))
reactive_value_wrappernight = reactive.value(deque(maxlen=DEQUE_SIZE))
# --------------------------------------------
# Initialize a REACTIVE CALC that all display components can call
# to get the latest data and display it.
# The calculation is invalidated every UPDATE_INTERVAL_SECS
# to trigger updates.
# It returns a tuple with everything needed to display the data.
# Very easy to expand or modify.
# --------------------------------------------


@reactive.calc()
def reactive_calc_combined():
    # Invalidate this calculation every UPDATE_INTERVAL_SECS to trigger updates
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)

    # Data generation logic
    tempday = round(random.uniform(113, 104), 1)
    tempnight = round(random.uniform(77, 86), 1)
    timestampday = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestampnight = timestampday - timedelta(hours=12)
    new_dictionary_entryday = {"tempday":tempday, "timestampday":timestamp}
    new_dictionary_entrynight = {"tempnight":tempnight, "timestampnight":timestampnight}

    # get the deque and append the new entry
    reactive_value_wrapperday.get().append(new_dictionary_entryday)
    reactive_value_wrappernight.get().append(new_dictionary_entrynight)
    
    # Get a snapshot of the current deque for any further processing
    deque_snapday = reactive_value_wrapperday.get()
    deque_snapnight = reactive_value_wrappernight.get()

    # For Display: Convert deque to DataFrame for display
    dfday = pd.DataFrame(deque_snapday)
    dfnight = pd.DataFrame(deque_snapnight)

    # For Display: Get the latest dictionary entry
    latest_dictionary_entryday = new_dictionary_entryday
    latest_dictionary_entrynight = new_dictionary_entrynight
    # Return a tuple with everything we need
    # Every time we call this function, we'll get all these values
    return deque_snapday, dfday, latest_dictionary_entryday,deque_snapnight, dfnight, latest_dictionary_entrynight




# Define the Shiny UI Page layout
# Call the ui.page_opts() function
# Set title to a string in quotes that will appear at the top
# Set fillable to True to use the whole page width for the UI
ui.page_opts(title="Daytime Teperatures in Fiyadh, Saudi Arabia", fillable=True)


# Sidebar is typically used for user interaction/information
# Note the with statement to create the sidebar followed by a colon
# Everything in the sidebar is indented consistently
with ui.sidebar(open="open"):
    ui.h2("Riyadh - Saudi Arabia", class_="text-center")
    ui.p(
        "Day Time Temperature readings in Riyadh",
        class_="text-center",
    )
    ui.hr()
    ui.h6("Links:")
    ui.a(
        "GitHub Source",
        href="https://github.com/hrawp/cintel-05-cintel",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://github.com/hrawp/cintel-05-cintel/blob/main/dashboard/app.py",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
 #   ui.a(
 #       "PyShiny Express",
 #       href="hhttps://shiny.posit.co/blog/posts/shiny-express/",
 #       target="_blank",
 #   )

# In Shiny Express, everything not in the sidebar is in the main panel

with ui.layout_columns():
    if( daynight = day,
        with ui.value_box(
            showcase=icon_svg("sun"),
            theme="bg-gradient-red-orange"
        ):

            "Current Temperature"

            @render.text
            def display_temp():
                """Get the latest reading and return a temperature string"""
                deque_snapday, dfday, latest_dictionary_entryday = reactive_calc_combined()
                return f"{latest_dictionary_entryday['tempday']} F"
    else
        with ui.value_box(
            showcase=icon_svg("moon"),
            theme="bg-gradient-blue-dark"
        ):

            "Current Temperature"

            @render.text
            def display_temp():
                """Get the latest reading and return a temperature string"""
                deque_snapnight, dfnight, latest_dictionary_entrynight = reactive_calc_combined()
                return f"{latest_dictionary_entrynight['tempnight']} F"
    )

  
    if( daynight = day,
        with ui.value_box(
            full_screen=True, 
            theme="bg-gradient-red-orange"
        ):
            "Current Date and Time"
        
        
            @render.text
            def display_time():
                """Get the latest reading and return a timestamp string"""
                deque_snapshot, df, latest_dictionary_entryday = reactive_calc_combined()
                return f"{latest_dictionary_entryday['timestampday']}"
    else
        with ui.value_box(
            full_screen=True, 
            theme="bg-gradient-blue-dark"
        ):
            "Current Date and Time"
        
        
            @render.text
            def display_time():
                """Get the latest reading and return a timestamp string"""
                deque_snapshot, df, latest_dictionary_entrynight = reactive_calc_combined()
                return f"{latest_dictionary_entrynight['timestampnight']}"
    )
#with ui.card(full_screen=True, min_height="40%"):
with ui.card(
    full_screen=True
):
    if( daynight = day,
        ui.card_header("Most Recent Readings")
    

        @render.data_frame
        def display_df():
            """Get the latest reading and return a dataframe with current readings"""
            deque_snapday, dfday, latest_dictionary_entryday = reactive_calc_combined()
            pd.set_option('display.width', None)        # Use maximum width
            return render.DataGrid( dfday,width="100%")
    else
        @render.data_frame
        def display_df():
            """Get the latest reading and return a dataframe with current readings"""
            deque_snapnight, dfnight, latest_dictionary_entrynight = reactive_calc_combined()
            pd.set_option('display.width', None)        # Use maximum width
            return render.DataGrid( dfnight,width="100%")

    )
with ui.card():
    ui.card_header("Chart with Current Trend")
    
    if(
        @render_plotly
        def display_plot():
            # Fetch from the reactive calc function
            deque_snapday, dfday, latest_dictionary_entryday = reactive_calc_combined()

            # Ensure the DataFrame is not empty before plotting
            if not dfday.empty:
                # Convert the 'timestamp' column to datetime for better plotting
                dfday["timestampday"] = pd.to_datetime(dfday["timestampday"])

                # Create scatter plot for readings
                # pass in the df, the name of the x column, the name of the y column,
                # and more
        
                fig = px.scatter(dfday,
                x="timestamp",
                y="temp",
                title="Temperature Readings with Regression Line",
                labels={"temp": "Temperature (°F)", "timestamp": "Time"},
                color_discrete_sequence=["red"] )
            
                # Linear regression - we need to get a list of the
                # Independent variable x values (time) and the
                # Dependent variable y values (temp)
                # then, it's pretty easy using scipy.stats.linregress()

                # For x let's generate a sequence of integers from 0 to len(df)
                sequence = range(len(dfday))
                x_vals = list(sequence)
                y_vals = dfday["temp"]

                slope, intercept, r_value, p_value, std_err = stats.linregress(x_vals, y_vals)
                dfday['best_fit_line'] = [slope * x + intercept for x in x_vals]

                # Add the regression line to the figure
                fig.add_scatter(x=dfday["timestamp"], y=dfday['best_fit_line'], mode='lines', name='Regression Line')

                # Update layout as needed to customize further
                fig.update_layout(yaxis=dict(range=[113.1, 103.9]),xaxis_title="Time",yaxis_title="Temperature (°F)",autosize=False,width=1000,height=400)

        return fig
    else
        @render_plotly
        def display_plot():
            # Fetch from the reactive calc function
            deque_snapshot, dfnight, latest_dictionary_entry = reactive_calc_combined()

            # Ensure the DataFrame is not empty before plotting
            if not dfnight.empty:
                # Convert the 'timestamp' column to datetime for better plotting
                dfday["timestamp"] = pd.to_datetime(dfnight["timestamp"])

                # Create scatter plot for readings
                # pass in the df, the name of the x column, the name of the y column,
                # and more
        
                fig = px.scatter(dfnight,
                x="timestamp",
                y="temp",
                title="Temperature Readings with Regression Line",
                labels={"temp": "Temperature (°F)", "timestamp": "Time"},
                color_discrete_sequence=["blue"] )
            
                # Linear regression - we need to get a list of the
                # Independent variable x values (time) and the
                # Dependent variable y values (temp)
                # then, it's pretty easy using scipy.stats.linregress()

                # For x let's generate a sequence of integers from 0 to len(df)
                sequence = range(len(dfnight))
                x_vals = list(sequence)
                y_vals = dfday["temp"]

                slope, intercept, r_value, p_value, std_err = stats.linregress(x_vals, y_vals)
                dfnight['best_fit_line'] = [slope * x + intercept for x in x_vals]

                # Add the regression line to the figure
                fig.add_scatter(x=dfnight["timestamp"], y=dfnight['best_fit_line'], mode='lines', name='Regression Line')

                # Update layout as needed to customize further
                fig.update_layout(yaxis=dict(range=[76.9, 86.1]),xaxis_title="Time",yaxis_title="Temperature (°F)",autosize=False,width=1000,height=400)

        return fig
    )
