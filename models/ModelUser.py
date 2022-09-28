

class ModelUser():
    
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, username, password, fullname FROM user 
                    WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                # user=User()
                print('')
            else:
                print('')
        except Exception as ex:
            raise Exception(ex)
        