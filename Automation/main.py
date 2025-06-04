from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, String, Boolean, Integer, Float, JSON, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
import shutil
from datetime import datetime
import threading
import time
import json
from decimal import Decimal
from packages.gm_pkg import GmailServices
from packages.driver_config import DriverConfig
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from io import BytesIO

# FastAPI app
app = FastAPI()

# Database setup
DATABASE_URL = "mysql+pymysql://root:root_db_hello111@localhost:3307/mail_auto_db"
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Profile model
class Profile(Base):
    __tablename__ = "config"
    token_id = Column(String(255), primary_key=True, index=True)
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
    process_id = Column(String(255))
    process_status = Column(String(255))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

Base.metadata.create_all(bind=engine)

# Thread-safe process tracking
processes = {}
processes_lock = threading.Lock()

# Thread-safe logging
log_lock = threading.Lock()

def create_directory(token_id):
    token_id = str(token_id)
    base_dir = os.path.join(os.getcwd(), token_id)
    archive_dir = os.path.join(os.getcwd(), "archive")
    os.makedirs(archive_dir, exist_ok=True)

    if os.path.exists(base_dir):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archived_dir = os.path.join(archive_dir, f"{token_id}_{timestamp}")
        shutil.move(base_dir, archived_dir)

    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(os.path.join(base_dir, "screenshots"), exist_ok=True)

    with open(os.path.join(base_dir, "config.json"), "w") as f:
        f.write("{}")
    with open(os.path.join(base_dir, "log.txt"), "w") as f:
        f.write("Log entries\n")

    return base_dir

def log_message(token_id, message):
    log_file_path = os.path.join(token_id, "log.txt")
    with log_lock:
        with open(log_file_path, "a", encoding="utf-8") as log_file:
            log_file.write(message + "\n")

def save_screenshot(image, token_id, image_name):
    img_file_path = os.path.join(token_id, "screenshots", f"{image_name}.png")
    image.save(img_file_path)

driver_lock = threading.Lock()

def initialize_driver(config_data):
    try:
        with driver_lock:
            driver_config = DriverConfig(config_data)
            driver = driver_config.configure_driver()
            if driver is None or isinstance(driver, str):
                print(f"Driver init failed: {driver if isinstance(driver, str) else 'Unknown error'}")
                return None
            return driver
    except Exception as e:
        print(f"Driver initialization crashed: {str(e)}")
        return None

def open_gmail_task(token_id, json_data, status_dict):
    pid = os.getpid()
    db = SessionLocal()
    driver = None
    try:
        driver = initialize_driver(json_data)
        if driver is None:
            log_message(token_id, "Error initializing driver")
            status_dict['running'] = False
            return

        log_message(token_id, "Driver initialized successfully")
        email = json_data['profile_details']['account_details']['login']['mail']
        password = json_data['profile_details']['account_details']['login']['password']
        mail_service = GmailServices(email, password, driver)
        actions = json_data['actions_chain']
        current_step_local = status_dict.get('current_step', 0)

        while status_dict.get('running', True) and current_step_local < len(actions):
            if status_dict.get('paused', False):
                time.sleep(0.5)
                continue
            try:
                action = actions[current_step_local]
                action_log_ss = execute_action(mail_service, action, token_id, pid)
                action_log = ''.join(action_log_ss['logs'])
                for image_name, image in action_log_ss['ss'].items():
                    save_screenshot(image, token_id, image_name)
                log_message(token_id, action_log)
                current_step_local += 1
                status_dict['current_step'] = current_step_local
            except Exception as e:
                screenshot = driver.get_screenshot_as_png()
                last_screenshot = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                filename = f'Error_last_screenshot_{date_time_prog}'
                log_message(token_id, f"Error during action execution at {date_time_prog}: {str(e)}")
                save_screenshot(last_screenshot, token_id, filename)
                status_dict['running'] = False
                break

        if current_step_local >= len(actions):
            profile = db.query(Profile).filter(Profile.token_id == token_id).first()
            if profile:
                profile.process_status = "complete"
                db.commit()
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                message = f"\n\nToken id: {token_id} Process id: {pid} All actions completed at {date_time_prog}\n"
                log_message(token_id, message)
                if driver:
                    screenshot = driver.get_screenshot_as_png()
                    last_screenshot = Image.open(BytesIO(screenshot))
                    filename = message.replace(' ', '_').replace(':', '')
                    save_screenshot(last_screenshot, token_id, filename)
                    driver.quit()
                status_dict['running'] = False
    except Exception as e:
        error_msg = f"Critical error in process {pid}: {str(e)}"
        log_message(token_id, error_msg)
        profile = db.query(Profile).filter(Profile.token_id == token_id).first()
        if profile:
            profile.process_status = "failed"
            db.commit()
        if driver:
            driver.quit()
        status_dict['running'] = False
    finally:
        db.close()

