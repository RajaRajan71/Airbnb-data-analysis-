import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import mysql.connector
from sqlalchemy import create_engine
import pandas as pd
import plotly_express as px
import plotly.graph_objects as go
import wordcloud
import matplotlib.pyplot as plt
from wordcloud import WordCloud



# Setting up page configuration

st.set_page_config(page_title= "Airbnb Data Visualization | By Jafar Hussain",
                
                layout= "wide",
                initial_sidebar_state= "expanded")


# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Overview","Explore","INSIGHTS"], 
                        icons=["house","graph-up-arrow","bar-chart-line"],
                        menu_icon= "menu-button-wide",
                        default_index=0,
                        styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#FF5A5F"},
                                "nav-link-selected": {"background-color": "#FF5A5F"}})
    

#ACCESSING CONNECT TO MYSQL

import mysql.connector         
mydb = mysql.connector.connect(host="localhost",user="root",password="",database="Airbnb")
print(mydb)
mycursor = mydb.cursor(buffered=True)
mycursor.execute('SET GLOBAL max_allowed_packet=1073741824')  #this is add due to the packet size is increased



#CSV FILES
df1=pd.read_csv(r'C:\Users\ADMIN\Desktop\raraj\Common_dataa.csv')
df2=pd.read_csv(r'C:\Users\ADMIN\Desktop\raraj\Amenitiesfunction.csv')
df3=pd.read_csv(r'C:\Users\ADMIN\Desktop\raraj\hostfunction')
df4=pd.read_csv(r'C:\Users\ADMIN\Desktop\raraj\Addressfunction.csv')
df5=pd.read_csv(r'C:\Users\ADMIN\Desktop\raraj\ReviewScorefunction.csv')
df6=pd.read_csv(r'C:\Users\ADMIN\Desktop\raraj\Reviews_table.csv')
df7=pd.read_csv(r'C:\Users\ADMIN\Desktop\raraj\AvailabilityDataa.csv')


# HOME PAGE
if selected == "Home":
    st.markdown("<h1 style='text-align:center; color:indianred;'>AIRBNB ANALYSIS PROJECT</h1>", unsafe_allow_html=True)

    st.write("")
    st.write(":small_airplane: Welcome to Airbnb, a global community marketplace that offers unique accommodations and experiences around the world. Whether you're seeking a cozy apartment in the heart of a bustling city, a rustic cabin nestled in the mountains, or an exotic villa by the beach, Airbnb provides a platform where travelers can discover and book accommodations that suit their preferences and budget.")
    

    st.write(' With millions of listings spanning over 191 countries, Airbnb connects people to unforgettable travel experiences while empowering hosts to share their spaces and passions with guests from every corner of the globe. Come explore, connect, and belong anywhere with Airbnb.')
    st.write("  Travel Industry, Property Management and Tourism")
    
    st.write(" Python, Pandas, Plotly, Streamlit,MYSQL")
    
    st.write(" To analyze Airbnb data using MYSQL, perform data cleaning and preparation, develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends. ")
    
