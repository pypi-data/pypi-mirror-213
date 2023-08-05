# Copyright 2023 Motion Signal Technologies Limited
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
Python client for extracting data from CATE archives to numpy arrays


------------
INSTALLATION
------------

-----
USAGE
-----

..

   from catenp import Authenticate,DatabaseInfo,GetData

   # Authenitcate to the server
   tk = Authenticate(serverAddress,serverPort,cateUserName,catePassword)
   
   # Optional get server info
   info = DatabaseInfo(serverAddress,serverPort,cateUserName)
   print("Info: ")
   for kk in info: 
     if kk !="segments": 
         print("  ",kk,":",info[kk])
     else:
         print("  segments:")
         for xx in info[kk]:
             for ll in xx: print("    ",ll,":",xx[ll]) 
             print("")
   
   
   # Exract some data    
   arr=GetData(serverAddress,serverPort,cateUserName,tstart,tstop,cstart,cstop)


'''


import requests
import json
import numpy as np


CATE_Session_Tokens={}
'''
Session token for accessing the CATE server
'''

class ExceptionCATENPNoData(Exception):
    '''
    Exception classs for absence of data
    '''


def Authenticate(cateServer,cateServerPort,username,password):
    '''
    Returns a session token for the CATE server and saves the result in a module variable
    '''


    resp=requests.post("http://"+str(cateServer)+":"+str(cateServerPort)+"/token", 
                       headers={"accept":"application/json",
                                "Content-Type": "application/x-www-form-urlencoded"
                                },
                       data={"username":str(username),"password":str(password),
                             "scope":None,"client_id": None,"client_secret":None},
                       )   

    if resp.status_code!=200: raise Exception( "ERROR in CATE login message: "+resp.content.decode() )

    global CATE_Session_Tokens
    rr=json.loads(resp.content)
    CATE_Session_Tokens[(cateServer,cateServerPort,username)]=rr["access_token"]
    
    return CATE_Session_Tokens[(cateServer,cateServerPort,username)]

def DatabaseInfo(cateServer,cateServerPort,username,detail=False):
    '''
    Get database coverage information from the server. Use detail=True to provide a comprehensive list
     the default is to show main data chunks (typically 1hr)
     
    @param cateServer: cate server address
    @type cateServer: str

    @param cateServer: cate server port
    @type cateServer: int
  
    @param username: cate server user name
    @type username: str
     
    '''
    
    global CATE_Session_Tokens
    if (cateServer,cateServerPort,username) not in CATE_Session_Tokens:
        raise Exception( "ERROR could not find authentication token for : "+str( (cateServer,cateServerPort,username) ) )
    sessionToken=CATE_Session_Tokens[(cateServer,cateServerPort,username)]
    
    
    resp=requests.get("http://"+cateServer+":"+str(cateServerPort)+"/archive_db_info", 
                       headers={"Authorization": "Bearer "+sessionToken},
                       params={"detail": detail}
                       )   
    
    if resp.status_code!=200: raise Exception( "ERROR in CATE login message: "+resp.content.decode() )
    return json.loads(resp.content)
    
def GetData(cateServer,cateServerPort,username,
            tstart,tstop,
            cstart,cstop
            ):
    '''
    Query and download data from the CATE server
    
    @param cateServer: cate server address
    @type cateServer: str

    @param cateServer: cate server port
    @type cateServer: int
  
    @param username: cate server user name
    @type username: str

    @param tstart: isoformat time string for start of data (first sample)
    @type tstart: str

    @param tstop: isoformat time string for stop of data (last sample)
    @type tstop: str

    @param cstart: channel number for start of data
    @type cstart: int

    @param cstop: channel number for stop of data (inclusive)
    @type cstop: int
    
    '''
    
    global CATE_Session_Tokens
    if (cateServer,cateServerPort,username) not in CATE_Session_Tokens:
        raise Exception( "ERROR could not find authentication token for : "+str( (cateServer,cateServerPort,username) ) )
    sessionToken=CATE_Session_Tokens[(cateServer,cateServerPort,username)]
    
    
    # Intitial query
    resp=requests.get("http://"+cateServer+":"+str(cateServerPort)+"/get_data_segments", 
                       headers={"Authorization": "Bearer "+sessionToken},
                       params={
                            "tmin":tstart,
                            "tmax": tstop,
                            "cmin": cstart,
                            "cmax": cstop
                       }
                       )   

    
    if resp.status_code!=200: raise Exception( "ERROR in CATE from CATE server: "+resp.content.decode() )
    rr=json.loads(resp.content)
    if len(rr)==0: raise ExceptionCATENPNoData("No data available for request")
    

    # Make the output data array
    start_row=min([xx["output_start_row"] for xx in rr])
    stop_row=max([xx["output_stop_row"] for xx in rr])
    nRow=stop_row-start_row+1
    
    start_col=min([xx["output_start_column"] for xx in rr])
    stop_col=max([xx["output_stop_column"] for xx in rr])
    nCol=stop_col-start_col+1
    dataType=rr[0]["dtype"]
    dataArray = np.zeros([nRow,nCol],dtype=dataType)
    #print("Output data shape=",dataArray.shape)

    # Download the data segments and place into output
    for xx in rr:
    
        # Call with data_key to download data
        dresp=requests.get("http://"+cateServer+":"+str(cateServerPort)+"/get_data",
                           headers={"Authorization": "Bearer "+sessionToken},
                           params={ "data_key": xx["data_key"] }
                          )   
        if dresp.status_code!=200: 
            raise Exception( "ERROR in CATE data retrieval for data segment error code="+dresp.content.decode() )   
        
        # Un pack the data and place into output
        arr = np.frombuffer(dresp.content,dtype=xx["dtype"])
        arr.shape=(
                   xx["input_stop_row"]-xx["input_start_row"]+1,
                   xx["input_stop_column"]-xx["input_start_column"]+1
                   )
        dataArray[ xx["output_start_row"]:xx["output_stop_row"]+1, 
                   xx["output_start_column"]:xx["output_stop_column"]+1 
                 ] = arr

    return dataArray


def Example():
    '''
    Simple test / example functionality
    '''

    print("\n*********************\nTest/ Example functionality\n******************\n")

    print("\n*********************\nRead in server data")

    with open("./test-data.txt") as fd:
        serverAddress = fd.readline().rstrip()           # CATE Server address (example 1.2,3,4)
        serverPort = int(fd.readline().rstrip())         # CATE Server port (example 8000)
        cateUserName = fd.readline().rstrip()            # User name on the server
        catePassword = fd.readline().rstrip()            # Password on the server
        
        tstart = fd.readline().rstrip()                  # Start of time interval to get
        tstop = fd.readline().rstrip()                   # Stop of time interval to get
        cstart = int( fd.readline().rstrip() )           # Start of channel interval to gets
        cstop = int( fd.readline().rstrip() )            # End of channel interval to get
        
        
    print("Got server details:")
    print("   Server=",serverAddress)  
    print("   port=",serverPort)  
    print("   User=",cateUserName)  
    
    
    print("\n*********************\nAuthenitcate")
    tk = Authenticate(serverAddress,serverPort,cateUserName,catePassword)
    print("Got session token: ",tk)

    print("\n*********************\nDatabase info")
    info = DatabaseInfo(serverAddress,serverPort,cateUserName)
    print("Info: ")
    for kk in info: 
        if kk !="segments": 
            print("  ",kk,":",info[kk])
        else:
            print("  segments:")
            for xx in info[kk]:
                for ll in xx: print("    ",ll,":",xx[ll]) 
                print("")


    # Get some data
    print("\n*********************\nGetting Data:")
    print("Interval: ")
    print("   tstart=",tstart)  
    print("   tstop=",tstop)  
    print("   cstart=",cstart) 
    print("   cstop=",cstop) 
    
    arr=GetData(serverAddress,serverPort,cateUserName,tstart,tstop,cstart,cstop)

    print("Got data:")
    print("  arr.shape=",arr.shape)
    print("  arr.dtype=",arr.dtype)
    print("  range=",np.min(arr),np.max(arr))    

    

if __name__ == '__main__':
    
    
    Example()
    
    