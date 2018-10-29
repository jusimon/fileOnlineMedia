import pymysql
import sys
from attrDict import AttrDict
import aws

class client:
    def __init__(self):
        self.rds_host = aws.getAwsRdsHost()
        self.username = aws.getAwsUsername()
        self.password = aws.getAwsPassword()
        self.dbname = aws.getAwsDbName()
        
    def connect_client_db(self):
        """
        This function connects to the DB and returns handle
        """
        
        conn = pymysql.connect(self.rds_host, user=self.username,
                               passwd=self.password, db=self.dbname,
                               connect_timeout=5)
        return conn
       
    def get_clients(self):
        """
        This function adds content to mysql RDS instance
        """
        result = []
        conn = self.connect_client_db()
        with conn.cursor() as cur:
            cur.execute("""select * from client""")
            conn.commit()
            cur.close()
            for row in cur:
                count  = 0 
                item = {}
                for info in cur.description:
                    item[info[0]] = row[count]
                    count += 1
                result.append(item)
        return (result)

    def get_client(self, username):
        """
        This function gets username mysql RDS instance
        """
        result = {}
        count  = 0
        conn = self.connect_client_db()
        with conn.cursor() as cur:
           sql = "select * from client where username=%s"
           ret = cur.execute(sql, (username))
           cur.close()
           for row in cur:
               for info in cur.description:
                   result[info[0]] = row[count]
                   count += 1
        return (result)

    def set_client(self, event):
        """
        This function fetches content from mysql RDS instance
        """
        code  = 0
        message = '' 
        
        conn = self.connect_client_db()
        with conn.cursor() as cur:
            try:
                sql = "INSERT INTO `client` (`username`, `password`, `FirstName`, `LastName`, `Email`) values( %s, %s, %s, %s, %s)"
                ret = cur.execute(sql, (event['username'], event['password'], event['firstname'], event['lastname'], event['email']))
                conn.commit()
                cur.close()
            except pymysql.InternalError as error:
                code, message = error.args
            except pymysql.ProgrammingError as error:
                code, message = error.args
            except pymysql.IntegrityError as error:
                code, message = error.args
            return (code, message)


    def del_client(self, username):
        """
        This function deletes content from mysql RDS instance
        """
        code  = 0
        message = '' 
        
        conn = self.connect_client_db()
        with conn.cursor() as cur:
            try:
                sql = "DELETE FROM `client` WHERE (`username` = %s)"
                ret = cur.execute(sql, (username))
                conn.commit()
                cur.close()
            except pymysql.InternalError as error:
                code, message = error.args
            except pymysql.ProgrammingError as error:
                code, message = error.args
            except pymysql.IntegrityError as error:
                code, message = error.args
            return (code, message)

    def validate_client(self, username, password):
        """
        This function deletes content from mysql RDS instance
        """
        code  = 0
        message = '' 
        result = ''
                
        conn = self.connect_client_db()
        with conn.cursor() as cur:
            try:
               sql = "select password from client where username=%s"
               ret = cur.execute(sql, (username))
               conn.commit()
               cur.close()
               for row in cur:
                   result = (list(row))
               if result == '':
                   code = 254
                   message = "User doesn't exists!!!!"
               elif result[0] != password:
                   code = 255
                   message = "Invalid Password!!!!"
                   
            except pymysql.InternalError as error:
                code, message = error.args
            except pymysql.ProgrammingError as error:
                code, message = error.args
            except pymysql.IntegrityError as error:
                code, message = error.args
            return (code, message)

    def is_admin_user(self, username):
        conn = self.connect_client_db()
        with conn.cursor() as cur:
            sql = "select userType from client where username=%s"
            ret = cur.execute(sql, (username))
            cur.close()
            for row in cur:
                if list(row)[0] != 0:
                    return 1 
        return 0 



#if __name__ == "__main__":
#        c = client()
#        ret = c.get_clients()
#        print(ret)