# OVERVIEW PAGE
if selected == "Overview":
    
    tab1 = st.tabs(["APP MODULE"])
    
    # INSIGHTS TAB
    # GETTING USER INPUTS
    country = st.sidebar.multiselect('Select a Country', sorted(df4.Country.unique()), sorted(df4.Country.unique()))
    property = st.sidebar.multiselect('Select Property_type', sorted(df1.Property_type.unique()), sorted(df1.Property_type.unique()))
    room = st.sidebar.multiselect('Select Room_type', sorted(df1.Room_type.unique()), sorted(df1.Room_type.unique()))
    price = st.slider('Select Price', df1.Price.min(), df1.Price.max(), (df1.Price.min(), df1.Price.max()))
        
    # CONVERTING THE USER INPUT INTO QUERY
    query = f'Country in {country} & Room_type in {room} & Property_type in {property} & Price >= {price[0]} & Price <= {price[1]}'
    
    # CREATING COLUMNS
    col1,col2 = st.columns(2,gap='medium')
    
    with col1:
        # TOP 10 PROPERTY TYPES BAR CHART
        sql_query1 =( """SELECT Property_type, SUM(Price) AS Total_Price 
                FROM common_datas 
                GROUP BY Property_type 
                ORDER BY Total_Price DESC 
                LIMIT 10;""" )
        mycursor.execute(sql_query1)
        myresult = mycursor.fetchall()
        df = pd.DataFrame(myresult, columns=['Property_type', 'Total_Price'])
        mydb.close()
        st.write(df)
        
        fig1 = px.bar(df,
                title='Top 10 Property Types',
                x='Property_type',
                y='Total_Price', 
                orientation='v',
                color='Property_type',
                color_continuous_scale=px.colors.sequential.Viridis)
        st.plotly_chart(fig1, use_container_width=True)
        
        
        # TOP 10 ID HOSTS BAR CHART
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="airbnb"
        )
        mycursor = mydb.cursor()
        
        sql_query2= (""" SELECT HostId , Host_listing_count AS total_listing 
                    FROM airbnb.host_table  
                    GROUP BY HostId 
                    ORDER BY total_listing DESC 
                    LIMIT 10; """)
        mycursor.execute(sql_query2)
        myresult = mycursor.fetchall()
        df2 = pd.DataFrame(myresult, columns=['HostId', 'Host_listing_count'])
        st.write(df2)
        
        fig2 = px.bar(df2,
                        title='Top 10 Hosts with Highest number of Listings',
                        x='HostId',
                        y='Host_listing_count',
                        orientation='v',
                        color='HostId',
                        color_continuous_scale=px.colors.sequential.Agsunset)
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2,use_container_width=True)
        
    with col2:
        # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
        sql_query3=("SELECT Room_type, COUNT(*) AS total_listings FROM common_datas GROUP BY Room_type; ")
        mycursor.execute(sql_query3)
        myresult = mycursor.fetchall()
        df3 = pd.DataFrame(myresult, columns=['Room_type', 'counts'])
        
        fig3 = px.pie(df3,
                        title='Total Listings in each counts',
                        names='Room_type',
                        values='counts',
                        color_discrete_sequence=px.colors.sequential.Rainbow
                        )
        fig3.update_traces(textposition='outside', textinfo='value+label')
        st.plotly_chart(fig3,use_container_width=True)
        st.write(df3)
            
        # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
        sql_query4=(("SELECT Country, COUNT(*) AS total_listings FROM address_table GROUP BY Country;"))
        mycursor.execute(sql_query4)
        myresult = mycursor.fetchall()
        df4 = pd.DataFrame(myresult, columns=['Country','total_listings'])
        
        fig4 = px.choropleth(df4,
                                title='Total Listings in each Country',
                                locations='Country',
                                locationmode='country names',
                                color='total_listings',
                                color_continuous_scale=px.colors.sequential.Plasma
                            )
        st.plotly_chart(fig4,use_container_width=True)
        st.write(df4)
