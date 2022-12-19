def main(now,then):
    while 1:
        now = dt.now()
        
        if (now - then).total_seconds() >= 10:
            print("plot cycle started")
            try:
                then = dt.now()
                #Fetch lists of time stamps and ratings and plot them
                dayLinePlotter(0,30)

                #Fetch lists of time stamps and ratings for console1 and plot them
                dayLinePlotter(1,30)

                #Fetch list of ratings and plot them
                piePlotter    (0,365)

                #Fetch list of ratings for console1 and plot them
                piePlotter    (1,365)
                #^^ all of these take arguments: wildcard for the console, amount of days back
            except:
                print("error in plotting")
            now = dt.now()
            
            sleep(0.01)
            print("plot cycle ended")
            then = now
        


def dayLinePlotter(wild, days): #Produces a nice line graph
    
    listy = Sql.fetcher(wild,days,"xy")
    

    # Plot the Ratings.
    fig, ax = plt.subplots()

    
    ax.plot(listy[0], listy[1], c='red',  alpha=0.5)


    # Format plot.    

    #fetches the specified title and location from the argument via sql
    titlelocation = Sql.titlLocFetch(wild, days, listy[2])
    
    plt.title(titlelocation[0], fontsize=13.5)


    plt.xlabel('Day', fontsize=16)
    fig.autofmt_xdate()
    
    plt.ylabel('Rating', fontsize = 16)
    plt.tick_params(axis='both', which='major', labelsize=12)
   
    plt.grid(True)
    plt.tight_layout()
#savename
    dayer = str(days)
    if wild >= 1:
        savename = titlelocation[1] + f"-Line{dayer}Days.png"
        plt.savefig('static/'+savename)
    else:
        plt.savefig(f'static/AllLine{dayer}Days.png')
    #plt.show()
    plt.close()



def piePlotter(wild, days):

    x = Sql.fetcher(wild,days, "y")
        
        
    
    count = x[0] + x[1] + x[2]    


    labels = 'Poor', 'Medium', 'Good'
    poor = x[0]
    medium = x[1]
    good = x[2]
    
    sizes = [poor, medium, good]
    explode = (0.02, 0.02, 0.08)  # only "explode" the 3rd slice ('good')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    


    #fetches the specified terminal from the argument via sql
    titlelocation=Sql.titlLocFetch(wild,days,count)
    plt.title(titlelocation[0], fontsize=15)

    plt.subplots_adjust()
    #savename
    dayer = str(days)
    #print("day count and titles: ",dayer, titlelocation, "\n")

    if wild >= 1:
        savename = titlelocation[1] + f"-{dayer}DaysPie.png"
        plt.savefig('static/'+savename)
    else:
        plt.savefig(f'static/All{dayer}DaysPie.png')
    #plt.show()
    
    plt.close()



def on_connect(client, userdata, flags, rc):
    if rc==0:
        print(f"MQTT connected with code {str(rc)}")
        client.subscribe("Project3/#")

    else:
        print("MQTT connection Error: Returned code=",rc)


#Callback for msg
def on_message(client,userdata,msg):
    
    try:
        if (msg.topic == "Project3/Console"):
            load = str(msg.payload)
            load = load.strip("b'")
            x = load.split("&")
            rating = float(x[0])
            address = str(x[1])
            print ("rating received: ",rating,",  from: ", address)
            Sql.inserter(rating, address,True)
            if address not in Sql.macList:
                Sql.inserter("N/A",address, False)

    except Exception as e:
        print("Error in payload: ",e)
        print(f"{msg.topic} {msg.payload}")





    




if __name__ == "__main__":
    
    #Importing classesSELECT User, Host FROM mysql.user
    from sqller import Sqller

    #MQTT
    import paho.mqtt.client as mqtt
    
    #MariaDB
    import mariadb, sys

    #Datetime
    from datetime import timedelta as td
    from datetime import datetime as dt

    #Sleep
    from time import sleep

    #MatPlotLib
    from matplotlib import pyplot as plt
    from matplotlib.ticker import PercentFormatter
    from matplotlib import colors

    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.username_pw_set("group4", "group4four")
        client.connect("127.0.0.1")
        
    except:
        print("mqtt connection error")
    


    #mariadb
    try:
        conn = mariadb.connect(
            
            user="group4",
            password="group4four",
            host="127.0.0.1",
            port=3306,
            database="group4",
            autocommit=True
        )
        print("mariadb connected with code 0")
    except mariadb.Error as e:
        print(f"Connection error, code: {e}")
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor()


    Sql = Sqller(conn,cur)

    then = dt.now()
    now  = dt.now()
    client.loop_start()
    main(now,then)
