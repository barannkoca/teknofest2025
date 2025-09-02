# ECOMINDS - Yatırım Karar Destek Sistemi Makefile

.PHONY: help install start start-backend start-frontend stop test clean setup-env

# Varsayılan hedef
.DEFAULT_GOAL := help

# Renkli çıktı için
RED=\033[0;31m
GREEN=\033[0;32m
YELLOW=\033[1;33m
BLUE=\033[0;34m
NC=\033[0m # No Color

help: ## 📋 Kullanılabilir komutları göster
	@echo "${BLUE}🌍 ECOMINDS - Yatırım Karar Destek Sistemi${NC}"
	@echo "${BLUE}============================================${NC}"
	@echo ""
	@echo "${GREEN}Kullanılabilir komutlar:${NC}"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  ${YELLOW}%-15s${NC} %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "${BLUE}Örnek kullanım:${NC}"
	@echo "  make start     # Hem backend hem frontend'i başlat"
	@echo "  make setup     # İlk kurulum için gerekli paketleri yükle"
	@echo "  make test      # API'leri test et"

setup: ## 🔧 İlk kurulum - gerekli paketleri yükle
	@echo "${GREEN}📦 Frontend paketleri yükleniyor...${NC}"
	cd frontend && npm install
	@echo "${GREEN}✅ Kurulum tamamlandı!${NC}"
	@echo "${YELLOW}💡 Şimdi 'make start' ile uygulamayı başlatabilirsin${NC}"

install: setup ## 🔧 Alias for setup

start: ## 🚀 Hem backend hem frontend'i başlat (paralel)
	@echo "${GREEN}🚀 Backend ve Frontend başlatılıyor...${NC}"
	@echo "${YELLOW}⚠️  Backend: http://localhost:8000${NC}"
	@echo "${YELLOW}⚠️  Frontend: http://localhost:3000${NC}"
	@echo "${YELLOW}⚠️  Durdurmak için: Ctrl+C veya 'make stop'${NC}"
	@echo ""
	make -j2 start-backend start-frontend

start-backend: ## 🔧 Sadece backend'i başlat
	@echo "${GREEN}🐍 Backend başlatılıyor...${NC}"
	cd backend && source venv/bin/activate && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

start-frontend: ## ⚛️ Sadece frontend'i başlat
	@echo "${GREEN}⚛️  Frontend başlatılıyor...${NC}"
	cd frontend && npm start

dev: start ## 🛠️ Geliştirme modu (alias for start)

stop: ## ⏹️ Çalışan servisleri durdur
	@echo "${RED}⏹️  Servisler durduruluyor...${NC}"
	-pkill -f "uvicorn app.main:app"
	-pkill -f "react-scripts start"
	@echo "${GREEN}✅ Servisler durduruldu${NC}"

test: ## 🧪 API endpoint'lerini test et
	@echo "${GREEN}🧪 API testleri başlıyor...${NC}"
	@echo ""
	@echo "${BLUE}1. Health Check:${NC}"
	@curl -s http://localhost:8000/health | python3 -m json.tool || echo "${RED}❌ Backend çalışmıyor!${NC}"
	@echo ""
	@echo "${BLUE}2. Teknoloji sektörü testi:${NC}"
	@curl -s "http://localhost:8000/api/mod1?sector=Teknoloji%20%2F%20Yazılım&topn=3" | python3 -c "import sys,json; data=json.load(sys.stdin); print('✅ Sector:', data['sector']); print('🏆 Top cities:', [city['name'] for city in data['top5']])" || echo "${RED}❌ API hatası!${NC}"
	@echo ""
	@echo "${BLUE}3. İstanbul testi:${NC}"
	@curl -s "http://localhost:8000/api/mod2?city=İstanbul&topn=3" | python3 -c "import sys,json; data=json.load(sys.stdin); print('✅ City:', data['city']); print('🏆 Top sectors:', [sector['name'] for sector in data['top5']])" || echo "${RED}❌ API hatası!${NC}"
	@echo ""
	@echo "${GREEN}✅ Test tamamlandı${NC}"

test-quick: ## ⚡ Hızlı health check
	@curl -s http://localhost:8000/health > /dev/null && echo "${GREEN}✅ Backend çalışıyor${NC}" || echo "${RED}❌ Backend çalışmıyor${NC}"

logs-backend: ## 📋 Backend loglarını göster
	@echo "${GREEN}📋 Backend logları (Ctrl+C ile çık):${NC}"
	tail -f backend/logs/*.log 2>/dev/null || echo "Log dosyası bulunamadı"

status: ## 📊 Servislerin durumunu kontrol et
	@echo "${GREEN}📊 Servis Durumu:${NC}"
	@echo ""
	@echo -n "${BLUE}Backend (Port 8000): ${NC}"
	@curl -s http://localhost:8000/health > /dev/null && echo "${GREEN}✅ Çalışıyor${NC}" || echo "${RED}❌ Çalışmıyor${NC}"
	@echo -n "${BLUE}Frontend (Port 3000): ${NC}"
	@curl -s http://localhost:3000 > /dev/null && echo "${GREEN}✅ Çalışıyor${NC}" || echo "${RED}❌ Çalışmıyor${NC}"

clean: ## 🧹 Geçici dosyaları temizle
	@echo "${GREEN}🧹 Temizlik başlıyor...${NC}"
	cd frontend && rm -rf node_modules/.cache
	cd backend && find . -name "*.pyc" -delete
	cd backend && find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "${GREEN}✅ Temizlik tamamlandı${NC}"

reset: clean ## 🔄 Tam reset - node_modules'u da sil
	@echo "${YELLOW}🔄 Tam reset başlıyor...${NC}"
	cd frontend && rm -rf node_modules package-lock.json
	@echo "${GREEN}✅ Reset tamamlandı. 'make setup' ile yeniden kurulum yapın${NC}"

ports: ## 🔍 Kullanılan portları göster
	@echo "${GREEN}🔍 Port Kullanımı:${NC}"
	@echo "${BLUE}Port 8000 (Backend):${NC}"
	@lsof -ti:8000 > /dev/null && echo "${YELLOW}  🟡 Kullanımda${NC}" || echo "${GREEN}  ✅ Boş${NC}"
	@echo "${BLUE}Port 3000 (Frontend):${NC}"  
	@lsof -ti:3000 > /dev/null && echo "${YELLOW}  🟡 Kullanımda${NC}" || echo "${GREEN}  ✅ Boş${NC}"

kill-ports: ## ⚔️ 8000 ve 3000 portlarındaki işlemleri öldür
	@echo "${RED}⚔️  Port 8000 ve 3000 temizleniyor...${NC}"
	-lsof -ti:8000 | xargs kill -9 2>/dev/null || true
	-lsof -ti:3000 | xargs kill -9 2>/dev/null || true
	@echo "${GREEN}✅ Portlar temizlendi${NC}"

quick-start: kill-ports start ## ⚡ Portları temizle ve başlat

info: ## ℹ️ Proje bilgileri
	@echo "${BLUE}🌍 ECOMINDS - Proje Bilgileri${NC}"
	@echo "${BLUE}================================${NC}"
	@echo ""
	@echo "${GREEN}📁 Backend:${NC} FastAPI + Python"
	@echo "${GREEN}📁 Frontend:${NC} React + TypeScript + Mapbox"
	@echo "${GREEN}🌐 Backend URL:${NC} http://localhost:8000"
	@echo "${GREEN}🌐 Frontend URL:${NC} http://localhost:3000"
	@echo "${GREEN}📚 API Docs:${NC} http://localhost:8000/docs"
	@echo ""
	@echo "${YELLOW}💡 İpucu: 'make help' ile tüm komutları görebilirsin${NC}"

# Makefile için özel hedefler
check-backend:
	@cd backend && source venv/bin/activate && python -c "import app.main" > /dev/null 2>&1

check-frontend:
	@cd frontend && test -f package.json

validate: check-backend check-frontend ## ✅ Proje yapısını doğrula
	@echo "${GREEN}✅ Proje yapısı doğru${NC}"

