## Simple FastAPI daemon

**Dead Simple** wrapper to start your FastAPI on a daemon (UNIX).

#### Usage:
    python3 handler.py start/stop/restart
#### Edit variables
    host =  "0.0.0.0"
	port =  8080
	fastAPI_app =  "app:app"  # Command to start fastAPI server
	#FastAPI boilerplate is "main:app".