# EXPLORE PAGE
if selected == "Explore":
    st.markdown("## Explore more about the Airbnb data")
    
    # GETTING USER INPUTS
    country = st.sidebar.multiselect('Select a Country',sorted(df4.Country.unique()),sorted(df4.Country.unique()))
    prop = st.sidebar.multiselect('Select Property_type',sorted(df1.Property_type.unique()),sorted(df1.Property_type.unique()))
    room = st.sidebar.multiselect('Select Room_type',sorted(df1.Room_type.unique()),sorted(df1.Room_type.unique()))
    price = st.slider('Select Price',df1.Price.min(),df1.Price.max(),(df1.Price.min(),df1.Price.max()))
    
    
    # CONVERTING THE USER INPUT INTO QUERY
    query2 = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'
    
    # HEADING 1
    st.markdown("## Price Analysis")
    
    # CREATING COLUMNS
    col1,col2 = st.columns(2,gap='medium')
    
    
    with col1:
        
        # AVG PRICE BY ROOM TYPE BARCHART
        sql_query5=("SELECT Room_type,AVG(price) AS avg_price FROM common_datas GROUP BY Room_type;")
        mycursor.execute(sql_query5)
        myresult = mycursor.fetchall()
        df5 = pd.DataFrame(myresult, columns=['Room_type','Price'])
        fig5 = px.bar(df5,
                    x='Room_type',
                    y='Price',
                    color='Price',
                    title='Avg Price in each Room type'
                    )
        st.plotly_chart(fig5,use_container_width=True)
        st.write(df5)
        
        
        # HEADING 2
        st.markdown("## Property price Analysis")
        sql_query6= ( " SELECT Property_type, AVG(Price) as avg_price FROM common_datas GROUP BY Property_type DESC LIMIT 20;")
        mycursor.execute(sql_query6)
        myresult = mycursor.fetchall()
        df6= pd.DataFrame(myresult, columns=['Property_type','Price'])
        
        
        st.write("Top 20 Property Types by Average Price")
        st.write(df6)
        fig6 = px.bar(
        df6, 
        x='Property_type', 
        y='Price', 
        title='Top 20 Property Types by Average Price"', 
        labels={'Property_type': 'Property Type', 'Price': 'Average Price'},
        color='Price',  
        color_continuous_scale='Viridis'
        )
        # Display the bar chart in Streamlit
        st.plotly_chart(fig6)
        
        with col2:
            
        
            # AVG PRICE IN COUNTRIES SCATTERGEO
            sql_query7= ('SELECT Country, AVG(Price) AS avg_price FROM common_datas GROUP BY Country ORDER BY avg_price DESC;')
            mycursor.execute(sql_query7)
            myresult = mycursor.fetchall()
            df7= pd.DataFrame(myresult, columns=['Country','avg_price'])
            
            st.write(" Average price by countries")
            
            fig = px.choropleth(df7,
                                title='average price in countries',
                                locations='Country',
                                locationmode='country names',
                                color='avg_price',
                                color_continuous_scale=px.colors.sequential.Plasma
                            )
            st.plotly_chart(fig,use_container_width=True)
            
            st.write(df7)
            
                    # BLANK SPACE
            st.markdown("#   ")
            st.markdown("#   ")
            
            # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
            
            sql_query8=('SELECT Country,AVG(Availability_365) AS avg_availability FROM availability_table GROUP BY Country;')
            mycursor.execute(sql_query8)
            myresult = mycursor.fetchall()
            df8= pd.DataFrame(myresult, columns=['Country','Availability_365'])
            
            
            st.write(" Availability_365 by countries")
            
            fig8 = px.choropleth(df8,
                                title='Availability_365 by countries',
                                locations='Country',
                                locationmode='country names',
                                color='Availability_365',
                                color_continuous_scale=px.colors.sequential.Turbo
                            )
            st.plotly_chart(fig8,use_container_width=True)
            
            st.write(df8)
            

    
                            ###################### INSIGHTS ###########################
                                                
