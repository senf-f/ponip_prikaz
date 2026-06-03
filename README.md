# Ponip Prikaz

Flask web application that displays Croatian property auction data in a sortable, filterable table. Reads from a database populated by the [ponip_scraper_v2](https://github.com/senf-f/ponip_scraper_v2) project.

## Local Development

```bash
git clone git@github.com:senf-f/ponip_prikaz.git
cd ponip_prikaz
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Development mode uses the SQLite database from the sibling `ponip_scraper_v2` directory.

## VPS Deployment

### 1. Clone and install

```bash
git clone git@github.com:senf-f/ponip_prikaz.git
cd ponip_prikaz
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set up PostgreSQL

```bash
sudo apt install postgresql
sudo -u postgres createdb ponip
sudo -u postgres createuser ponip_user -P
```

Make sure the scraper populates this database (or import existing data).

### 3. Create `.env`

```
ENVIRONMENT=production
SQLALCHEMY_DATABASE_URI=postgresql://ponip_user:yourpassword@localhost/ponip
```

### 4. Verify it runs

```bash
gunicorn wsgi:app --bind 0.0.0.0:8000
```

### 5. Systemd service

Create `/etc/systemd/system/ponip.service`:

```ini
[Unit]
Description=Ponip Prikaz
After=network.target

[Service]
User=youruser
WorkingDirectory=/path/to/ponip_prikaz
Environment="PATH=/path/to/ponip_prikaz/venv/bin"
ExecStart=/path/to/ponip_prikaz/venv/bin/gunicorn wsgi:app --bind 127.0.0.1:8000 --workers 2
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now ponip
```

### 6. Nginx reverse proxy

Create `/etc/nginx/sites-available/ponip`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/ponip /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

### 7. HTTPS

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```