def execute_action(class_instance, action, token_id, pid):
    if isinstance(action, list):
        if len(action) == 1 and isinstance(action[0], int):
            time.sleep(action[0])
            log_ss = {}
        else:
            method_name, *args = action
            method = getattr(class_instance, method_name)
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            message = f"Token id: {token_id} Process id: {pid} Work on actions {action} started at {date_time_prog}\n"
            log_message(token_id, message)
            log_ss = method(*args)
            time.sleep(1)
        log_ss = log_ss[1]
        return log_ss
    else:
        raise ValueError(f"Invalid action format: {action}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def run_task_in_thread(token_id, config_data, status_dict):
    thread = threading.Thread(
        target=open_gmail_task,
        args=(token_id, config_data, status_dict),
        daemon=True
    )
    thread.start()
    return thread

@app.get("/start-process")
def start_process(token_id: str, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.token_id == token_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    config_data = {
        "token_id": profile.token_id,
        "browser_details": {
            "user_agent": profile.browser_user_agent,
            "browser_type": profile.browser_type,
            "language": profile.browser_language,
            "geo_location": {
                "latitude": Decimal(profile.geo_latitude),
                "longitude": Decimal(profile.geo_longitude)
            },
            "timezone": {
                "timezoneId": profile.timezone_id
            },
            "other_settings": {
                "enable_javascript": profile.enable_javascript,
                "accept_ssl_certificates": profile.accept_ssl_certificates,
                "headless": profile.headless,
                "disable_images": profile.disable_images
            }
        },
        "device_matrix": {
            "width": profile.device_width,
            "height": profile.device_height,
            "deviceScaleFactor": Decimal(profile.device_scale_factor),
            "mobile": profile.device_mobile,
            "fitWindow": profile.device_fit_window
        },
        "proxy_details": {
            "ip": profile.proxy_ip,
            "port": profile.proxy_port,
            "username": profile.proxy_username,
            "password": profile.proxy_password
        },
        "profile_details": {
            "profile_name": profile.profile_name,
            "account_details": {
                "login": {
                    "mail": profile.login_mail,
                    "password": profile.login_password
                },
                "password_recovery": {
                    "recovery_mailbox": profile.recovery_mailbox,
                    "recovery_phone": profile.recovery_phone
                }
            }
        },
        "actions_chain": profile.actions_chain
    }

    create_directory(profile.token_id)

    with processes_lock:
        if token_id in processes and processes[token_id]['running']:
            return {"message": "Process is already running", "process_id": None}

        processes[token_id] = {
            "running": True,
            "paused": False,
            "current_step": 0
        }
        run_task_in_thread(token_id, config_data, processes[token_id])

    profile.process_status = "started"
    db.commit()
    return {
        "token_id": profile.token_id,
        "message": "Process started",
        "process_id": None
    }

@app.get("/pause")
def pause(token_id: str, db: Session = Depends(get_db)):
    with processes_lock:
        if token_id in processes and processes[token_id]['running']:
            processes[token_id]['paused'] = True
            profile = db.query(Profile).filter(Profile.token_id == token_id).first()
            if profile:
                profile.process_status = "paused"
                db.commit()
            log_message(token_id, "paused")
            return {"message": "Process paused", "process_id": None}
    raise HTTPException(status_code=404, detail="No active process for this token_id")

@app.get("/resume")
def resume(token_id: str, db: Session = Depends(get_db)):
    with processes_lock:
        if token_id in processes and processes[token_id]['running']:
            processes[token_id]['paused'] = False
            profile = db.query(Profile).filter(Profile.token_id == token_id).first()
            if profile:
                profile.process_status = "resumed"
                db.commit()
            log_message(token_id, "resumed")
            return {"message": "Process resumed", "process_id": None}
    raise HTTPException(status_code=404, detail="No active process for this token_id")

@app.get("/stop")
def stop(token_id: str, db: Session = Depends(get_db)):
    with processes_lock:
        if token_id in processes and processes[token_id]['running']:
            processes[token_id]['running'] = False
            profile = db.query(Profile).filter(Profile.token_id == token_id).first()
            if profile:
                profile.process_status = "stopped"
                db.commit()
            log_message(token_id, "stopped")
            return {"message": "Process stopped", "process_id": None}
    raise HTTPException(status_code=404, detail="No active process for this token_id")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
