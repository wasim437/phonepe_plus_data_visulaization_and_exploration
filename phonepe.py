



import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import psycopg2
import plotly.express as px
import json
import requests

mydb = psycopg2.connect(host="localhost",
                        user='postgres',
                        port="5432",
                        database="phonepe_data",
                        password="admin")
cursor = mydb.cursor()

# aggre_trans
cursor.execute("SELECT  * FROM  aggregated_transaction")
table1 = cursor.fetchall()
aggre_trans = pd.DataFrame(table1, columns=("State", "Year", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))

# aggre_user
cursor.execute("SELECT  * FROM  aggregated_user")
table2 = cursor.fetchall()
aggre_user = pd.DataFrame(table2, columns=("State", "Year", "Quarter", "Brands", "Count", "Percentage"))

# map_trans
cursor.execute("SELECT  * FROM  map_transaction")
table3 = cursor.fetchall()
map_trans = pd.DataFrame(table3, columns=("State", "Year", "Quarter", "District", "Transaction_count", "Transaction_amount"))

# map_user
cursor.execute("SELECT  * FROM map_user")
table4 = cursor.fetchall()
map_user = pd.DataFrame(table4, columns=("State", "Year", "Quarter", "District", "RegisteredUser", "AppOpens"))

# top_trans
cursor.execute("SELECT  * FROM top_transaction")
table5 = cursor.fetchall()
top_trans = pd.DataFrame(table5, columns=("State", "Year", "Quarter", "Pincode", "Transaction_count", "Transaction_amount"))

# top_user
cursor.execute("SELECT  * FROM top_user")
table6 = cursor.fetchall()
top_user = pd.DataFrame(table6, columns=("State", "Year", "Quarter", "Pincode", "RegisteredUsers"))


