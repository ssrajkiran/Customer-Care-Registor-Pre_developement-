# CONNECTED WITH IBM DB

# FLASK WITH IBM-DB2-DATABASE

Working with IBM Db2 service 

> Install Necessary Packages

> Add the connection details from IBM DB2 as show under Service credentials of Portal

--- ADD IT IN YOUR PYTHON APP ---
> import ibm_db
> conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=<HOSTNAME>;PORT=<PORTNUMBER>;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;
> UID=<USERNAME>;PWD=<PASSWORD>",'','')
> print(conn)
> print("connection successful...")

----------

> Download SSL Certificate form setting pages of IBM DB2

Open the application

http://127.0.0.1:5000/
