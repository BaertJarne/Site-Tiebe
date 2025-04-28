from .Database import Database

class DataRepository:
    @staticmethod
    def read_foto_pad():
        sql = "SELECT * FROM tblfoto_paden"
        params = []
        return Database.get_rows(sql, params)
    
    @staticmethod
    def read_tekst():
        sql = "SELECT * FROM tbltekst"
        params = []
        return Database.get_rows(sql, params)
    
    @staticmethod
    def create_foto_pad(foto_pad):
        sql = "INSERT INTO tblfoto_paden (paden) VALUES (%s)"
        params = [foto_pad]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def create_tekst(tekst, fotoID):
        sql = "INSERT INTO tbltekst (tekstje, idfoto) VALUES (%s, %s)"
        params = [tekst, fotoID]
        return Database.execute_sql(sql, params)