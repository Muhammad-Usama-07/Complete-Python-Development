from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from datetime import datetime
from database import Base

class FaceDetection(Base):
    __tablename__ = "face_detections"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Image information
    image_name = Column(String(255), nullable=False)
    image_size = Column(String(50))  # e.g., "1920x1080"
    
    # Detection results
    faces_detected = Column(Integer, default=0)
    face_locations = Column(JSON)  # Store as JSON array
    # Format: [{"x": 100, "y": 150, "width": 200, "height": 200}, ...]
    
    # Base64 encoded images
    image_with_boxes = Column(Text)  # Base64 string
    original_image = Column(Text)    # Base64 string of original image
    
    # Performance metrics
    detection_time_ms = Column(Float)  # Processing time in milliseconds
    confidence_score = Column(Float)   # Average confidence score
    
    # Metadata
    ip_address = Column(String(45))  # IPv4 or IPv6
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self, include_images=False):
        """Convert model to dictionary
        
        Args:
            include_images: If True, include base64 images (large data)
        """
        result = {
            "id": self.id,
            "image_name": self.image_name,
            "image_size": self.image_size,
            "faces_detected": self.faces_detected,
            "face_locations": self.face_locations,
            "detection_time_ms": self.detection_time_ms,
            "confidence_score": self.confidence_score,
            "ip_address": self.ip_address,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        
        if include_images:
            result["image_with_boxes"] = self.image_with_boxes
            result["original_image"] = self.original_image
        
        return result
    
    def __repr__(self):
        return f"<FaceDetection(id={self.id}, image='{self.image_name}', faces={self.faces_detected})>"