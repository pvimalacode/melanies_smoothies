# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import time
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your smoothie!
    """
)





#option = st.selectbox(
#    "What is your favorite fruit",
#    ("Banana", "Strawberry", "Peaches"),
#)
#
#st.write("your favorite fruit is", option)
text_help='Enter the name for smoothie'
name_on_order = st.text_input("Name on Smoothie:",placeholder =text_help,key="ip_name")
st.write("The name on your smoothie will be", name_on_order)

def clear_text():
    st.session_state["ip_name"] = ""
    st.session_state["fruit_list"] = []

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)



ingredients_list = st.multiselect(
    "Choose upto 5 ingredients:",
    my_dataframe,
    max_selections=5,
    key='fruit_list'
)

ingredients_string = ' '.join(ingredients_list)
ingredients_string_txt = ' , '.join(ingredients_list)

if ingredients_string and name_on_order:
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','""" +  name_on_order +  """');"""
    for ingredient in ingredients_list:
        st.subheader(ingredient + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon"+ ingredient)
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)


def insert_data():
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie with '+ingredients_string_txt+' is ordered,'+name_on_order+'!', icon="✅")
    clear_text()
      
    #st.write(my_insert_stmt)
time_to_insert = st.button("Submit", type="primary", on_click=insert_data)


    

    
    
