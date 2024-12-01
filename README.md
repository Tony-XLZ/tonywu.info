# tonywu.info

## Project Description

**tonywu.info** is a personal website designed to showcase the author's projects and blog posts. The target audience includes those interested in learning about the author's professional skills, project experience, and viewpoints. The project page displays various completed projects, while the blog page provides in-depth discussions on different topics. You can follow the instructions to build your own version.

## Project Structure

- **Homepage**: Displays an introduction of me, along with a summary of projects and blog posts and links to details.
- **Project Detail Page**: Displays detailed descriptions.
- **Blog Detail Page**: Displays detailed blog posts.

## Tech Stack

- **Backend**: Django 5.1.3
- **Database**: PostgreSQL
- **Frontend**: Django's built-in template system, Bootstrap
- **Deployment Tools**: Gunicorn, Nginx

## Installation and Running

### Prerequisites

- Python 3.11
- PostgreSQL Database

### Installation Steps

1. Clone the project repository:
   ```bash
   git clone https://github.com/tonyxlz/Portfolio_with_Django.git
   cd Portfolio_with_Django
   ```

2. Create and activate a virtual environment:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

3. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   Create a database in PostgreSQL and update the database configuration in the project's `settings.py`.


5. Migrate the database:
   ```bash
   python manage.py migrate
   ```

6. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

Note: Some values in the following configurations (e.g., `<YOUR_USERNAME>`, `<YOUR_IP_ADDRESS>`, `<YOUR_DOMAIN>`) are placeholders. Please replace them with your actual deployment environment values.

### Gunicorn Configuration

Use Gunicorn as the WSGI server. Create a `gunicorn.service` file in the `/etc/systemd/system/` directory with the following content:

```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=<YOUR_USERNAME>
Group=www-data
WorkingDirectory=/home/<YOUR_USERNAME>/Portfolio_with_Django
ExecStart=/home/<YOUR_USERNAME>/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          Portfolio_with_Django.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Nginx Configuration

Create or edit the Nginx configuration file for the project in `/etc/nginx/sites-available/`:

```nginx
server {
    listen 80;
    server_name <YOUR_IP_ADDRESS> <YOUR_DOMAIN> www.<YOUR_DOMAIN>;

    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name <YOUR_DOMAIN> www.<YOUR_DOMAIN>;

    ssl_certificate /etc/letsencrypt/live/<YOUR_DOMAIN>/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/<YOUR_DOMAIN>/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /home/<YOUR_USERNAME>/Portfolio_with_Django/static/;
    }
    
    location /media/ {
        alias /home/<YOUR_USERNAME>/Portfolio_with_Django/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

### Starting and Managing Services

- Reload systemd to apply the configuration:
  ```bash
  sudo systemctl daemon-reload
  ```

- Start the Gunicorn service and enable it to start at boot:
  ```bash
  sudo systemctl start gunicorn
  sudo systemctl enable gunicorn
  ```

- Restart Nginx:
  ```bash
  sudo systemctl restart nginx
  ```

## Contributing

Contributions of any kind are welcome. If you find any issues or have suggestions for improvements, feel free to submit an issue or a pull request.

## License

This project is licensed under the MIT License.

