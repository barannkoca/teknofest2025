"""
Vercel için FastAPI uygulaması giriş noktası
"""

import sys
import os

# Backend app klasörünü Python path'ine ekle
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.main import app

# Vercel için gerekli
handler = app
