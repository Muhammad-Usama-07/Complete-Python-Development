from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
import subprocess
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
import shutil
from datetime import datetime
import multiprocessing
import time
from PIL import ImageGrab
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Boolean, Integer, Float, JSON, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import List, Optional
import logging
from fastapi import Request
app = FastAPI()

# Database credentials for FastAPI integration
DATABASE_URL = "mysql+pymysql://root:root_db_hello111@localhost:3307/mail_auto_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Pydantic models for request validation
class GeoLocation(BaseModel):
    latitude: float
    longitude: float

class Timezone(BaseModel):
    timezoneId: str

class OtherSettings(BaseModel):
    enable_javascript: bool
    accept_ssl_certificates: bool
    headless: bool
    disable_images: bool

class BrowserDetails(BaseModel):
    user_agent: str
    browser_type: str
    language: str
    geo_location: GeoLocation
    timezone: Timezone
    other_settings: OtherSettings

class DeviceMatrix(BaseModel):
    width: int
    height: int
    deviceScaleFactor: float
    mobile: bool
    fitWindow: bool

class ProxyDetails(BaseModel):
    ip: str
    port: str
    username: str
    password: str

class LoginDetails(BaseModel):
    mail: str
    password: str

class PasswordRecovery(BaseModel):
    recovery_mailbox: str
    recovery_phone: str

class AccountDetails(BaseModel):
    login: LoginDetails
    password_recovery: PasswordRecovery

class ProfileDetails(BaseModel):
    profile_name: str
    account_details: AccountDetails

class RequestData(BaseModel):
    token_id: str  # Add token_id to the input JSON
    browser_details: BrowserDetails
    device_matrix: DeviceMatrix
    proxy_details: ProxyDetails
    profile_details: ProfileDetails
    actions_chain: List[List]

# Database model
class Profile(Base):
    __tablename__ = "config"
    token_id = Column(String(255), primary_key=True)  # Use token_id as the primary key
    browser_user_agent = Column(String(255))
    browser_type = Column(String(50))
    browser_language = Column(String(50))
    geo_latitude = Column(Float(9, 6))
    geo_longitude = Column(Float(9, 6))
    timezone_id = Column(String(50))
    enable_javascript = Column(Boolean)
    accept_ssl_certificates = Column(Boolean)
    headless = Column(Boolean)
    disable_images = Column(Boolean)
    device_width = Column(Integer)
    device_height = Column(Integer)
    device_scale_factor = Column(Float(3, 1))
    device_mobile = Column(Boolean)
    device_fit_window = Column(Boolean)
    proxy_ip = Column(String(50))
    proxy_port = Column(String(10))
    proxy_username = Column(String(100))
    proxy_password = Column(String(100))
    profile_name = Column(String(255))
    login_mail = Column(String(255))
    login_password = Column(String(255))
    recovery_mailbox = Column(String(255))
    recovery_phone = Column(String(20))
    actions_chain = Column(JSON)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/start")
