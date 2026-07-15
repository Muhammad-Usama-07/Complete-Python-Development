import os
import sys
import base64
import urllib.request
import numpy as np
import time
from flask import Flask, request, jsonify
from sqlalchemy.orm import Session

# ===== FIX: OpenCV import compatibility =====
try:
    import cv2
    if not hasattr(cv2, 'CascadeClassifier'):
        import cv2.cv2 as cv2
except ImportError:
    import cv2.cv2 as cv2

# Database imports
from database import init_db, SessionLocal
from models import FaceDetection

app = Flask(__name__)

# Initialize database
init_db()

def load_face_cascade():
    """Reliably load face cascade classifier"""
    print("🔍 Looking for cascade file...")
    
    # Check local file first
    local_path = 'haarcascade_frontalface_default.xml'
    if os.path.exists(local_path) and os.path.getsize(local_path) > 1000:
        print(f"✅ Found cascade locally: {local_path}")
        cascade = cv2.CascadeClassifier(local_path)
        if not cascade.empty():
            print("✅ Cascade loaded successfully!")
            return cascade
    
    # Try OpenCV's built-in path
    try:
        if hasattr(cv2, 'data') and hasattr(cv2.data, 'haarcascades'):
            builtin = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            if os.path.exists(builtin):
                cascade = cv2.CascadeClassifier(builtin)
                if not cascade.empty():
                    print(f"✅ Loaded from OpenCV: {builtin}")
                    return cascade
    except:
        pass
    
    # Download as last resort
    print("📥 Downloading cascade file...")
    url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
    
    try:
        urllib.request.urlretrieve(url, local_path)
        if os.path.exists(local_path) and os.path.getsize(local_path) > 1000:
            cascade = cv2.CascadeClassifier(local_path)
            if not cascade.empty():
                print("✅ Downloaded and loaded successfully!")
                return cascade
    except Exception as e:
        print(f"❌ Download failed: {e}")
    
    raise RuntimeError("Could not load face cascade classifier!")

# Print OpenCV info
print(f"📌 OpenCV version: {cv2.__version__}")
print(f"📌 OpenCV location: {cv2.__file__}")

# Load the cascade
face_cascade = load_face_cascade()

@app.route('/')
def home():
    return jsonify({
        "message": "Face Recognition API with Database",
        "version": "2.0",
        "opencv_version": cv2.__version__,
        "endpoints": {
            "/detect": "POST - Detect faces and save to database",
            "/history": "GET - Get detection history",
            "/history/<id>": "GET - Get specific detection",
            "/stats": "GET - Get detection statistics",
            "/health": "GET - Check API health"
        }
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "opencv_version": cv2.__version__,
        "cascade_loaded": not face_cascade.empty(),
        "database": "connected"
    })

