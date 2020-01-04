import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import folium
def q1(qq1,connection):
    start_year= input('Enter start year(YYYY) ')
    end_year = input('Enter end year(YYYY) ')
    crime_type = input('Enter crime type ')
    df = pd.read_sql('select month1,count(Incidents_Count) from (select distinct crime_incidents.Month as month1 from crime_incidents where typeof(month1) = \"integer\") left outer join (select * , crime_incidents.Month as month2 from crime_incidents where  crime_incidents.Year >=  ' + str(start_year) + ' AND crime_incidents.Year <=  ' + str(end_year) + ' AND crime_incidents.Crime_Type =  \"' + str(crime_type) + '\" ) on month1 = month2 group by month1', connection)
    plot = df.plot.bar(x="month1")
    plt.plot()
    plt.savefig('Q1-'+str(qq1)+'.png')
 
def q2(qq2,conn):
    m = folium.Map(location=[53.5444,-113.323], zoom_start=11)#connect map
    c=conn.cursor()#create cursor
    a=input('Enter number of locations: ')
    #to select top neighbourhood
    c.execute('select (population.CANADIAN_CITIZEN+population.NON_CANADIAN_CITIZEN+population.NO_RESPONSE) as number,population.Neighbourhood_Name,coordinates.Latitude,coordinates.Longitude from population,coordinates  where population.Neighbourhood_Name=coordinates.Neighbourhood_Name and number <> 0 and (coordinates.Latitude<>0 or coordinates.Longitude<>0) order by population.CANADIAN_CITIZEN+population.NON_CANADIAN_CITIZEN+population.NO_RESPONSE desc limit :a;',{"a":a})
    rows=c.fetchall()#get result
    #draw circles
    for i in range(0,len(rows)-1):
        folium.Circle(
        location=[rows[i][2], rows[i][3]], # location
        
        popup=str(rows[i][1])+"<br>"+str(rows[i][0]) , # popup text
        radius= 0.1*rows[i][0], # size of radius in meter
        color= 'crimson', # color of the radius
        fill= True, # whether to fill the map
        fill_color= 'crimson' # color to fill with
        ).add_to(m)
        
    
    #to select last neighbourhood
    c.execute('select (population.CANADIAN_CITIZEN+population.NON_CANADIAN_CITIZEN+population.NO_RESPONSE) as number,population.Neighbourhood_Name,coordinates.Latitude,coordinates.Longitude from population ,coordinates  where population.Neighbourhood_Name=coordinates.Neighbourhood_Name and number <> 0 and (coordinates.Latitude<>0 or coordinates.Longitude<>0) order by population.CANADIAN_CITIZEN+population.NON_CANADIAN_CITIZEN+population.NO_RESPONSE asc limit :a;',{"a":a})
    rows2 = c.fetchall()
    if len(rows) !=0 and len(rows2)!=0:
        for i in range(0,len(rows2)-1):
            folium.Circle(
            location=[rows2[i][2], rows2[i][3]], # location
                
            popup=str(rows2[i][1])+"<br>"+str(rows2[i][0]) , # popup text
            radius= 0.1*rows2[i][0], # size of radius in meter
            color= 'crimson', # color of the radius
            fill= True, # whether to fill the map
            fill_color= 'crimson' # color to fill with
            ).add_to(m)
            
        lasttop = rows[len(rows)-1][0]
        lastmin = rows2[len(rows2)-1][0]
        #deal with tie cases
        c.execute('select (population.CANADIAN_CITIZEN+population.NON_CANADIAN_CITIZEN+population.NO_RESPONSE) as number,population.Neighbourhood_Name,coordinates.Latitude,coordinates.Longitude from population ,coordinates  where population.Neighbourhood_Name=coordinates.Neighbourhood_Name and number <> 0 and (coordinates.Latitude<>0 or coordinates.Longitude<>0) and (number=:a or number=:b);',{"a":int(lasttop),"b":int(lastmin)})
        rows3=c.fetchall()
        s=len(rows3)
        for i in range(len(rows3)):
            folium.Circle(
            location=[rows3[i][2], rows3[i][3]], # location
                
            popup=str(rows3[i][1])+"<br>"+str(rows3[i][0]) , # popup text
            radius= 0.1*rows3[i][0], # size of radius in meter
            color= 'crimson', # color of the radius
            fill= True, # whether to fill the map
            fill_color= 'crimson' # color to fill with
            ).add_to(m)
        
    m.save('Q2-'+str(qq2)+'.html')
    conn.commit()	
    
