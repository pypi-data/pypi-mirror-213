import pymysql
import json


class mysql_connect():
    def __init__(self, host, user, pwd, db_name, port=None):
        self.db = pymysql.connect(host=host, user=user, password=pwd, database=db_name, port=port)
        self.cursor = self.db.cursor()

    def trans_to_json(self, description, results):
        fields = [field[0] for field in description]
        data = [dict(zip(fields, row)) for row in results]
        json_data = json.dumps(data)
        return json_data

    def select(self, sql):
        self.cursor.execute(sql)
        results = self.cursor.fetchall()

        description = self.cursor.description
        json_data = self.trans_to_json(description, results)
        json_data = json.loads(json_data)
        return json_data

    def find(self, sql):
        self.cursor.execute(sql)
        results = self.cursor.fetchone()
        description = self.cursor.description[0][0]
        json_data = {description: results[0]}
        return json_data

    def delete(self, sql):
        '''未测试'''
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            print("删除出错")
            self.db.rollback()
            return False
        else:
            return True

    def update(self, sql):
        self.cursor.execute(sql)
        self.db.commit()

    def insert(self, sql):
        self.update(sql)

    def quit(self):
        self.db.close()
        self.cursor.close()