async def start(request: Request, data: RequestData, db: Session = Depends(get_db)):
    # Log the incoming request payload
    request_body = await request.json()
    # logger.info(f"Incoming request payload: {request_body}")

    # Extract data from the request
    token_id = data.token_id
    browser_details = data.browser_details
    device_matrix = data.device_matrix
    proxy_details = data.proxy_details
    profile_details = data.profile_details
    actions_chain = data.actions_chain

    # Check if profile with the same token_id already exists
    existing_profile = db.query(Profile).filter(Profile.token_id == token_id).first()

    if existing_profile:
        # Update existing profile
        existing_profile.browser_user_agent = browser_details.user_agent
        existing_profile.browser_type = browser_details.browser_type
        existing_profile.browser_language = browser_details.language
        existing_profile.geo_latitude = browser_details.geo_location.latitude
        existing_profile.geo_longitude = browser_details.geo_location.longitude
        existing_profile.timezone_id = browser_details.timezone.timezoneId
        existing_profile.enable_javascript = browser_details.other_settings.enable_javascript
        existing_profile.accept_ssl_certificates = browser_details.other_settings.accept_ssl_certificates
        existing_profile.headless = browser_details.other_settings.headless
        existing_profile.disable_images = browser_details.other_settings.disable_images
        existing_profile.device_width = device_matrix.width
        existing_profile.device_height = device_matrix.height
        existing_profile.device_scale_factor = device_matrix.deviceScaleFactor
        existing_profile.device_mobile = device_matrix.mobile
        existing_profile.device_fit_window = device_matrix.fitWindow
        existing_profile.proxy_ip = proxy_details.ip
        existing_profile.proxy_port = proxy_details.port
        existing_profile.proxy_username = proxy_details.username
        existing_profile.proxy_password = proxy_details.password
        existing_profile.profile_name = profile_details.profile_name
        existing_profile.login_mail = profile_details.account_details.login.mail
        existing_profile.login_password = profile_details.account_details.login.password
        existing_profile.recovery_mailbox = profile_details.account_details.password_recovery.recovery_mailbox
        existing_profile.recovery_phone = profile_details.account_details.password_recovery.recovery_phone
        existing_profile.actions_chain = actions_chain
        db.commit()
    else:
        # Insert new profile
        profile = Profile(
            token_id=token_id,
            browser_user_agent=browser_details.user_agent,
            browser_type=browser_details.browser_type,
            browser_language=browser_details.language,
            geo_latitude=browser_details.geo_location.latitude,
            geo_longitude=browser_details.geo_location.longitude,
            timezone_id=browser_details.timezone.timezoneId,
            enable_javascript=browser_details.other_settings.enable_javascript,
            accept_ssl_certificates=browser_details.other_settings.accept_ssl_certificates,
            headless=browser_details.other_settings.headless,
            disable_images=browser_details.other_settings.disable_images,
            device_width=device_matrix.width,
            device_height=device_matrix.height,
            device_scale_factor=device_matrix.deviceScaleFactor,
            device_mobile=device_matrix.mobile,
            device_fit_window=device_matrix.fitWindow,
            proxy_ip=proxy_details.ip,
            proxy_port=proxy_details.port,
            proxy_username=proxy_details.username,
            proxy_password=proxy_details.password,
            profile_name=profile_details.profile_name,
            login_mail=profile_details.account_details.login.mail,
            login_password=profile_details.account_details.login.password,
            recovery_mailbox=profile_details.account_details.password_recovery.recovery_mailbox,
            recovery_phone=profile_details.account_details.password_recovery.recovery_phone,
            actions_chain=actions_chain
        )
        db.add(profile)
        db.commit()

    response = subprocess.run(
        ["curl", "--location", f"http://127.0.0.1:8000/start-process?token_id={token_id}", 
         "--header", "accept: application/json"],
        capture_output=True, text=True
    )

    return {"status": "start", "response": response.stdout}

@app.post("/pause")
async def pause(token_id: str = Form(...)):
    response = subprocess.run(
    ["curl", "--location", f"http://127.0.0.1:8000/pause?token_id={token_id}", 
     "--header", "accept: application/json"],
        capture_output=True, text=True
    )
    return {"status": "paused", "response": response.stdout}

@app.post("/resume")
async def resume(token_id: str = Form(...)):
    response = subprocess.run(
        ["curl", "--location", f"http://127.0.0.1:8000/resume?token_id={token_id}", 
     "--header", "accept: application/json"],
        capture_output=True, text=True
    )
    return {"status": "resume", "response": response.stdout}

@app.post("/stop")
async def stop(token_id: str = Form(...)):
    response = subprocess.run(
        ["curl", "--location", f"http://127.0.0.1:8000/stop?token_id={token_id}", 
     "--header", "accept: application/json"],
        capture_output=True, text=True
    )
    return {"status": "stopped", "response": response.stdout}
