import numpy as np
from itertools import combinations

class Apriori:
    def __init__(self,DATABASE,SingleItems,minsupp):
        """
        *************************************************
        - DATABASE: Binary numpy 2d array.              -
        - SingleItems: Unique string is DATABASE column.-
        - SingleItems Type: Numpy 1d array.             -
        - minsupp: Minimum absolute support.            -
        - minsupp Type: Integer.                        -
        - FREQUENTITEMSETS: Dictionary.                 -
        *************************************************
        """
        self.DATABASE = DATABASE
        self.SingleItems = SingleItems
        self.minsupp = minsupp
        self.FREQUENTITEMSETS = {}

    def showDatabase(self):
        """
        *************************************************
        -       This method shows binary database.      -
        *************************************************
        """
        for i in range(0, self.DATABASE.shape[0]):
            tr = self.DATABASE[i,:]
            I = np.nonzero(tr>0)[0]
            print(i,": ",self.SingleItems[I])

    def databaseOptimision(self):
        """
        ***********************************************************
        *  This method extracts individual items from the         * 
        *  database that do not exceed the minimum support value. *
        ***********************************************************
        """
        SingleItemsSupport = np.sum(self.DATABASE,axis = 0)
        ReminderItem = np.nonzero(SingleItemsSupport >= self.minsupp)[0]
        self.DATABASE = self.DATABASE[:,ReminderItem]
        self.SingleItems = self.SingleItems[ReminderItem]
        SingleItemsSupport = SingleItemsSupport[ReminderItem]
        

    def listToString(self,s):
        """
        *************************************************
        - This method convert list to string.           -
        - s: New frequent item list.                    -
        - s Type: List.                                 -
        *************************************************
        """
        str1 = "" 
        for ele in s: 
            str1 += self.SingleItems[ele] + ","
        return str1[:-1]

    def doesExist(itm,transaction):
        """
        **********************************************************
        - This method checks the presence of itm in transaction. -
        **********************************************************
        """
        if sum(transaction[itm]) == len(itm):     
            E=True
        else:     
            E=False

        return E

    def calcAbsSup(self,itm): 
        """
        **********************************************************
        -       This method calc the itm absolute support.       -
        **********************************************************
        """
        AbsSupp = 0
        for i in range(0, self.DATABASE.shape[0]):
            transaction = self.DATABASE[i,:]
            if Apriori.doesExist(itm, transaction):
                AbsSupp += 1
        
        return AbsSupp
    
    def candidateGeneration(Fkm1):
        Ck= [] 
        for i in range(0, len(Fkm1)-1):
            for j in range(i+1,len(Fkm1)):
                itemset1 = Fkm1[i]
                itemset2 = Fkm1[j]
                
                if len(itemset1) == 1:
                    NewItem = np.hstack((np.array(itemset1),np.array(itemset2[-1])))
                    Ck.append(NewItem)
                else:
                    if sum(abs(itemset1[1:]-itemset2[:-1])) == 0:
                        NewItem = np.hstack((np.array(itemset1),np.array(itemset2[-1])))
                        Ck.append(NewItem)              
        return Ck
    
    def findFrequentItems(self):
        self.databaseOptimision()
        NumOfItems = self.DATABASE.shape[1]
        Fk = []
        k=1
        for i in range(0,NumOfItems):
            itm = np.array([i])
            AbsSupp = self.calcAbsSup(itm)

            if self.minsupp <= AbsSupp:
                Fk.append(itm)
                self.FREQUENTITEMSETS[self.listToString(itm)] = AbsSupp
        
        loop = True
        k = 2
        while loop:   
            Fkm1 = Fk ; Fk = []
            Ck = Apriori.candidateGeneration(Fkm1)
            for i in range(0,len(Ck)):
                adayoge = Ck[i]
                abssupp = self.calcAbsSup(adayoge)
                if self.minsupp <= abssupp:
                    Fk.append(adayoge)
                    self.FREQUENTITEMSETS[self.listToString(adayoge)] = abssupp
            k+=1       
            if len(Ck)* len(Fk) == 0:
                loop = False
        return self.FREQUENTITEMSETS
        
    def showFrequentItems(self):
        FREQUENTITEMSETS_ = []
        SUPPORTS = []
        for key,value in self.FREQUENTITEMSETS.items():
            FREQUENTITEMSETS_.append(key)
            SUPPORTS.append(value)
        
        I = np.argsort(-np.array(SUPPORTS))
        FREQUENTITEMSETS_ = [FREQUENTITEMSETS_[i] for i in I]
        SUPPORTS = [SUPPORTS[i] for i in I]

        for i in range(0,len(FREQUENTITEMSETS_)):
            print("#",i+1,FREQUENTITEMSETS_[i],"Supp:",SUPPORTS[i])

