import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark.context import get_active_session

# ----------------------------
# Get current Snowflake session
# ----------------------------
session = get_active_session()

st.title("🥤 Customize Your Smoothie! 🥤")

# ----------------------------
# Input for smoothie name
# ----------------------------
smoothie_name = st.text_input("Name on Smoothie:", "Johnny")
st.write(f"The name on your Smoothie will be: {smoothie_name}")

# ----------------------------
# Fetch fruits list from Snowflake
# ----------------------------
fruit_df = session.table("smoothies.public.fruit_options").to_pandas()
fruit_options = fruit_df["FRUIT_NAME"].tolist()

# ----------------------------
# Multi-select fruit ingredients
# ----------------------------
ingredients = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_options,
    max_selections=5
)

# ----------------------------
# Loop through each selected fruit
# ----------------------------
for fruit in ingredients:
    # Lookup the API search value (SEARCH_ON column)
    search_on = fruit_df.loc[fruit_df["FRUIT_NAME"] == fruit, "SEARCH_ON"].values[0]

    # Show the mapping sentence
    st.info(f"The search value for {fruit} is {search_on}.")

    # Call the Smoothiefroot API
    url = f"https://my.smoothiefroot.com/api/fruit/{search_on}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        st.subheader(f"{fruit} Nutrition Information")

        # Convert JSON to DataFrame for pretty table
        nutrition_df = pd.DataFrame(list(data.items()), columns=["Nutrient", "Value"])
        st.table(nutrition_df)

    else:
        st.subheader(f"{fruit} Nutrition Information")
        st.error("Nutrition info not found.")
