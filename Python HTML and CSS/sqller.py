class Sqller:
    def __init__(self,conn,cur):
        self.__cur = cur
        self.__conn = conn
        self.__cur.execute("SELECT macAddress from group4.locations ORDER by id")
        self.__macList0 = self.__cur.fetchall()
        self.macList =  []
        for mac in self.__macList0:
            self.macList.append(mac[0])
        del(self.__macList0)
        print("known mac addresses: ", self.macList)

    def inserter(self,rating,macAddress, known):
        if known == True:
            self.__cur.execute("INSERT INTO group4.console( rating, macAddress) VALUES(?,?)", (rating, macAddress))
        if known == False:
            print("unknown mac: ",macAddress, " inserting in group4.locations")
            self.__cur.execute("INSERT INTO group4.locations(location, macAddress) VALUES(?,?)", (rating, macAddress))
            print("updated mac addresses: ", self.macList)


    def fetcher(self, wild, days, xy): #wildcard for console number, 0 is all, day count, x or y for plot
        
        

        if xy == "y":
            
            if wild >= 1:
                wild += -1
                self.__cur.execute(f"SELECT rating FROM group4.console WHERE macAddress='{self.macList[wild]}' and ts >= DATE_SUB(CURDATE(), INTERVAL {days} DAY) ")                       

            else:
                self.__cur.execute(f"SELECT rating FROM group4.console WHERE ts >= DATE_SUB(CURDATE(), INTERVAL {days} DAY)")
                
            self.__ratings = self.__cur.fetchall()    
            
            self.__ratings2 = self.algore2(self.__ratings)
            

            return self.__ratings2

        
        elif xy == "xy":
            
            if wild >= 1: 
                wild += -1
                self.__cur.execute(f"SELECT ts, rating FROM group4.console WHERE macAddress= '{self.macList[wild]}' and ts >= DATE_SUB(CURDATE(), INTERVAL {days} DAY) ")
                # COULD ORDER BY INDEX NUMBER ON RPI, DATETIME IS OUT OF ORDER

            else:
                self.__cur.execute(f"SELECT ts, rating FROM group4.console WHERE ts >= DATE_SUB(CURDATE(), INTERVAL {days} DAY) ")#ORDER BY idx")
            self.__raw = self.__cur.fetchall()    
            
            self.__raw.sort()
            listy = self.algoreithm( self.__raw)
            return listy



    def titlLocFetch(self, wild, days, count):
        
        if wild >= 1:
            wild += -1
            self.__cur.execute(f"SELECT location FROM group4.locations where macAddress = '{self.macList[wild]}'") # rating from group4.console topic like [insert topic] and mac like [insert mac])
            self.__loc  = self.__cur.fetchall()

            self.__loc1 = ""
            self.__loc1 = str(self.__loc[0]).strip("('')}{,")    

            self.__title = f"Ratings from classroom: {self.__loc1} for the past {days} day(s)\n Total rating(s): {count}" #**********

            #From all terminals    
        else:
            self.__title = f"Ratings from all locations for the past {days} day(s)\n Total rating(s): {count}" #**********
            self.__loc1 = ""

        setty = []
        setty.append(self.__title)  
        setty.append(self.__loc1)

        return setty




    def algoreithm(self, listy):
        #Getting X **************
        self.x = []
        self.y = []

        self.TsWithTIME = []
        self.TsWithoutTIME = []
        self.ratings = []
        self.rating = 0.0

        for row in listy:

            self.current_Ts = row[0].strftime('%Y-%m-%d-%H-%M')
            self.current_day = row[0].strftime('%Y-%m-%d')
            self.rating = row[1]
            self.TsWithTIME.append(self.current_Ts)
            self.TsWithoutTIME.append(self.current_day)
            self.ratings.append(self.rating)

        del(self.rating, self.current_day)

        

        self.ratingCount = len(self.TsWithTIME)

        #making a version of TsWithoutTIME without duplicates
        self.x = list(set(self.TsWithoutTIME))
        


        #Getting Y *************
        #Creating empty list 
        
        self.ytemp3 = []
        
        for i in self.x:
            self.ytemp1 = []
            for u in self.TsWithTIME:
                if i in u:
                    self.idx = self.TsWithTIME.index(u)

                    self.ytemp0 = self.ratings[self.idx]
                    self.ytemp1.append(self.ytemp0)

            self.ytemp1sum = sum(self.ytemp1)
            self.ytemp1len = float(len(self.ytemp1)) + 1
            
            self.ytemp2 = self.ytemp1sum/self.ytemp1len
            
            self.ytemp3.append(self.ytemp2)
            
        self.y = self.ytemp3
        
        self.x, self.y = zip(*sorted(zip(self.x,self.y)))    
        self.lister = [self.x,self.y, self.ratingCount]
        
        return self.lister


    def algore2(self, x):

        self.__bad = 0
        self.__mid = 0
        self.__good = 0


        # For this one I simply need the amount of 1's 2's and 3's,
        # so I simply use booleans as the type, in hope of cutting processing time
        for i in x:
            
            
            if i[0] == 1:
                self.__bad += 1
            if i[0] == 2:
                self.__mid += 1
            if i[0] == 3:
                self.__good += 1
        
        self.__returnable = [self.__bad, self.__mid, self.__good]
        return self.__returnable