def q3(qq3,conn):
    m = folium.Map(location=[53.5444,-113.323], zoom_start=11)#connect map
    c=conn.cursor()#create cursor
    #get input
    start_year= input('Enter start year(YYYY) ')
    end_year = input('Enter end year(YYYY) ')
    crime_type = input('Enter crime type ')
    number=input('Enter number of neighborhoods ')
    #to select top crime count neighbourhood
    c.execute("select crime_incidents.Neighbourhood_Name, SUM(crime_incidents.Incidents_Count) as number ,coordinates.Latitude,coordinates.Longitude from crime_incidents,coordinates where crime_incidents.Year >=:a AND crime_incidents. Year <= :b AND crime_incidents.Crime_Type = :c and crime_incidents.Neighbourhood_Name=coordinates.Neighbourhood_Name and(coordinates.Latitude<>0 or coordinates.Longitude<>0) group by crime_incidents.Neighbourhood_Name order by number DESC LIMIT :d;", {"a":int(start_year),"b":int(end_year),"c":crime_type,"d":number})
    rows=c.fetchall()
    for i in range(0,len(rows)-1):
        folium.Circle(
        location=[rows[i][2], rows[i][3]], # location
        
        popup=str(rows[i][0])+"<br>"+str(rows[i][1]) , # popup text
        radius= 2*rows[i][1], # size of radius in meter
        color= 'crimson', # color of the radius
        fill= True, # whether to fill the map
        fill_color= 'crimson' # color to fill with
        ).add_to(m)
    if len(rows)!=0:
        lasttop=int(rows[len(rows)-1][1])
        #deal with tie cases
        c.execute("select Neighbourhood_Name,number ,Latitude,Longitude from (select crime_incidents.Neighbourhood_Name, SUM(crime_incidents.Incidents_Count) as number ,coordinates.Latitude,coordinates.Longitude from crime_incidents,coordinates where crime_incidents.Year >=:a AND crime_incidents. Year <= :b AND crime_incidents.Crime_Type = :c and crime_incidents.Neighbourhood_Name=coordinates.Neighbourhood_Name and (coordinates.Latitude<>0 or coordinates.Longitude<>0) group by crime_incidents.Neighbourhood_Name) where number=:d;", {"a":int(start_year),"b":int(end_year),"c":crime_type,"d":lasttop})
        rows2=rows=c.fetchall()
    
        for i in range(len(rows2)):
            folium.Circle(
            location=[rows2[i][2], rows2[i][3]], # location
                
            popup=str(rows2[i][0])+"<br>"+str(rows2[i][1]) , # popup text
            radius= 2*rows2[i][1], # size of radius in meter
            color= 'crimson', # color of the radius
            fill= True, # whether to fill the map
            fill_color= 'crimson' # color to fill with
            ).add_to(m)
    m.save('Q3-'+str(qq3)+'.html')
    conn.commit()	
        