elif selected=="Insights":
        st.write("<h1 style='color:deeppink;text-align:center;'>INSIGHTS</h1>", unsafe_allow_html=True)
        
        
        options = ["--Select any of the Questions--","1.Which host locations have the highest number of hosts registered?",
                "2.What is the geographical spread (using Longitude and Latitude) of addresses within a specific Government_Area?",
                "3.Are there any noticeable trends in availability rates over different time periods (30 days, 60 days, etc.)?",
                "4.Are there any markets that have the same minimum suburb name?",
                "5.Which reviewers submitted reviews on the most recent 30 dates, and what are their names?",
                "6.Are there Rating Types with consistently high or low ratings?",
                "7.What is the distribution of accommodations based on price ranges?",
                "8.What are the host neighbourhood have more than five listings and the number of listings falls within the range of 1 to 30?",
                "9.Which government areas have specific amenities available?"]
        
        select = st.selectbox("Select the option", options)
        
        if select=='1.Which host locations have the highest number of hosts registered?':
            mycursor.execute('SELECT Host_location,COUNT(*) AS Host_location_Count FROM host_table GROUP BY Host_location ORDER BY Host_location_Count DESC LIMIT 10;')
            hostdb=mycursor.fetchall()

            df1 = pd.DataFrame(hostdb, columns=['Host_location', 'Host_location_Count'])

            fig1 = px.bar(df1, x='Host_location_Count', y='Host_location', orientation='h',
                        title='Top 10 Host Locations by Count',color_discrete_sequence=['palevioletred'])

            fig1.update_layout(xaxis_title='Count', yaxis_title='Host Location')
            st.write(df1)

            st.plotly_chart(fig1, use_container_width=True)
            
        elif select=='2.What is the geographical spread (using Longitude and Latitude) of addresses within a specific Government_Area?':
            mycursor.execute("SELECT Longitude, Latitude, Market, Government_Area FROM address_table WHERE Market='Rio De Janeiro' ORDER BY Government_Area DESC LIMIT 10;")
            data = mycursor.fetchall()

            df2 = pd.DataFrame(data, columns=['Longitude', 'Latitude', 'Market', 'Government_Area'])

            fig2 = px.scatter_mapbox(df2, lat='Latitude', lon='Longitude', hover_name='Government_Area', hover_data=['Market'],color='Market',
                                    color_discrete_sequence=["crimson"], zoom=10, height=500, title='Top 10 Locations in Rio De Janeiro by Government Area')

            fig2.update_layout(mapbox_style="open-street-map")
            st.write(df2)

            st.plotly_chart(fig2, use_container_width=True)
            
        elif select=='3.Are there any noticeable trends in availability rates over different time periods (30 days, 60 days, etc.)?':
            mycursor.execute('SELECT "30 Days" AS Time_Period,AVG(Availability_30) AS Avg_Availability FROM availability_table UNION SELECT "60 Days" AS Days,AVG(Availability_60) AS Avg_Availability FROM availability_table UNION SELECT "90 Days" AS Time_Period,AVG(Availability_90) AS Avg_Availability FROM availability_table UNION SELECT "365 Days" AS Time_Period,AVG(Availability_365) AS Avg_Availability FROM availability_table;')
            newdata=mycursor.fetchall()

            df3 = pd.DataFrame(newdata, columns=['Time_Period', 'Avg_Availability'])

            df3['Category'] = 'Availability'

            fig3 = px.parallel_categories(df3, dimensions=['Category', 'Time_Period'], color='Avg_Availability',
                                        color_continuous_scale='Inferno', title='Average Availability Across Different Time Periods')
            st.write(df3)
            st.plotly_chart(fig3, use_container_width=True)
            
        elif select =="4.Are there any markets that have the same minimum suburb name?":
            mycursor.execute("SELECT Market, MIN(Country_code) as Country_code, MIN(SubUrb) as SubUrb, is_location_exact FROM address_table WHERE Country_code = 'US' GROUP BY Market ORDER BY MIN(SubUrb), is_location_exact;")
            data = mycursor.fetchall()

            df4 = pd.DataFrame(data, columns=['Market', 'Country_code', 'SubUrb', 'is_location_exact'])

            fig4 = px.scatter(df4, x='Market', y='SubUrb', color='is_location_exact',title='Minimum SubUrb Across Different Markets(Colored by Location Exactness)')

            fig4.update_xaxes(type='category')
            st.write(df4)

            st.plotly_chart(fig4, use_container_width=True)
            
        elif select=='5.Which reviewers submitted reviews on the most recent 30 dates, and what are their names?':
            mycursor.execute('SELECT ReviewerName AS Names, DATE(Date) AS Review_Date FROM reviews_table WHERE DATE(Date) BETWEEN "2010-01-01" AND "2012-12-31" GROUP BY Names LIMIT 30;')
            revdb=mycursor.fetchall()
            df5 = pd.DataFrame(revdb, columns=['Names', 'Review_Date'])

            fig5 = px.bar(df5, x='Names', y='Review_Date',
                        title='Number of Reviews by Reviewer',color_discrete_sequence=['goldenrod'],
                        labels={'Names': 'Reviewer Names', 'Review_Date': 'Number of Reviews'})

            fig5.update_layout(xaxis_title='Reviewer Names', yaxis_title='Number of Reviews')
            st.write(df5)

            st.plotly_chart(fig5, use_container_width=True)
            
        elif select=='6.Are there Rating Types with consistently high or low ratings?':

            mycursor.execute('SELECT MIN(ReviewScoreRating) as MinimumReviewScoreRating, MAX(ReviewScoreRating) as MaximumReviewScoreRating FROM reviewscores_table;')
            revscoredb = mycursor.fetchall()

            la = pd.DataFrame(revscoredb, columns=['MinimumReviewScoreRating', 'MaximumReviewScoreRating'])

            bar_fig = go.Figure()
            bar_fig.add_trace(go.Bar(
                y=['Minimum Review Score', 'Maximum Review Score'],
                x=[la['MinimumReviewScoreRating'][0], la['MaximumReviewScoreRating'][0]],
                orientation='h',marker=dict(color='darkgreen')))
            bar_fig.update_layout(
                title='Horizontal Bar Chart of Review Scores',
                xaxis_title='Review Score Rating',
                yaxis_title='Rating Type')
            st.write(df6)
            st.plotly_chart(bar_fig)
            
        elif select=='7.What is the distribution of accommodations based on price ranges?':
            mycursor.execute('''SELECT CASE WHEN Price <= 50 THEN '0-50' WHEN Price <= 100 THEN '51-100'
                WHEN Price <= 150 THEN '101-150' ELSE 'Over 150' END AS Price_Range,COUNT(*) AS Accommodation_Count FROM common_datas GROUP BY Price_Range;''')
            accomdb=mycursor.fetchall()
            df7 = pd.DataFrame(accomdb, columns=['Price_Range', 'Accommodation_Count'])
            donut_fig7 = px.pie(df7, names='Price_Range', values='Accommodation_Count', hole=0.5,color_discrete_sequence=["aqua"],
                title='Donut Chart of Accommodation Counts by Price Range')
            st.write(df7)
            
            st.plotly_chart(donut_fig7)
            
        elif select=='8.What are the host neighbourhood have more than five listings and the number of listings falls within the range of 1 to 30?':
            mycursor.execute('SELECT Host_neighbourhood, Host_profile, Host_listing_count FROM host_table WHERE Host_listing_count > 5 AND Host_listing_count BETWEEN 1 AND 30 GROUP by Host_neighbourhood;')
            host_neighdb=mycursor.fetchall()
            df8=pd.DataFrame(host_neighdb,columns=['Host_neighbourhood','Host_profile','Host_listing_count'])
            scatter_fig8 = px.scatter(df8, x='Host_listing_count', y='Host_neighbourhood', color='Host_neighbourhood',
                        title='Scatter Plot of Host Listing Count by Neighborhood and Profile',
                        labels={'Host_listing_count': 'Listing Count', 'Host_neighbourhood': 'Neighborhood'})
            st.write(df8)
            
            st.plotly_chart(scatter_fig8)
            
        elif select=='9.Which government areas have specific amenities available?':
            mycursor.execute('SELECT amenities.AmenitiesId, amenities.Amenities, address_table.Government_Area FROM amenities JOIN address_table ON amenities.AmenitiesId = address_table.Id;')
            amenities=mycursor.fetchall()

            df9 = pd.DataFrame(amenities, columns=['AmenitiesId', 'Amenities', 'Government_Area'])
            # Group amenities by government area and join them into a single string
            wordcloud_data = df9.groupby('Government_Area')['Amenities'].apply(' '.join).reset_index()
            # Create a WordCloud object
            wordcloud = WordCloud(width=800, height=400, background_color='white')
            # Generate   
            wordcloud.generate(' '.join(wordcloud_data['Amenities']))
            # Display the word cloud
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.title('Word Cloud of Amenities Across Government Areas')
            plt.axis('off')
            st.write(df9)
            st.pyplot(plt)
