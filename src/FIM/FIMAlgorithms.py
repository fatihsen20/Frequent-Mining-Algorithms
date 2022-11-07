import numpy as np
from itertools import combinations

def showDatabase(DATABASE:np.array, SingleItems:np.array):
    """
        This method shows binary database.
    """
    for i in range(0, DATABASE.shape[0]):
        tr = DATABASE[i,:]
        I = np.nonzero(tr>0)[0]
        print(i,": ",SingleItems[I])

def databaseOptimision(DATABASE:np.array, SingleItems:np.array, minsupp:int) -> np.array:
    """
        This method extracts individual items from the database that do not exceed the minimum support value.
    """
    SingleItemsSupport = np.sum(DATABASE,axis = 0)
    ReminderItem = np.nonzero(SingleItemsSupport >= minsupp)[0]
    DATABASE = DATABASE[:,ReminderItem]
    SingleItems = SingleItems[ReminderItem]
    SingleItemsSupport = SingleItemsSupport[ReminderItem]
    return SingleItemsSupport

def listToString(SingleItems:np.array,s:list) -> str:
    """
        This method convert list to string.
        s: New frequent item list.                    
    """
    str1 = "" 
    for ele in s: 
        str1 += SingleItems[ele] + ","
    return str1[:-1]

class Apriori:
    def __init__(self,DATABASE:np.array,SingleItems:np.array,minsupp:int):
        """
            DATABASE: Binary numpy 2d array.              
            SingleItems: Unique string is DATABASE column.
            SingleItems Type: Numpy 1d array.             
            minsupp: Minimum absolute support.            
            minsupp Type: Integer.                       
            FREQUENTITEMSETS: Dictionary. 
            rules: Dictionary.                
        
        """
        self.DATABASE = DATABASE
        self.SingleItems = SingleItems
        self.minsupp = minsupp
        self.FREQUENTITEMSETS = {}
        self.rules = {}

    def doesExist(itm,transaction) -> bool:
        """
            This method checks the presence of itm in transaction.
        """
        if sum(transaction[itm]) == len(itm):     
            E=True
        else:     
            E=False

        return E

    def calcAbsSup(self,itm) -> int: 
        """
            This method calc the itm absolute support.
        """
        AbsSupp = 0
        for i in range(0, self.DATABASE.shape[0]):
            transaction = self.DATABASE[i,:]
            if Apriori.doesExist(itm, transaction):
                AbsSupp += 1
        
        return AbsSupp
    
    def candidateGeneration(Fkm1) -> list:
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
    
    def findFrequentItems(self) -> dict:
        _ = databaseOptimision(self.DATABASE, self.SingleItems, self.minsupp)
        NumOfItems = self.DATABASE.shape[1]
        Fk = []
        k=1
        for i in range(0,NumOfItems):
            itm = np.array([i])
            AbsSupp = self.calcAbsSup(itm)

            if self.minsupp <= AbsSupp:
                Fk.append(itm)
                self.FREQUENTITEMSETS[listToString(self.SingleItems,itm)] = AbsSupp
        
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
                    self.FREQUENTITEMSETS[listToString(self.SingleItems,adayoge)] = abssupp
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
        
    def showRules(self, minconf:float, minkulc:float):
        arm = ARM((self.DATABASE,self.SingleItems), self.FREQUENTITEMSETS, minconf, minkulc)
        self.rules = arm.findRules()
        arm.showRules()

class Eclat:
    def __init__(self, DATABASE:np.array, SingleItems:np.array, minsupp:int):
        """
            DATABASE: Binary numpy 2d array.              
            SingleItems: Unique string is DATABASE column.
            SingleItems Type: Numpy 1d array.             
            minsupp: Minimum absolute support.
            VDB: Vertical Database.                                    
            FREQUENTITEMSETS: Dictionary.  
            rules: Dictionary.               
        """

        self.DATABASE = DATABASE
        self.SingleItems = SingleItems
        self.minsupp = minsupp
        self.VDB = []
        self.FREQUENTITEMSETS = {}
        self.rules = {}
    
    def HDtoVDB(self):
        """
            This method convert horizontal DB to Vertical DB.
        """
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
            
    def eclatMiner(self,item,Tid) -> dict:
        """
            This method includes the recursive part of the eclat algorithm.
        """
        tmp = item[-1]
        tid = []
        for itx in range(tmp+1,len(self.VDB)): 
         
            tid = set(Tid).intersection(self.VDB[itx])
                    
            if len(tid)>= self.minsupp:
                NewItem = np.hstack((item,itx))
                self.FREQUENTITEMSETS[listToString(self.SingleItems,NewItem)] = len(tid)
                self.FREQUENTITEMSETS = self.eclatMiner(NewItem,tid)
                tid = []
        return self.FREQUENTITEMSETS
    
    def findFrequentItems(self) -> dict:
        _ = databaseOptimision(self.DATABASE, self.SingleItems, self.minsupp)
        self.HDtoVDB()

        for i in range(0,len(self.VDB)):
            item = np.array([i])
            self.FREQUENTITEMSETS[listToString(self.SingleItems,item)] = len(self.VDB[i])
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
    
    def showRules(self, minconf:float, minkulc:float):
        arm = ARM((self.DATABASE,self.SingleItems), self.FREQUENTITEMSETS, minconf, minkulc)
        self.rules = arm.findRules()
        arm.showRules()