def q4(qq4,conn):
    m = folium.Map(location=[53.5444,-113.323], zoom_start=11)#connect map
    c=conn.cursor()#create cursor
    start_year= input('Enter start year(YYYY) ')
    end_year = input('Enter end year(YYYY) ')
    neighborhoods = input('Enter numebr of neighborhoods ')
    #to select the top radio neighbourhood
    c.execute('select population.Neighbourhood_Name,max(crime_incidents.Incidents_Count),crime_incidents.Crime_Type,coordinates.Latitude,coordinates.Longitude,cast(sum(crime_incidents.Incidents_Count)as float)/(population.CANADIAN_CITIZEN+population.NON_CANADIAN_CITIZEN+population.NO_RESPONSE)as number from population,crime_incidents,coordinates where crime_incidents.Year >=:a AND crime_incidents.Year <= :b and population.Neighbourhood_Name=crime_incidents.Neighbourhood_Name and (population.CANADIAN_CITIZEN+population.NON_CANADIAN_CITIZEN+population.NO_RESPONSE) <>0 and (coordinates.Latitude<>0 or coordinates.Longitude<>0)and population.Neighbourhood_Name=coordinates.Neighbourhood_Name group by population.Neighbourhood_Name order by number desc limit :c',{"a":int(start_year),"b":int(end_year),"c":int(neighborhoods)})
    rows=c.fetchall()
    if len(rows)!=0:
        lasttop=rows[int(neighborhoods)-1][5]
        #to select the most frenquntly crime type
        for i in range(len(rows)):
            s=''
            c.execute('select Crime_Type from (select crime_incidents.Crime_Type ,sum(crime_incidents.Incidents_Count)as number from crime_incidents  where crime_incidents.Year >=:a AND crime_incidents.Year <=:b and crime_incidents.Neighbourhood_Name=:d group by crime_incidents.Crime_Type) where number = (select max(number) from (select crime_incidents.Crime_Type ,sum(crime_incidents.Incidents_Count)as number from crime_incidents  where crime_incidents.Year >=:a AND crime_incidents.Year <=:b and crime_incidents.Neighbourhood_Name=:d group by crime_incidents.Crime_Type))',{"a":int(start_year),"b":int(end_year),"d":rows[i][0]})
            rows2=c.fetchall()
            
            for j in range(len(rows2)):
                s=s+'<br>'+rows2[j][0]
    
            folium.Circle(
            location=[rows[i][3], rows[i][4]], # location
            
            popup=str(rows[i][0])+s+"<br>"+str(rows[i][5]) , # popup text
            radius= 1000*rows[i][5], # size of radius in meter
            color= 'crimson', # color of the radius
            fill= True, # whether to fill the map
            fill_color= 'crimson' # color to fill with
            ).add_to(m)    
        #to deal with tie cases
        c.execute('select Neighbourhood_Name,Latitude,Longitude,number from(select population.Neighbourhood_Name,coordinates.Latitude,coordinates.Longitude,cast(sum(crime_incidents.Incidents_Count)as float)/(population.CANADIAN_CITIZEN+population.NON_CANADIAN_CITIZEN+population.NO_RESPONSE)as number from population,crime_incidents,coordinates where crime_incidents.Year >=:a AND crime_incidents.Year <= :b and population.Neighbourhood_Name=crime_incidents.Neighbourhood_Name and population.Neighbourhood_Number<>0 and (coordinates.Latitude<>0 or coordinates.Longitude<>0)and population.Neighbourhood_Name=coordinates.Neighbourhood_Name group by population.Neighbourhood_Name) where number =:c',{"a":int(start_year),"b":int(end_year),"c":int(lasttop)})
        
        rows3=c.fetchall()
        # to find the most frenquntly crime type in tie cases
        for i in range(len(rows3)):
            s=''
            c.execute('select Crime_Type from (select crime_incidents.Crime_Type ,sum(crime_incidents.Incidents_Count)as number from crime_incidents  where crime_incidents.Year >=:a AND crime_incidents.Year <=:b and crime_incidents.Neighbourhood_Name=:d group by crime_incidents.Crime_Type) where number = (select max(number) from (select crime_incidents.Crime_Type ,sum(crime_incidents.Incidents_Count)as number from crime_incidents  where crime_incidents.Year >=:a AND crime_incidents.Year <=:b and crime_incidents.Neighbourhood_Name=:d group by crime_incidents.Crime_Type))',{"a":int(start_year),"b":int(end_year),"d":rows[i][0]})
            rows2=c.fetchall()
            
            for j in range(len(rows2)):
                s=s+'<br>'+rows2[j][0]
            folium.Circle(
            location=[rows3[i][1], rows3[i][2]], # location
            
            popup=str(rows[i][0])+s+"<br>"+str(rows[i][3]) , # popup text
            radius= 1000*rows[i][3], # size of radius in meter
            color= 'crimson', # color of the radius
            fill= True, # whether to fill the map
            fill_color= 'crimson' # color to fill with
            ).add_to(m)    
            
    m.save('Q4-'+str(qq4)+'.html')  
    conn.commit()

def main():
    qq1=0
    qq2=0
    qq3=0
    qq4=0    
    command = ''
    connection = sqlite3.connect('./' + input('Enter database name: '))
    while command != 'E':
        command = input('1:Q1\n2:Q2\n3:Q3\n4:Q4\nE:Exit\n')
        if command=='1':
            qq1=qq1+1
            q1(qq1,connection)
        if command=='2':
            qq2=qq2+1
            q2(qq2,connection)
        if command=='3':
            qq3=qq3+1
            q3(qq3,connection)
        if command=='4':
            qq4=qq4+1
            q4(qq4,connection)
    connection.close()
       
if __name__ == "__main__":
    main()