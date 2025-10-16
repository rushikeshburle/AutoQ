# AutoQ Deployment Guide

## Production Deployment Options

### 1. Docker Deployment (Recommended)

#### Prerequisites
- Docker and Docker Compose installed
- Domain name configured
- SSL certificate (Let's Encrypt recommended)

#### Steps

1. **Clone repository:**
   ```bash
   git clone https://github.com/yourusername/AutoQ.git
   cd AutoQ
   ```

2. **Configure environment:**
   ```bash
   cp backend/.env.example backend/.env
   nano backend/.env
   ```

   Update these critical values:
   ```env
   SECRET_KEY=<generate-with-openssl-rand-hex-32>
   JWT_SECRET_KEY=<generate-with-openssl-rand-hex-32>
   DEBUG=False
   DATABASE_URL=postgresql://autoq_user:STRONG_PASSWORD@db:5432/autoq_db
   ALLOWED_ORIGINS=https://yourdomain.com
   ```

3. **Update docker-compose.yml:**
   ```yaml
   # Change PostgreSQL password
   environment:
     POSTGRES_PASSWORD: STRONG_PASSWORD_HERE
   ```

4. **Deploy:**
   ```bash
   docker-compose up -d
   ```

5. **Setup Nginx reverse proxy:**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       return 301 https://$server_name$request_uri;
   }

   server {
       listen 443 ssl http2;
       server_name yourdomain.com;

       ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

       # Frontend
       location / {
           proxy_pass http://localhost:3000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       # Backend API
       location /api {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### 2. Cloud Deployment

#### AWS Deployment

**Using EC2:**

1. Launch EC2 instance (t3.medium or larger)
2. Install Docker and Docker Compose
3. Configure security groups (ports 80, 443)
4. Follow Docker deployment steps above
5. Use RDS for PostgreSQL (recommended)
6. Use S3 for file storage (optional)

**Using ECS:**

1. Build and push Docker images to ECR
2. Create ECS cluster
3. Define task definitions
4. Create services
5. Configure Application Load Balancer
6. Use RDS for database

#### Azure Deployment

1. Create Azure Container Instances or App Service
2. Use Azure Database for PostgreSQL
3. Configure Azure Blob Storage for files
4. Set up Application Gateway

#### Google Cloud Deployment

1. Use Cloud Run for containers
2. Cloud SQL for PostgreSQL
3. Cloud Storage for files
4. Cloud Load Balancing

### 3. VPS Deployment (DigitalOcean, Linode, etc.)

1. **Create droplet/VPS:**
   - Ubuntu 22.04 LTS
   - 4GB RAM minimum
   - 50GB storage

2. **Initial setup:**
   ```bash
   # Update system
   apt update && apt upgrade -y

   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh

   # Install Docker Compose
   apt install docker-compose -y

   # Create user
   adduser autoq
   usermod -aG docker autoq
   ```

3. **Deploy application:**
   ```bash
   su - autoq
   git clone https://github.com/yourusername/AutoQ.git
   cd AutoQ
   # Follow Docker deployment steps
   ```

4. **Setup firewall:**
   ```bash
   ufw allow 22
   ufw allow 80
   ufw allow 443
   ufw enable
   ```

### 4. Manual Production Deployment

#### Backend

1. **Setup Python environment:**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

2. **Install Gunicorn:**
   ```bash
   pip install gunicorn
   ```

3. **Create systemd service:**
   ```bash
   sudo nano /etc/systemd/system/autoq.service
   ```

   ```ini
   [Unit]
   Description=AutoQ FastAPI Application
   After=network.target

   [Service]
   User=autoq
   Group=autoq
   WorkingDirectory=/home/autoq/AutoQ/backend
   Environment="PATH=/home/autoq/AutoQ/backend/venv/bin"
   ExecStart=/home/autoq/AutoQ/backend/venv/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

   [Install]
   WantedBy=multi-user.target
   ```

4. **Start service:**
   ```bash
   sudo systemctl start autoq
   sudo systemctl enable autoq
   ```

#### Frontend

1. **Build frontend:**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Serve with Nginx:**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       root /home/autoq/AutoQ/frontend/dist;
       index index.html;

       location / {
           try_files $uri $uri/ /index.html;
       }

       location /api {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## Security Checklist

- [ ] Change all default passwords
- [ ] Generate strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_ORIGINS properly
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Set up firewall (UFW, Security Groups)
- [ ] Regular security updates
- [ ] Backup database regularly
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting (optional)
- [ ] Set up monitoring and logging
- [ ] Restrict database access
- [ ] Use strong PostgreSQL password

## Database Setup

### PostgreSQL Production Setup

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql

CREATE DATABASE autoq_db;
CREATE USER autoq_user WITH PASSWORD 'STRONG_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE autoq_db TO autoq_user;
\q
```

### Database Backups

**Automated backup script:**
```bash
#!/bin/bash
# /home/autoq/backup.sh

BACKUP_DIR="/home/autoq/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup
docker-compose exec -T db pg_dump -U autoq_user autoq_db > "$BACKUP_DIR/autoq_$DATE.sql"

# Keep only last 7 days
find $BACKUP_DIR -name "autoq_*.sql" -mtime +7 -delete
```

**Add to crontab:**
```bash
crontab -e
# Add: 0 2 * * * /home/autoq/backup.sh
```

## Monitoring

### Basic Monitoring

```bash
# Check service status
systemctl status autoq

# View logs
journalctl -u autoq -f

# Docker logs
docker-compose logs -f
```

### Advanced Monitoring

Consider using:
- **Prometheus + Grafana** for metrics
- **ELK Stack** for log aggregation
- **Sentry** for error tracking
- **Uptime Robot** for uptime monitoring

## Performance Optimization

### Backend

1. **Use Gunicorn with multiple workers:**
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Enable caching with Redis:**
   ```python
   # Add Redis caching for frequently accessed data
   ```

3. **Database connection pooling:**
   ```python
   # Already configured in SQLAlchemy
   ```

### Frontend

1. **Build optimization:**
   ```bash
   npm run build
   # Vite automatically optimizes
   ```

2. **Enable Nginx gzip:**
   ```nginx
   gzip on;
   gzip_types text/plain text/css application/json application/javascript;
   ```

3. **Browser caching:**
   ```nginx
   location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
       expires 1y;
       add_header Cache-Control "public, immutable";
   }
   ```

## Scaling

### Horizontal Scaling

1. **Load balancer** (Nginx, HAProxy, AWS ALB)
2. **Multiple backend instances**
3. **Shared database** (PostgreSQL with replication)
4. **Shared file storage** (S3, NFS)
5. **Redis for session management**

### Vertical Scaling

- Increase server resources (CPU, RAM)
- Optimize database queries
- Add database indexes
- Use CDN for static files

## SSL Certificate Setup

### Let's Encrypt (Free)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

## Environment Variables Reference

### Production Backend .env

```env
# Application
APP_NAME=AutoQ
APP_VERSION=1.0.0
DEBUG=False
SECRET_KEY=<generate-strong-key>
ALLOWED_ORIGINS=https://yourdomain.com

# Database
DATABASE_URL=postgresql://autoq_user:PASSWORD@localhost:5432/autoq_db

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=<generate-strong-key>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Storage
UPLOAD_DIR=/var/autoq/uploads
MAX_UPLOAD_SIZE=52428800

# Institution
INSTITUTION_NAME=Your Institution Name
```

## Troubleshooting Production Issues

### Service won't start
```bash
# Check logs
journalctl -u autoq -n 50

# Check permissions
ls -la /home/autoq/AutoQ

# Test manually
cd /home/autoq/AutoQ/backend
source venv/bin/activate
uvicorn app.main:app
```

### Database connection errors
```bash
# Test connection
psql -U autoq_user -d autoq_db -h localhost

# Check PostgreSQL status
systemctl status postgresql
```

### High memory usage
```bash
# Check processes
htop

# Reduce Gunicorn workers
# Optimize database queries
# Add caching
```

## Maintenance

### Regular Tasks

- **Daily**: Check logs for errors
- **Weekly**: Review disk space, backup verification
- **Monthly**: Security updates, dependency updates
- **Quarterly**: Performance review, optimization

### Update Procedure

```bash
# Backup first
./backup.sh

# Pull updates
git pull origin main

# Update backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart autoq

# Update frontend
cd ../frontend
npm install
npm run build
sudo systemctl reload nginx
```

## Support

For deployment issues:
1. Check logs first
2. Review this documentation
3. Open GitHub issue
4. Contact support

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