class Eclat:
    def __init__(self, DATABASE, SingleItems, minsupp):
        self.DATABASE = DATABASE
        self.SingleItems = SingleItems
        self.minsupp = minsupp
        self.VDB = []
        self.FREQUENTITEMSETS = {}
        
    def databaseOptimision(self):
        SingleItemsSupport = np.sum(self.DATABASE,axis = 0)
        ReminderItems = np.nonzero(SingleItemsSupport >= self.minsupp)[0]
        self.DATABASE = self.DATABASE[:,ReminderItems]
        self.SingleItems = self.SingleItems[ReminderItems]
        SingleItemsSupport = SingleItemsSupport[ReminderItems]
    
    def HDtoVDB(self):
        NumOfItems = self.DATABASE.shape[1]
        for i in range(0,NumOfItems):
            tmp = []
            for j in range(0,self.DATABASE.shape[0]):
                transaction = self.DATABASE[j]
                if transaction[i] != 0:
                    tmp.append(j)
            self.VDB.append(tmp)
    
    def showVDBdatabase(self):
        for i in range(0,self.SingleItems.shape[0]):
            print(self.SingleItems[i],':',self.VDB[i])
    
    def listToString(self,s):
        """
        *************************************************
        - This method convert list to string.           -
        - s: New frequent item list.                    -
        - s Type: List.                                 -
        *************************************************
        """
        str1 = "" 
        for ele in s: 
            str1 += self.SingleItems[ele] + ","
        return str1[:-1]
            
    def eclatMiner(self,item,Tid):
     tmp = item[-1]
     tid = []
     for itx in range(tmp+1,len(self.VDB)): 
         
         tid = set(Tid).intersection(self.VDB[itx])
                    
         if len(tid)>= self.minsupp:
            NewItem = np.hstack((item,itx))
            self.FREQUENTITEMSETS[self.listToString(NewItem)] = len(tid)
            self.FREQUENTITEMSETS = self.eclatMiner(NewItem,tid)
            tid = []
     return self.FREQUENTITEMSETS
    
    def findFrequentItems(self):
        self.databaseOptimision()
        self.HDtoVDB()

        for i in range(0,len(self.VDB)):
            item = np.array([i])
            self.FREQUENTITEMSETS[self.listToString(item)] = len(self.VDB[i])
            self.FREQUENTITEMSETS = self.eclatMiner(item,self.VDB[i])
        
        return self.FREQUENTITEMSETS
    
    def showFrequentItems(self):
        FREQUENTITEMSETS_ = []
        SUPPORTS = []
        for key,value in self.FREQUENTITEMSETS.items():
            FREQUENTITEMSETS_.append(key)
            SUPPORTS.append(value)
        
        I = np.argsort(-np.array(SUPPORTS))
        FREQUENTITEMSETS_ = [FREQUENTITEMSETS_[i] for i in I]
        SUPPORTS = [SUPPORTS[i] for i in I]

        for i in range(0,len(FREQUENTITEMSETS_)):
            print("#",i+1,FREQUENTITEMSETS_[i],"Supp:",SUPPORTS[i])

class HMine:
    def __init__(self, DATABASE, SingleItems, minsupp):
        """
        *************************************************
        - DATABASE: Binary numpy 2d array.              -
        - SingleItems: Unique string is DATABASE column.-
        - SingleItems Type: Numpy 1d array.             -
        - minsupp: Minimum absolute support.            -
        - minsupp Type: Integer.                        -
        - FREQUENTITEMSETS: Dictionary.                 -
        *************************************************
        """
        self.DATABASE = DATABASE
        self.SingleItems = SingleItems
        self.minsupp = minsupp
        self.FREQUENTITEMSETS = {}
    
    def showDB(self):
        """
        *************************************************
        -       This method shows binary database.      -
        *************************************************
        """
        for i in range(0, self.DATABASE.shape[0]):
            tr = self.DATABASE[i,:]
            I = np.nonzero(tr>0)[0]
            print(i,": ",self.SingleItems[I])

    def databaseOptimision(self):
        """
        ***********************************************************
        *  This method extracts individual items from the         * 
        *  database that do not exceed the minimum support value. *
        ***********************************************************
        """
        SingleItemsSupport = np.sum(self.DATABASE,axis = 0)
        ReminderItems = np.nonzero(SingleItemsSupport >= self.minsupp)[0]
        self.DATABASE = self.DATABASE[:,ReminderItems]
        self.SingleItems = self.SingleItems[ReminderItems]
        SingleItemsSupport = SingleItemsSupport[ReminderItems]
        return SingleItemsSupport
    
    def listToString(self,s):
        """
        *************************************************
        - This method convert list to string.           -
        - s: New frequent item list.                    -
        - s Type: List.                                 -
        *************************************************
        """
        str1 = "" 
        for ele in s: 
            str1 += self.SingleItems[ele]+","  
        return str1[:-1]

    def hMiner(self,DATABASE_,itemset):
        """
        *************************************************
        - This method allows data mining to be done.    -
        - This method is called for each single item.   -
        - Searched as DFS.                              -
        *************************************************
        """
        I = np.nonzero(np.sum(DATABASE_[:,itemset],axis = 1) == len(itemset))[0]
        ProjectedDatabase = DATABASE_[I,:]  
        InitialSupports = np.sum(ProjectedDatabase,axis = 0)
        Suffixes = np.nonzero(InitialSupports >= self.minsupp)[0]
        Suffixes = Suffixes[np.nonzero(Suffixes > itemset[-1])[0]]
        for suffix in Suffixes:
            NewItem = 1*itemset
            NewItem.append(suffix)
            self.FREQUENTITEMSETS[self.listToString(NewItem)] = InitialSupports[suffix]
            self.FREQUENTITEMSETS = self.hMiner(ProjectedDatabase,NewItem)
        return self.FREQUENTITEMSETS
    
    def findFrequentItems(self):
        """
        *************************************************
        -         Finding all frequentitems...          -
        *************************************************
        """
        SingleItemsSupport = self.databaseOptimision()
        for item in range(0,self.SingleItems.shape[0]):
            NewItem = [item]
            self.FREQUENTITEMSETS[self.listToString(NewItem)] = SingleItemsSupport[item]
            self.FREQUENTITEMSETS = self.hMiner(self.DATABASE,NewItem)
        return self.FREQUENTITEMSETS
    
    def showFrequentItems(self):
        FREQUENTITEMSETS_ = []
        SUPPORTS = []
        for key,value in self.FREQUENTITEMSETS.items():
            FREQUENTITEMSETS_.append(key)
            SUPPORTS.append(value)
        
        I = np.argsort(-np.array(SUPPORTS))
        FREQUENTITEMSETS_ = [FREQUENTITEMSETS_[i] for i in I]
        SUPPORTS = [SUPPORTS[i] for i in I]

        for i in range(0,len(FREQUENTITEMSETS_)):
            print("#",i+1,FREQUENTITEMSETS_[i],"Supp:",SUPPORTS[i])