def transaction_amount_count_Y(df, year):
    tacy = df[df["Year"] == year]
    tacy.reset_index(drop=True, inplace=True)
    tacyg = tacy.groupby("State")[[ "Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1, col2 , = st.columns(2)
    with col1:

     fig_amount = px.bar(tacyg, x='State', y="Transaction_amount", title=f"{year}_TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
     st.plotly_chart(fig_amount)

    with col2:
     fig_count = px.bar(tacyg, x='State', y="Transaction_count", title=f"{year}_TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
     st.plotly_chart(fig_count)


    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    col1, col2 , = st.columns(2)
    with col1:
        response = requests.get(url)
        states_name = []
        data1 = json.loads(response.content)
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        fig_india_1 = px.choropleth(tacyg, geojson=data1, locations="State", featureidkey="properties.ST_NM",
                                    color="Transaction_amount", color_continuous_scale="viridis",
                                    range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                    hover_name="State", title=f"{year} TRANSACTION AMOUNT", fitbounds="locations",
                                    height=500, width=500)

        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2 = px.choropleth(tacyg, geojson=data1, locations="State", featureidkey="properties.ST_NM",
                                    color="Transaction_count", color_continuous_scale="viridis",
                                    range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                    hover_name="State", title=f"{year} TRANSACTION COUNT", fitbounds="locations",
                                    height=500, width=500)

        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)
    return tacy



def transaction_amount_count_Y_Q(df, Quarter):
    tacy = df[df["Quarter"] == Quarter]
    tacy.reset_index(drop=True, inplace=True)
    tacyg = tacy.groupby("State")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    col1, col2 , = st.columns(2)
    with col1:

        fig_amount = px.bar(tacyg, x='State', y="Transaction_amount", title=f"{tacy['Year'].min()} YEAR  {Quarter}QUARTER TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
        st.plotly_chart(fig_amount )
    with col2:
        fig_count = px.bar(tacyg, x='State', y="Transaction_count", title=f"{tacy['Year'].min()} YEAR  {Quarter}QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width=600)
        st.plotly_chart( fig_count)
    col1, col2 , = st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

        response = requests.get(url)
        states_name = []
        data1 = json.loads(response.content) 
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        fig_india_1 = px.choropleth(tacyg, geojson=data1, locations="State", featureidkey="properties.ST_NM",
                                    color="Transaction_amount", color_continuous_scale="viridis",
                                    range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                    hover_name="State",title=f"{tacy['Year'].min()} YEAR  {Quarter}QUARTER TRANSACTION AMOUNT", fitbounds="locations",
                                    height=500, width=500)

        fig_india_1.update_geos(visible=False)
        st.plotly_chart( fig_india_1)
    with col2:    
        fig_india_2 = px.choropleth(tacyg, geojson=data1, locations="State", featureidkey="properties.ST_NM",
                                    color="Transaction_count", color_continuous_scale="viridis",
                                    range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                    hover_name="State", title=f"{tacy['Year'].min()} YEAR  {Quarter}QUARTER TRANSACTION AMOUNT", fitbounds="locations",
                                    height=500, width=500)

        fig_india_2.update_geos(visible=False)
        st.plotly_chart( fig_india_2)
        return tacy


def aggre_trans_count(df, state):


    tacy = df[df["State"] == state]
    tacy.reset_index(drop=True, inplace=True)
    tacyg = tacy.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    col1 ,col2=st.columns(2)
    with col1:

        fig_pi_1 = px.pie(data_frame=tacyg, names="Transaction_type", values="Transaction_amount", width=600, title=f"{state.upper()} TRANSACTION AMOUNT", hole=0.5, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pi_1)

    with col2:
        fig_pi_2 = px.pie(data_frame=tacyg, names="Transaction_type", values="Transaction_count", width=600, title=f"{state.upper()} TRANSACTION COUNT", hole=0.5, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pi_2)

def aggre_user_plot_1(df,year):

    aguy =df[df['Year']==year]
    aguy.reset_index(drop=True,inplace=True)
    aguyg=pd.DataFrame(aguy.groupby("Brands")["Count"].sum())
    aguyg.reset_index(inplace=True)
    fig_ba_1 = px.bar(aguyg,x="Brands",y= "Count" ,title=f" {year} BRANDS AND TRANSACTION COUNT",width=1000,color_discrete_sequence=px.colors.sequential.Mint_r,hover_name="Brands")
    st.plotly_chart(fig_ba_1)
    return aguy
 
def aggre_user_plot_2(df, quarter):
    aguyq =df[df['Quarter']== quarter]
    aguyq.reset_index(drop=True,inplace=True)
    aguyqg=pd.DataFrame(aguyq.groupby("Brands")[	"Count"].sum())
    aguyqg.reset_index(inplace=True)
    fig_ba_1 = px.bar(aguyqg,x="Brands",y= "Count" ,title= f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",width=1000,color_discrete_sequence=px.colors.sequential.amp,hover_name="Brands")

    st.plotly_chart( fig_ba_1)
    return aguyq

def aggre_year_plot_3(df, state):
    auyqs = df[df["State"] == state]
    auyqs.reset_index(drop=True, inplace=True)
    fig_line_1 = px.line(auyqs, x="Brands", y="Count", hover_data="Percentage", title=f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE", width=1000, markers=True)
    st.plotly_chart(fig_line_1 )

def map_trans_dis(df, state):


    tacy = df[df["State"] == state]
    tacy.reset_index(drop=True, inplace=True)
    tacyg = tacy.groupby("District")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    col1 ,col2=st.columns(2)
    

    fig_bar_1 = px.bar(tacyg, x="Transaction_amount", y="District", orientation="h", title=f"{state.upper()}   DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_bar_1)

    fig_bar_2 = px.bar(tacyg, x="Transaction_count", y="District", orientation="h", title=f"{state.upper()}   DISTRICT AND TRANSACTION COUNT", color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart( fig_bar_2)

def map_user_plot_1(df , year):
    muy = df[df['Year'] == year]
    muy.reset_index(drop=True, inplace=True)



    muyg = muy.groupby("State")[["RegisteredUser","AppOpens"]].sum()
    muyg.reset_index(inplace=True)
    fig_line_1 = px.line(muyg, x="State", y=["RegisteredUser","AppOpens"], title=f"{year}  REGISTERED USERS APPOPENS", width=1000, markers=True, color_discrete_sequence=px.colors.qualitative.Set1)
    st.plotly_chart( fig_line_1 )
    return muy

def map_user_plot_2(df ,quarter):
    muyq = df[df['Quarter'] == quarter]
    muyq.reset_index(drop=True, inplace=True)

    muygq = muyq.groupby("State")[["RegisteredUser","AppOpens"]].sum()
    muygq.reset_index(inplace=True)
    fig_line_1 = px.line(muygq, x="State", y=["RegisteredUser","AppOpens"], title=f"{df['Year'].min()}  {quarter}  REGISTERED USERS APPOPENS", width=1000, markers=True, color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)
    return muyq

def map_user_plot_3(df, states):
    muyqs = df[df['State'] == states]
    muyqs.reset_index(drop=True, inplace=True)
    col1, col2 = st.columns(2)
    with col1:
        fig_map_user_bar_1 = px.bar(muyqs, x="RegisteredUser", y="District", orientation="h", title="REGISTERED USER",
                                     height=800, width=700, color_discrete_sequence=px.colors.sequential.algae)
   

def top_trans_plot_1(df,state):
    tiy = df[df['State'] == state]
    tiy.reset_index(drop=True, inplace=True)
    col1, col2 = st.columns(2)
    with col1:

        fig_top_trans_bar_1 =px.bar(tiy,x="Quarter",y="Transaction_amount",hover_data="Pincode",title="TRANSACTION AMOUNT",height=800,color_discrete_sequence=px.colors.sequential.algae)
        st.plotly_chart(fig_top_trans_bar_1)
    with col2:
        fig_top_trans_bar_2 =px.bar(tiy,x="Quarter",y="Transaction_count",hover_data="Pincode",title="TRANSACTION COUNT",height=800,color_discrete_sequence=px.colors.sequential.algae)
        st.plotly_chart(fig_top_trans_bar_2 )
def top_user_plot_1(df,year):

    tuy = df[df['Year'] == year]
    tuy.reset_index(drop=True, inplace=True)


    tuyg = pd.DataFrame(tuy.groupby(["State", "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)

    
    
    
    fig_top_plot_1  =px.area(tuyg,x="State", y="RegisteredUsers",hover_name="State",color="Quarter",title=f"{year} REGISTERED USERS",height=800,color_discrete_sequence=px.colors.sequential.ice)
    st.plotly_chart(fig_top_plot_1)
    
    return tuy


def top_user_plot_2(df , state):
    
    tuys = df[df['State'] ==  state]
    tuys.reset_index(drop=True, inplace=True)

    
    fig_top_pot_2 = px.bar(tuys, x="Quarter", y="RegisteredUsers", title="REGISTERED USERS, PINCODES, QUARTER",
                        width=1000, height=800, color="RegisteredUsers", hover_data=["Pincode"],
                        color_continuous_scale=px.colors.sequential.Magenta)

    
    st.plotly_chart(fig_top_pot_2)

def top_chart_transaction_amount(table_name):
    import psycopg2
    import pandas as pd
    import plotly.express as px

    mydb = psycopg2.connect(host="localhost",
                            user='postgres',
                            port="5432",
                            database="phonepe_data",
                            password="admin")
    cursor = mydb.cursor()

    query1 = f'''select state, sum(transaction_amount) AS transaction_amount
                from {table_name}
                group by state
                order by transaction_amount desc
                limit 10;'''

    cursor.execute(query1)
    table = cursor.fetchall()
    mydb.commit()
    df1 = pd.DataFrame(table, columns=["States", "Transaction Amount"])

    fig_amount = px.bar(df1, x='States', y="Transaction Amount", title="Transaction Amount", hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
    st.plotly_chart(fig_amount)

    query2 = f'''select state, sum(transaction_amount) AS transaction_amount
                from {table_name}
                group by state
                order by transaction_amount 
                limit 10;'''

    cursor.execute(query2)
    table2 = cursor.fetchall()
    mydb.commit()
    df_2 = pd.DataFrame(table2, columns=["States", "Transaction Amount"])

    fig_amount_2 = px.bar(df_2, x='States', y="Transaction Amount", title="Transaction Amount", hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
    st.plotly_chart(fig_amount_2 )

    query3 = f'''
                select state, avg(transaction_amount ) AS avg_transaction_amount
                from {table_name}
                group by state
                order by avg_transaction_amount;'''

    cursor.execute(query3)
    table3 = cursor.fetchall()
    mydb.commit()
    df_3 = pd.DataFrame(table3, columns=["States", "Average Transaction Amount"])

    fig_amount_3 = px.bar(df_3, x='Average Transaction Amount', y="States", title="Average Transaction Amount", 
                        hover_name="States", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Cividis, height=650, width=600)
    st.plotly_chart(fig_amount_3)
def top_chart_transaction_count(table_name):
    import psycopg2
    import pandas as pd
    import plotly.express as px

    mydb = psycopg2.connect(host="localhost",
                            user='postgres',
                            port="5432",
                            database="phonepe_data",
                            password="admin")
    cursor = mydb.cursor()

    query1 = f'''select state, sum(transaction_count) AS transaction_count
                from {table_name}
                group by state
                order by transaction_count desc
                limit 10;'''

    cursor.execute(query1)
    table = cursor.fetchall()
    mydb.commit()
    df1 = pd.DataFrame(table, columns=["States", "Transaction count"])

    fig_amount = px.bar(df1, x='States', y="Transaction count", title="Transaction count", hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
    st.plotly_chart(fig_amount)

    query2 = f'''select state, sum(transaction_count) AS transaction_count
                from {table_name}
                group by state
                order by transaction_count
                limit 10;'''

    cursor.execute(query2)
    table2 = cursor.fetchall()
    mydb.commit()
    df_2 = pd.DataFrame(table2, columns=["States", "Transaction count"])

    fig_amount_2 = px.bar(df_2, x='States', y="Transaction count", title="Transaction count", hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
    st.plotly_chart(fig_amount_2)

    query3 = f'''
                select state, avg(transaction_count ) AS avg_transaction_count
                from {table_name}
                group by state
                order by avg_transaction_count;'''

    cursor.execute(query3)
    table3 = cursor.fetchall()
    mydb.commit()
    df_3 = pd.DataFrame(table3, columns=["States", "Average Transaction count"])

    fig_amount_3 = px.bar(df_3, x='Average Transaction count', y="States", title="Average Transaction count", 
                        hover_name="States", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Cividis, height=650, width=600)
    st.plotly_chart(fig_amount_3)

def top_chart_transaction_amount1(table_name):
    import psycopg2
    import pandas as pd
    import plotly.express as px

    mydb = psycopg2.connect(host="localhost",
                            user='postgres',
                            port="5432",
                            database="phonepe_data",
                            password="admin")
    cursor = mydb.cursor()

    query1 = f'''select state, sum(amount) AS transaction_amount
                from {table_name}
                group by state
                order by transaction_amount desc
                limit 10;'''

    cursor.execute(query1)
    table = cursor.fetchall()
    mydb.commit()
    df1 = pd.DataFrame(table, columns=["States", "Transaction Amount"])

    fig_amount = px.bar(df1, x='States', y="Transaction Amount", title="Transaction Amount", hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
    st.plotly_chart(fig_amount)

    query2 = f'''select state, sum(amount) AS transaction_amount
                from {table_name}
                group by state
                order by transaction_amount 
                limit 10;'''

    cursor.execute(query2)
    table2 = cursor.fetchall()
    mydb.commit()
    df_2 = pd.DataFrame(table2, columns=["States", "Transaction Amount"])

    fig_amount_2 = px.bar(df_2, x='States', y="Transaction Amount", title="Transaction Amount", hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
    st.plotly_chart(fig_amount_2)

    query3 = f'''
                select state, avg(amount ) AS avg_transaction_amount
                from {table_name}
                group by state
                order by avg_transaction_amount;'''

    cursor.execute(query3)
    table3 = cursor.fetchall()
    mydb.commit()
    df_3 = pd.DataFrame(table3, columns=["States", "Average Transaction Amount"])

    fig_amount_3 = px.bar(df_3, x='Average Transaction Amount', y="States", title="Average Transaction Amount", 
                        hover_name="States", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Cividis, height=650, width=600)
    st.plotly_chart(fig_amount_3)

def top_chart_transaction_count1(table_name):
    import psycopg2
    import pandas as pd
    import plotly.express as px

    mydb = psycopg2.connect(host="localhost",
                            user='postgres',
                            port="5432",
                            database="phonepe_data",
                            password="admin")
    cursor = mydb.cursor()

    query1 = f'''select state, sum(count) AS transaction_count
                from {table_name}
                group by state
                order by transaction_count desc
                limit 10;'''

    cursor.execute(query1)
    table = cursor.fetchall()
    mydb.commit()
    df1 = pd.DataFrame(table, columns=["States", "Transaction count"])

    fig_amount = px.bar(df1, x='States', y="Transaction count", title="Transaction count", hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
    st.plotly_chart(fig_amount)

    query2 = f'''select state, sum(count) AS transaction_count
                from {table_name}
                group by state
                order by transaction_count
                limit 10;'''

    cursor.execute(query2)
    table2 = cursor.fetchall()
    mydb.commit()
    df_2 = pd.DataFrame(table2, columns=["States", "Transaction count"])

    fig_amount_2 = px.bar(df_2, x='States', y="Transaction count", title="Transaction count", hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
    st.plotly_chart(fig_amount_2)

    query3 = f'''
                select state, avg(count ) AS avg_transaction_count
                from {table_name}
                group by state
                order by avg_transaction_count;'''

    cursor.execute(query3)
    table3 = cursor.fetchall()
    mydb.commit()
    df_3 = pd.DataFrame(table3, columns=["States", "Average Transaction count"])

    fig_amount_3 = px.bar(df_3, x='Average Transaction count', y="States", title="Average Transaction count", 
                        hover_name="States", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Cividis, height=650, width=600)
    st.plotly_chart(fig_amount_3)

def top_chart_registered_users(table_name, state):
    import psycopg2
    import pandas as pd
    import plotly.express as px

    mydb = psycopg2.connect(host="localhost",
                            user='postgres',
                            port="5432",
                            database="phonepe_data",
                            password="admin")
    cursor = mydb.cursor()

    query1 = f'''SELECT district, SUM(registereduser) AS registered_user FROM {table_name}
                WHERE state = '{state}'
                GROUP BY district
                ORDER BY registered_user DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table1 = cursor.fetchall()
    df1 = pd.DataFrame(table1, columns=["districts", "registereduser"])

    fig_amount = px.bar(df1, x='districts', y="registereduser", title="Top 10 Registered Users",
                        hover_name="districts", color_discrete_sequence=px.colors.sequential.Aggrnyl_r,
                        height=650, width=600)
    st.plotly_chart(fig_amount)

    query2 = f'''SELECT district, SUM(registereduser) AS registered_user FROM {table_name}
                WHERE state = '{state}'
                GROUP BY district
                ORDER BY registered_user
                LIMIT 10;'''

    cursor.execute(query2)
    table2 = cursor.fetchall()
    df2 = pd.DataFrame(table2, columns=["districts", "registereduser"])

    fig_amount_2 = px.bar(df2, x='districts', y="registereduser", title="Bottom 10 Registered Users",
                          hover_name="districts", color_discrete_sequence=px.colors.sequential.Aggrnyl_r,
                          height=650, width=600)
    st.plotly_chart(fig_amount_2)

    query3 = f'''SELECT district, AVG(registereduser) AS registered_user FROM {table_name}
                WHERE state = '{state}'
                GROUP BY district
                ORDER BY registered_user DESC
                LIMIT 10;'''

    cursor.execute(query3)
    table3 = cursor.fetchall()
    df3 = pd.DataFrame(table3, columns=["districts", "registereduser"])

    fig_amount_3 = px.bar(df3, x='districts', y="registereduser", title="Average Registered Users",
                          hover_name="districts", color_discrete_sequence=px.colors.sequential.Aggrnyl_r,
                          orientation="h", height=650, width=600)
    st.plotly_chart(fig_amount_3)


# streamlit part
st.set_page_config(layout="wide")


st.title(":blue[PHONEPE DATA VISUALIZATION AND EXPLORATION]")
   
col1,col2= st.columns(2)
with col1:
        video_path = r"D:\\Downloads\\videoplayback.mp4"
        st.video(video_path)
 

with col2:
        st.title("")
        image = "C:\\Users\\misaw\\Pictures\\images.jpeg" 
        st.image(image, use_column_width=2000,)
        st.download_button(":blue[DOWNLOAD THE APP NOW]", "https://www.phonepe.com/app-download/")
with st.sidebar:

    select = option_menu("main menu", ["HOME", "DATA EXPLORATION", "TOP CHARTS"])
if select == "HOME":


    col1,col2= st.columns(2)
    with col1:
        
        st.title("INDIA'S BEST TRANSACTION APP")
        st.header("PhonePe  is an Indian digital payments and financial technology company")
        st.header("****FEATURES****")
        st.header("****Credit & Debit card linking****")
        st.header("****Bank Balance check****")
        st.header("****Money Storage****")
        st.header("****PIN Authorization****")




        
     







    

elif select == "DATA EXPLORATION":
    tab1, tab2, tab3 = st.tabs(["aggregated analysis" , "map analysis" , "top analysis"])
    with tab1:
        method = st.radio("select the method", ["aggregated transaction", "aggregated user"])
        if method == "aggregated transaction":
               col1,col2=st.columns(2)
               with col1:
                    years = st.slider("select the year", aggre_trans["Year"].min(), aggre_trans["Year"].max(), aggre_trans["Year"].min())
               tac_y=transaction_amount_count_Y(aggre_trans, years)
                 
               col1,col2=st.columns(2)
               with col1:
                   states =st.selectbox("select the state",tac_y["State"].unique())
               aggre_trans_count(tac_y, states )

               col1,col2=st.columns(2)
               with col1:
                    quarter = st.slider("select the quarter", tac_y["Quarter"].min(), tac_y["Quarter"].max(), tac_y["Quarter"].min())
               agg_trans_tac_c_y=transaction_amount_count_Y_Q(tac_y, quarter )   

               col1,col2=st.columns(2)
               with col1:
                   states =st.selectbox("select the state_ty", agg_trans_tac_c_y["State"].unique())
               aggre_trans_count( agg_trans_tac_c_y, states )



        elif method =="aggregated user":
            col1,col2=st.columns(2)
            with col1:
                years = st.slider("select the year", aggre_user ["Year"].min(), aggre_user ["Year"].max(), aggre_user ["Year"].min())
            aggre_user_y=aggre_user_plot_1(aggre_user ,years)
            col1,col2=st.columns(2)
            with col1:
                quarter = st.slider("select the quarter",  aggre_user["Quarter"].min(),  aggre_user["Quarter"].max(),  aggre_user["Quarter"].min())
            aggre_user_y_q=aggre_user_plot_2( aggre_user_y, quarter ) 
            col1,col2=st.columns(2)
            with col1:
                states =st.selectbox("select the state_ty",   aggre_user_y_q["State"].unique())
            aggre_year_plot_3( aggre_user_y_q, states )  



    with tab2:
        method2 = st.radio("select the method", ["map transaction", "map user"])
        if method2 == "map transaction":
            
    
            col1, col2 = st.columns(2)
            with col1:
                map_transaction_years_slider_key = "map_transaction_years_slider"
                years = st.slider("select the year.1", map_trans["Year"].min(), map_trans["Year"].max(), map_trans["Year"].min(), key=map_transaction_years_slider_key)
            map_trans_tac_y = transaction_amount_count_Y(map_trans, years)

            
            col1,col2=st.columns(2)
            with col1:
                states =st.selectbox("select the state",map_trans_tac_y["State"].unique())
            map_trans_dis(map_trans_tac_y, states )

            col1,col2=st.columns(2)

            with col1:
                quarter = st.slider("select the quarterr", map_trans_tac_y["Quarter"].min(), map_trans_tac_y["Quarter"].max(), map_trans_tac_y["Quarter"].min())
            map_trans_y_q=transaction_amount_count_Y_Q(map_trans_tac_y , quarter )   

                        
            col1,col2=st.columns(2)
            with col1:
                states =st.selectbox("select the statee", map_trans_y_q["State"].unique())
            map_trans_dis(map_trans_y_q, states )




    if method2 == "map user":
        col1,col2=st.columns(2)
        with col1:
                years = st.slider("select the year_r", map_user ["Year"].min(), map_user["Year"].max(), map_user ["Year"].min())
        map_user_y=map_user_plot_1(map_user,years)

        col1,col2=st.columns(2)
        with col1:
            quarter= st.slider("select the quarterr", map_user_y["Quarter"].min(), map_user_y["Quarter"].max(),map_user_y["Quarter"].min())
        map_user_y_q=map_user_plot_2(map_user_y , quarter )   

        col1, col2 = st.columns(2)
        with col1:
            states = st.selectbox("Select the state", map_user_y_q["State"].unique())
        map_user_plot_3(map_user_y_q, states)
        


    with tab3:
        method3 = st.radio("select the method", ["top transaction", "top user"])
        if method3 == "top transaction":
            col1,col2=st.columns(2)
            with col1:
                years = st.slider("select the yearr", top_trans ["Year"].min(), top_trans["Year"].max(), top_trans ["Year"].min())
            top_trans_tac_y=transaction_amount_count_Y(top_trans, years)

            col1,col2=st.columns(2)
            with col1:
                states =st.selectbox("select the statess", top_trans_tac_y["State"].unique())
            top_trans_plot_1(top_trans_tac_y,states)

            col1,col2=st.columns(2)
            with col1:
                quarter= st.slider("select the quarteres", top_trans_tac_y["Quarter"].min(), top_trans_tac_y["Quarter"].max(),top_trans_tac_y["Quarter"].min())
            top_trans_tac_c_y=transaction_amount_count_Y_Q(top_trans_tac_y, quarter)  

        if method3 == "top user":
            col1,col2=st.columns(2)
            with col1:
                years = st.slider("select the yeaar", top_user ["Year"].min(), top_user["Year"].max(), top_user ["Year"].min())
            top_user_y = top_user_plot_1(top_user, years)
            
            col1,col2=st.columns(2)
            with col1:
                states =st.selectbox("select the stateess", top_user_y["State"].unique())
            top_user_plot_2(top_user_y,states)
    
                
elif select == "TOP CHARTS":
      question = st.selectbox("select the question",["1.transaction amount and count of aggregated transaction",
                                                     "2.transaction amount and count of map transaction",
                                                     "3.transaction amount and count of top transaction",
                                                     "4.transaction count of aggregated user",

                                                     ])
      if question =="1.transaction amount and count of aggregated transaction":
            st.subheader("TRANSACTION AMOUNT")
            top_chart_transaction_amount("aggregated_transaction")
            st.subheader("TRANSACTION count")
            top_chart_transaction_count("aggregated_transaction")
      elif question =="2.transaction amount and count of map transaction":
            st.subheader("TRANSACTION AMOUNT")
            top_chart_transaction_amount1("map_transaction")
            st.subheader("TRANSACTION count")
            top_chart_transaction_count1("top_transaction")
      elif question =="3.transaction amount and count of top transaction":
            st.subheader("TRANSACTION AMOUNT")
            top_chart_transaction_amount("top_transaction")
            st.subheader("TRANSACTION count")
      elif question =="4.transaction count of aggregated user":
           st.subheader("TRANSACTION count")
           top_chart_transaction_count1("aggregated_user")
    

    

