from fastapi import FastAPI
from routes import robot_routes

from config import settings
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import Config as UviconrConfig
from uvicorn import Server as UviconrServer
import threading
import logging
  

class Server:
    def __init__(self):
        self.app = FastAPI()
        self.app.include_router(robot_routes.router)
        self.server = None
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
        config = UviconrConfig(app=self.app, host=settings.host_ip, port=settings.host_port, log_config=None)
        
        self.server = UviconrServer(config=config)

        self.thread = threading.Thread(target=self.server.run)
        self.thread.daemon = True
        self.thread.start()
        
        logging.info(f"Server started on http://{settings.host_ip}:{settings.host_port}")

        
    def stop(self):
        if self.server:
            self.server.should_exit = True
            self.thread.join()
            logging.info("Server stopped.")