@app.route('/detect', methods=['POST'])
def detect_faces():
    """Detect faces and save results to database"""
    start_time = time.time()
    
    try:
        # Check if face_cascade is loaded
        if face_cascade is None or face_cascade.empty():
            return jsonify({"error": "Face cascade not loaded"}), 500
        
        # Check if image is in request
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        # Get image from request
        file = request.files['image']
        image_name = file.filename or "unknown.jpg"
        
        # Read image
        img_bytes = file.read()
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({"error": "Invalid image"}), 400
        
        # Get image dimensions
        height, width = img.shape[:2]
        image_size = f"{width}x{height}"
        
        # Save original image as base64
        _, original_buffer = cv2.imencode('.jpg', img)
        original_base64 = base64.b64encode(original_buffer).decode('utf-8')
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # Calculate detection time
        detection_time = (time.time() - start_time) * 1000  # Convert to ms
        
        # Draw rectangles
        face_locations = []
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            face_locations.append({
                "x": int(x), 
                "y": int(y), 
                "width": int(w), 
                "height": int(h)
            })
        
        # Convert image with boxes to base64
        _, buffer = cv2.imencode('.jpg', img)
        img_with_boxes_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # Calculate average confidence (approximate based on face size ratio)
        avg_confidence = 0.0
        if len(faces) > 0:
            confidences = []
            for (x, y, w, h) in faces:
                # Simple heuristic: larger faces relative to image = higher confidence
                face_area_ratio = (w * h) / (width * height)
                confidence = min(face_area_ratio * 100, 1.0)  # Normalize
                confidences.append(confidence)
            avg_confidence = sum(confidences) / len(confidences)
        
        # Get client IP
        ip_address = request.remote_addr or "unknown"
        
        # Save to database
        db = SessionLocal()
        try:
            detection_record = FaceDetection(
                image_name=image_name,
                image_size=image_size,
                faces_detected=len(faces),
                face_locations=face_locations,
                image_with_boxes=img_with_boxes_base64,
                original_image=original_base64,
                detection_time_ms=round(detection_time, 2),
                confidence_score=round(avg_confidence, 2),
                ip_address=ip_address
            )
            
            db.add(detection_record)
            db.commit()
            db.refresh(detection_record)
            
            detection_id = detection_record.id
            
        except Exception as e:
            db.rollback()
            return jsonify({"error": f"Database error: {str(e)}"}), 500
        finally:
            db.close()
        
        # Return response (without images to reduce payload)
        return jsonify({
            "id": detection_id,
            "image_name": image_name,
            "image_size": image_size,
            "faces_detected": len(faces),
            "face_locations": face_locations,
            "detection_time_ms": round(detection_time, 2),
            "confidence_score": round(avg_confidence, 2),
            "message": "Detection saved to database"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    """Get detection history (without images to save bandwidth)"""
    try:
        # Get query parameters for pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        offset = (page - 1) * per_page
        
        db = SessionLocal()
        try:
            # Get total count
            total = db.query(FaceDetection).count()
            
            # Get records with pagination
            detections = db.query(FaceDetection)\
                .order_by(FaceDetection.created_at.desc())\
                .offset(offset)\
                .limit(per_page)\
                .all()
            
            # Convert to dictionaries (without images)
            history = [detection.to_dict(include_images=False) for detection in detections]
            
            return jsonify({
                "total": total,
                "page": page,
                "per_page": per_page,
                "total_pages": (total + per_page - 1) // per_page,
                "detections": history
            })
            
        finally:
            db.close()
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/history/<int:detection_id>', methods=['GET'])
def get_detection(detection_id):
    """Get specific detection with images"""
    try:
        # Check if images should be included
        include_images = request.args.get('include_images', 'false').lower() == 'true'
        
        db = SessionLocal()
        try:
            detection = db.query(FaceDetection)\
                .filter(FaceDetection.id == detection_id)\
                .first()
            
            if not detection:
                return jsonify({"error": "Detection not found"}), 404
            
            return jsonify(detection.to_dict(include_images=include_images))
            
        finally:
            db.close()
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get detection statistics"""
    try:
        db = SessionLocal()
        try:
            # Total detections
            total_detections = db.query(FaceDetection).count()
            
            # Total faces detected
            from sqlalchemy import func
            total_faces = db.query(func.sum(FaceDetection.faces_detected)).scalar() or 0
            
            # Average processing time
            avg_time = db.query(func.avg(FaceDetection.detection_time_ms)).scalar() or 0
            
            # Average faces per image
            avg_faces = total_faces / total_detections if total_detections > 0 else 0
            
            # Recent detections (last 24 hours)
            from datetime import datetime, timedelta
            last_24h = datetime.utcnow() - timedelta(hours=24)
            recent = db.query(FaceDetection)\
                .filter(FaceDetection.created_at >= last_24h)\
                .count()
            
            # Images with most faces
            most_faces = db.query(FaceDetection)\
                .order_by(FaceDetection.faces_detected.desc())\
                .limit(5)\
                .all()
            
            return jsonify({
                "total_detections": total_detections,
                "total_faces_detected": total_faces,
                "average_faces_per_image": round(avg_faces, 2),
                "average_processing_time_ms": round(avg_time, 2),
                "detections_last_24h": recent,
                "top_detections": [
                    {
                        "id": d.id,
                        "image_name": d.image_name,
                        "faces_detected": d.faces_detected,
                        "date": d.created_at.isoformat()
                    } for d in most_faces
                ]
            })
            
        finally:
            db.close()
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Face Detection API with Database...")
    app.run(host='0.0.0.0', port=5000, debug=False)