-----------
DESCRIPTION
-----------

Python client for extracting data from CATE archives to numpy arrays

------------
INSTALLATION
------------

::

   pip install catenp


-----
USAGE
-----

See also `catenp.catenumpy.Example`

::

   from catenp import Authenticate,DatabaseInfo,GetData
   
   # Authenticate to the server
   tk = Authenticate(serverAddress,serverPort,cateUserName,catePassword)
   
   # (Optional) get server/ data info
   info = DatabaseInfo(serverAddress,serverPort,cateUserName)
   print("Info: ")
   for kk in info: print("  ",kk,":",info[kk])


   # Extract some data    
   arr=GetData(serverAddress,serverPort,cateUserName,tstart,tstop,cstart,cstop)



