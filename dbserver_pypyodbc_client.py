import pypyodbc

#dbserver_ip = "localhost"
dbserver_ip = "10.131.83.195"
dbserver_db = "AUVSI"
dbserver_user = "spykat"
dbserver_password = "pass"

conn = pypyodbc.connect('DRIVER={SQL Server};Server='+dbserver_ip+'Database='+dbserver_db+';uid=sa;pwd=sa')

conn.close()
