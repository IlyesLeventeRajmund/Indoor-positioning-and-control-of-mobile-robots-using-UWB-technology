from fastapi import FastAPI, HTTPException
from routes import robot_routes

from datetime import datetime
from config import settings
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import threading
import logging
  

class Server:
    def __init__(self):

        self.app = FastAPI()
        self.app.include_router(robot_routes.router)

        self.thread = None
       
        # Configure CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
   
    def start(self):
        self.thread = threading.Thread(target=self._run_server)
        self.thread.daemon = True  # Thread will exit when main program exits
        self.thread.start()
        
        logging.info(f"Server started on http://{settings.host_ip}:{settings.host_port}")
        
        return self.thread
    
    def _run_server(self):
        # Do not let uvicorn override the logging config
        uvicorn.run(self.app, host=settings.host_ip, port=settings.host_port, log_config=None)
        
    def stop(self):
        """Stop the server - note: this is not fully implemented as uvicorn doesn't 
        provide a clean shutdown method when run this way"""
        # This is a placeholder - proper shutdown would need a more complex approach
        # with uvicorn's server instance
        if self.thread:
            logging.debug("Warning: Cannot fully stop uvicorn server once started.")
            logging.debug("You may need to restart your application to fully release the port.")
    