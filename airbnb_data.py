# Import Packages

import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import plotly_express as px
import plotly.graph_objects as go
import wordcloud
import matplotlib.pyplot as plt
from wordcloud import WordCloud


#ACCESSING CONNECT TO MYSQL

import mysql.connector         
mydb = mysql.connector.connect(host="localhost",user="root",password="",database="Airbnb")
print(mydb)
mycursor = mydb.cursor(buffered=True)
mycursor.execute('SET GLOBAL max_allowed_packet=1073741824')  #this is add due to the packet size is increased

#CSV FILES

df1=pd.read_csv(r'C:\Users\ADMIN\Desktop\raraj\Common_data.csv')
df2=pd.read_csv(r'C:\Users\ADMIN\Desktop\raraj\Amenitiesfunction.csv')
df3=pd.read_csv(r'C:\Users\ADMIN\Desktop\raraj\hostfunction')
df4=pd.read_csv(r'C:\Users\ADMIN\Desktop\raraj\Addressfunction.csv')
df5=pd.read_csv(r'C:\Users\ADMIN\Desktop\raraj\ReviewScorefunction.csv')
df6=pd.read_csv(r'C:\Users\ADMIN\Desktop\raraj\Reviews_table.csv')



st.set_page_config(
    page_title="Airbnb Data Analysis",
    layout="wide",
    initial_sidebar_state="expanded")

with st.sidebar:
    selected = option_menu(None,
                        ["HOME","EXPLORE DATA","INSIGHTS"],
                        icons=["house-door-fill","tools","card-text"],
                        default_index=0,
                        orientation="vertical",
                        styles={"nav-link":{"font-size": "20px", "text-align": "center", "margin": "0px", "--hover-color": " #FF8080"},
                        "icon": {"font-size": "30px"},
                        "container" : {"max-width": "6000px"},
                        "nav-link-selected": {"background-color": "#FF8080"}})
    
if selected == "HOME":
    st.markdown("<h1 style='text-align:center; color:indianred;'>AIRBNB ANALYSIS PROJECT</h1>", unsafe_allow_html=True)

    st.write("")
    st.write(":small_airplane: Welcome to Airbnb, a global community marketplace that offers unique accommodations and experiences around the world. Whether you're seeking a cozy apartment in the heart of a bustling city, a rustic cabin nestled in the mountains, or an exotic villa by the beach, Airbnb provides a platform where travelers can discover and book accommodations that suit their preferences and budget.")

    st.write(':small_airplane: With millions of listings spanning over 191 countries, Airbnb connects people to unforgettable travel experiences while empowering hosts to share their spaces and passions with guests from every corner of the globe. Come explore, connect, and belong anywhere with Airbnb.')

    st.subheader(':red[TECHNOLOGIES USED]')
    st.write(":small_airplane: Technologies used in this project include Python scripting, Data Preprocessing, Visualization, EDA, Streamlit,MySQL")

    st.write(":small_airplane: The project falls under the domain of Travel Industry, Property Management and Tourism.")

    st.subheader(':red[PROBLEM STATEMENT]')

    st.write(":small_airplane: This project aims to analyze Airbnb data to uncover valuable insights without focusing on specific technologies.You'll perform data cleaning, develop interactive geospatial visualizations, and create dynamic plots to understand pricing dynamics, availability patterns, and location-based trends.")
    st.write(":small_airplane: Explore the insights and visualizations provided by the Streamlit!")
    
                                                            #  DATA EXPLORATION   ###########
    
