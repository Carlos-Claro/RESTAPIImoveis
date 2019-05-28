# -*- coding: utf-8 -*-


from myMongo import myMongo
import datetime

class imoveisMongo(object):
    
    def __init__(self):
        self.db = myMongo('imoveis')
        
    def add(self,data):
        return self.db.add_one(data)
    
    def update_id(self,id,data):
        return self.db.update_one('imoveis',{'_id':id},data)
        
    
    def delete_id(self, id):
        return self.db.delete_one('imoveis',{'_id':id})
    
    def getItem(self, id):
        return self.db.getItem('imoveis',id)
    
    def getItens(self, data):
        return self.db.getItens('imoveis',data)
    
if __name__ == '__main__':
    print('')
    