class HMine:
    def __init__(self, DATABASE:np.array, SingleItems:np.array, minsupp:int):
        """
            DATABASE: Binary numpy 2d array.              
            SingleItems: Unique string is DATABASE column.
            SingleItems Type: Numpy 1d array.             
            minsupp: Minimum absolute support.            
            minsupp Type: Integer.                        
            FREQUENTITEMSETS: Dictionary.
            rules: Dictionary.                
        """
        self.DATABASE = DATABASE
        self.SingleItems = SingleItems
        self.minsupp = minsupp
        self.FREQUENTITEMSETS = {}
        self.rules = {}

    def hMiner(self,DATABASE_,itemset) -> dict:
        """
            This method allows data mining to be done.    
            This method is called for each single item.   
            Searched as DFS.                              
        """
        I = np.nonzero(np.sum(DATABASE_[:,itemset],axis = 1) == len(itemset))[0]
        ProjectedDatabase = DATABASE_[I,:]  
        InitialSupports = np.sum(ProjectedDatabase,axis = 0)
        Suffixes = np.nonzero(InitialSupports >= self.minsupp)[0]
        Suffixes = Suffixes[np.nonzero(Suffixes > itemset[-1])[0]]
        for suffix in Suffixes:
            NewItem = 1*itemset
            NewItem.append(suffix)
            self.FREQUENTITEMSETS[listToString(self.SingleItems,NewItem)] = InitialSupports[suffix]
            self.FREQUENTITEMSETS = self.hMiner(ProjectedDatabase,NewItem)
        return self.FREQUENTITEMSETS
    
    def findFrequentItems(self) -> dict:
        """
            Finding all frequentitems... 
        """
        SingleItemsSupport = databaseOptimision(self.DATABASE, self.SingleItems, self.minsupp)
        for item in range(0,self.SingleItems.shape[0]):
            NewItem = [item]
            self.FREQUENTITEMSETS[listToString(self.SingleItems,NewItem)] = SingleItemsSupport[item]
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
    
    def showRules(self, minconf:float, minkulc:float):
        arm = ARM((self.DATABASE,self.SingleItems), self.FREQUENTITEMSETS, minconf, minkulc)
        self.rules = arm.findRules()
        arm.showRules()

class ARM:
    def __init__(self, data:tuple, FIS:dict, minconf:float, minkulc:float):
        self.data = data
        self.FIS = FIS
        self.minconf = minconf
        self.minkulc = minkulc
        self.rules = {}
    
    def findIndex(itemset:np.array, FREQUENTITEMSETS:np.array) -> int:
        Index = []

        for i in range(0,len(FREQUENTITEMSETS)):
            temp = FREQUENTITEMSETS[i]
            if len(itemset) == len(temp):
                if all(itemset == temp):
                    Index = i
        return Index
                
    def findRules(self) -> dict:
        """
            Finding all association rules.        
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

    def showRules(self):
        RULES_ = []
        SUPPORTS = []
        CONFIDINCES = []
        KULCS = []
        for key,value in self.rules.items():
            RULES_.append(key)
            SUPPORTS.append(value["Supp"])
            CONFIDINCES.append(value["Confidince"])
            KULCS.append(value["Kulc"])
        
        I = np.argsort(-np.array(KULCS))
        RULES_ = [RULES_[i] for i in I]
        SUPPORTS = [SUPPORTS[i] for i in I]
        CONFIDINCES = [CONFIDINCES[i] for i in I]
        KULCS = [KULCS[i] for i in I]

        for i in range(0,len(RULES_)):
            print("#",i+1,RULES_[i],"Supp:",SUPPORTS[i],"Conf:",CONFIDINCES[i],"Kulc:",KULCS[i])