#    
elif selected=="EXPLORE DATA":
    st.markdown("<h1 style='text-align:center; color:indianred;'>AIRBNB DATA ANALYSIS</h1>", unsafe_allow_html=True)
    
    on = st.toggle(":red[**Availability Analysis**]")   
    if on:  
        sql = pd.read_sql("SELECT host_table.Host_Name ,availability_table.Availability_30,Availability_60 FROM availability_table JOIN host_table ON availability_table.Id = host_table.Id;", mydb)
        fig1 = px.line(sql,
                        x="Availability_30",
                        y="Availability_60",
                        title="Availability over 30 Days vs 60 Days",
                        width=1300, height=700,
                        labels={"Availability_30": "Availability 30 Days", "Availability_60": "Availability 60 Days"})

        fig1.update_traces(mode='markers') 

        fig1.update_layout(xaxis_title='Availability 30 Days', yaxis_title='Availability 60 Days')

        st.plotly_chart(fig1)
        
        sql2 = pd.read_sql("SELECT common_datas.Name,availability_table.Availability_90,Availability_365 FROM availability_table JOIN common_datas ON availability_table.Id = common_datas.Id WHERE availability_table.Availability_365 < 100 GROUP BY Availability_365;", mydb)
        
        fig2 = px.scatter(sql2, x='Availability_90', y='Availability_365', title='Availability (90 Days) vs Availability (365 Days)',color_discrete_sequence=['brown'])
        
        st.plotly_chart(fig2)
        
    secondon = st.toggle(":red[**Price Analysis**]")
    if secondon:
        sql3 = pd.read_sql('SELECT Government_Area, Country FROM airbnb.address_table ORDER BY Street DESC LIMIT 10;', mydb)
        
        fig2 = px.pie(sql3, names='Government_Area', title='Top 10 Government Areas by Country',color_discrete_sequence=['pink'])
        
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        
        fig2.update_layout(showlegend=True)
        
        st.plotly_chart(fig2)
        
        ###########################          Average Price by Property Type         ##############################
        
        avg_price_by_type = df1.groupby("Property_type")["Price"].mean()
        
        fig3 = px.line(
            avg_price_by_type.reset_index(),
            x="Property_type",
            y="Price",
            title="Average Price by Property Type in Airbnb Data",width=1300,height=700,
            labels={"Property_type": "Property Type", "Price": "Average Price"},color_discrete_sequence=['purple'])
        
        fig3.update_traces(mode='markers+lines') 
        
        fig3.update_layout(xaxis_title='Property Type', yaxis_title='Average Price')
        
        st.plotly_chart(fig3)
        
        
                                                        ### MAX CLEANING FEE DETAILS   ################
                                                        
                                                        
        max_cleaning_fee = df1.groupby('Name').agg({'ExtraPeople': 'max', 'Guests': 'max', 'CleaningFee': 'max'}).max()
        
        fig4 = px.bar(x=max_cleaning_fee.index, y=max_cleaning_fee.values, labels={'x': 'Category', 'y': 'Maximum Value'}, title='Maximum Values by Category',color_discrete_sequence=['mediumaquamarine'])
        
        st.plotly_chart(fig4)                                               
                                                        #### ACCOMODATION ############
                                                        
        grouped_data = df1.groupby('Accomodation').agg({'Name': 'first',  
            'Description': 'first',  
            'Minimum_night': 'min',  
            'Maximum_night': 'max'}).reset_index()
        fig5 = px.box(grouped_data, x='Accomodation', y=['Minimum_night', 'Maximum_night'],
                hover_data=['Name', 'Description'],title='Minimum vs Maximum Value by Accomodation',color_discrete_sequence=['yellow'])
        
        st.plotly_chart(fig5)
        
        
                                            ##########    HOST NAME DETAILS ##################
                                            
        lastgr = df3.groupby('Host_Name')['Host_verification'].nunique().head(10).reset_index()

        chart = px.bar(lastgr, 
            x='Host_Name', 
            y='Host_verification', 
            color='Host_verification', 
            title='Average Host Verification for Top 10 Hosts',
            labels={'Host_Name': 'Host Name', 'Host_verification': 'Host Verification'},
            width=1300, 
            height=700,
            color_discrete_sequence=px.colors.qualitative.Pastel1)
        chart.update_layout(xaxis_tickangle=-45)

        st.plotly_chart(chart)    
        
                                                ######## HOST LOCATION ######################
        
        dfw=df3.groupby('Host_location')['Host_neighbourhood'].min().head(5)

        fig = px.scatter(dfw.reset_index(), x='Host_location', y='Host_neighbourhood',
                        color="Host_neighbourhood",title='Minimum Host Neighborhood by Host Location')
        
        fig.update_traces(mode='markers+lines',marker_color='green')

        st.plotly_chart(fig)         
        
                                                    ###########   Geo visualisation #######################
                                                    
    one = st.toggle(":red[**Geo visualisation**]")
    if one:
        df_filtered = pd.read_sql("SELECT Longitude, Latitude, Market, Government_Area FROM airbnb.address_table WHERE Market ='New York' ORDER BY Government_Area DESC LIMIT 10;",mydb)
        fig = px.scatter_mapbox(df_filtered, lat="Latitude", 
            lon="Longitude", color="Government_Area",hover_name="Market", 
            hover_data={"Government_Area": True, "Market": True},
            color_discrete_sequence=['brown'],zoom=1,
            width=1300,height=700)
        
        fig.update_layout(mapbox_style="carto-darkmatter",title="Listing Availability by Location")
        st.plotly_chart(fig)

            #----------------------------------------Reviews Details----------------------------------------#
    reviews=st.toggle(":red[**Review Rating Analysis**]")
    if reviews:
        rev = df6.groupby('ReviewerName')['Comment'].count().reset_index()

        figs = px.bar(rev, x='ReviewerName', y='Comment', hover_data=['Comment'],
                    labels={'ReviewerName':'ReviewerName','Comment':'Comment'},
                    title='Comment Counts by Reviewer',width=1200,height=600,color_discrete_sequence=['saddlebrown'])
        
        st.plotly_chart(figs)

            #------------------------------#ReviewScores Details----------------------------------------#
        grouped_df = df5.groupby(['ReviewScoreValue','ReviewScoreRating','ReviewScoreLocation']).size().reset_index()

        grouped_df.columns = ['ReviewScoreValue','ReviewScoreRating', 'ReviewScoreLocation','Count']

        violin_fig = px.violin(grouped_df, x='ReviewScoreRating', y='Count',
            title='Violin Plot of Review Counts by Rating',color_discrete_sequence=['lawngreen'],
            labels={'ReviewScoreRating': 'Review Score Rating', 'Count': 'Count'})
        
        st.plotly_chart(violin_fig)

            #------------------------------#ReviewScores Details----------------------------------------#
        new_df = df5.groupby(['ReviewScoreChecking', 'ReviewScoreAccuracy', 'ReviewScoreCleanliness']).median().reset_index()
        fig = px.scatter_3d(new_df, 
                            x='ReviewScoreChecking', 
                            y='ReviewScoreAccuracy', 
                            z='ReviewScoreCleanliness', 
                            color='ReviewScoreChecking',
                            size_max=10, 
                            opacity=0.7)
        
        fig.update_layout(scene=dict(
                            xaxis_title='Review Score Checking',
                            yaxis_title='Review Score Accuracy',
                            zaxis_title='Review Score Cleanliness'),
                            width=800,
                            height=700,
                            title='3D Scatter Plot of Review Scores')
        
        
        st.plotly_chart(fig)
                                        ####### INSIGHTS #######################
                                                
elif selected=="INSIGHTS":
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
            
            st.pyplot(plt)