class ARM:
    def __init__(self, data, FIS, minconf, minkulc):
        self.data = data
        self.FIS = FIS
        self.minconf = minconf
        self.minkulc = minkulc
        self.rules = {}
    
    def findIndex(itemset, FREQUENTITEMSETS):
        Index = []

        for i in range(0,len(FREQUENTITEMSETS)):
            temp = FREQUENTITEMSETS[i]
            if len(itemset) == len(temp):
                if all(itemset == temp):
                    Index = i
        return Index
                
    def findRules(self):
        """
        *************************************************
        -     Finding all association rules.            -
        *************************************************
        """
        FREQUENTITEMSETS = []
        SUPPORTS = []
        DATABASE = self.data[0]
        SingleItems = self.data[1]

        for key,value in self.FIS.items():
            FREQUENTITEMSETS.append(key)
            SUPPORTS.append(value)

        FREQUENTITEMSETS = [i.split(",") for i in FREQUENTITEMSETS]
        for i in FREQUENTITEMSETS:
            tmp = []
            for j in i:
                tmp.append(np.where(SingleItems == j)[0][0])
            FREQUENTITEMSETS[FREQUENTITEMSETS.index(i)] = tmp
        
        FREQUENTITEMSETS = np.array(FREQUENTITEMSETS,dtype="object")
        NumOfTransaction = DATABASE.shape[0]
        SUPPORTS = [support/NumOfTransaction for support in SUPPORTS]

        for itemset in FREQUENTITEMSETS:

            itemset = np.array(itemset)
            itemset_size = len(itemset)
            if itemset_size > 1:
                I = ARM.findIndex(itemset, FREQUENTITEMSETS)
                ItemsetSupport = SUPPORTS[I]
            
                for j in range(1,itemset_size):
                
                    CMBN = list(combinations(np.arange(0,itemset_size), j))
                    CMBN = np.matrix(CMBN)
                    for k in range(0,len(CMBN)):
                    
                        PrefixIndex = np.array(CMBN[k,:])[0]
                        tmp = np.ones(itemset_size)
                        tmp[PrefixIndex] = 0
                        SuffixIndex = np.nonzero(tmp != 0)[0]
                        Prefix = itemset[PrefixIndex]
                        Suffix = itemset[SuffixIndex]
                        
                        showPrefix = ""
                        for kk in range(0, np.size(Prefix)):
                            showPrefix += SingleItems[Prefix[kk]]
                    
                        showSuffix = ""
                        for kk in range(0, np.size(Suffix)):
                            showSuffix += SingleItems[Suffix[kk]]
                    
                        I = ARM.findIndex(Prefix, FREQUENTITEMSETS)
                        PrefixSupport = SUPPORTS[I]
                    
                        I = ARM.findIndex(Suffix, FREQUENTITEMSETS)
                        SuffixSupport = SUPPORTS[I]
                    
                        Confidince = ItemsetSupport / PrefixSupport
                    
                        Kulc = 0.5 * (ItemsetSupport / PrefixSupport + ItemsetSupport / SuffixSupport)
                        Kulc = 2*(Kulc-0.5)
                    
                        if self.minkulc <= Kulc:
                            if self.minconf <= Confidince:
                                # print(showPrefix,"==>",showSuffix, "supp:",ItemsetSupport," conf:",Confidince, " Kulc:",Kulc)
                                self.rules[str(showPrefix)+"==>"+str(showSuffix)] = {   "Supp":ItemsetSupport,
                                                                                        "Confidince": Confidince, 
                                                                                        "Kulc": Kulc}
        return self.rules    