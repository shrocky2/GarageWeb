# Purchase a domain
- Go to https://domains.google.com/ and get your own domain.
- Create a record to point the domain to your public IP address. Use that record (garage.example.com) for the rest of this tutorial. The public address of the Pi would be the same as the public address of the router you set up port forwarding on. After you complete this, you will need to shift port forwarding from 5000 to 443 You only need one of these two records:
    - An A record to point to the public IP address of your router (like garage.example.com A x.x.x.x). 
    - Dynamic DNS record that will auto-update the IP address of your router when your ISP changes it. For this, you would create a synthetic record of the subdomain, then use the username and password provided to paste on your router to update the Dynamic DNS record automatically.

# Install NGINX and deploy your certificate

This deploys a self-signed certificate. You will need to rekey it after a year, or switch to a hosted certificate by replacing cert.key and cert.crt.

**While this is not best practice and a certificate from an official certificate authority is best, this will get you started on using HTTPS. Update cert.key and cert.crt when you have completed a csr to a trusted authority.**

~~~
sudo apt update
sudo apt install nginx
cd /etc/nginx
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/cert.key -out /etc/nginx/cert.crt
~~~

Here, it will ask you questions to fill out the information for the certificate. Keep an eye for where it asks you to abbreviate and where it asks you to spell out locations. The most important part of this section is the common name needs to be the fully qualified domain name (FQDN) of the service you are trying to connect to. 

# Configure NGINX to use HTTPS
~~~
cd /etc/nginx/sites-available/
sudo cp default default-backup
sudo nano /etc/nginx/sites-available/default
~~~

Remove all contents from this file and use the following. Change the parts that say changeme.example.com or changeme to your fully qualified domain name (FQDN). HTTP redirect may be broken on IP addresses, but should work with the hostname when you have it set up on DNS.

~~~
server {
    listen 80;
    return 301 https://$host$request_uri;
}

server {

    listen 443;
    server_name changeme.example.com;

    ssl_certificate           /etc/nginx/cert.crt;
    ssl_certificate_key       /etc/nginx/cert.key;

    ssl on;
    ssl_session_cache  builtin:1000  shared:SSL:10m;
    ssl_protocols  TLSv1.2;
    ssl_ciphers HIGH:!aNULL:!eNULL:!EXPORT:!CAMELLIA:!DES:!MD5:!PSK:!RC4;
    ssl_prefer_server_ciphers on;

    access_log            /var/log/nginx/changeme.access.log;

    location / {

      proxy_set_header        Host $host;
      proxy_set_header        X-Real-IP $remote_addr;
      proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header        X-Forwarded-Proto $scheme;

      # Fix the “It appears that your reverse proxy set up is broken" error.
      proxy_pass          http://localhost:5000;
      proxy_read_timeout  90;

      proxy_redirect      http://localhost:5000 https://changeme.example.com;
    }
  }
  ~~~

# Configure and Enable The Firewall

Ensure the firewall is installed

~~~
sudo apt install ufw
~~~

Configure UFW to allow the necessary resources.

~~~
sudo ufw allow https
sudo ufw allow ssh
sudo ufw enable
~~~

If you want to allow the http to https redirect on nginx, also run the following command:

~~~
sudo ufw alow http
~~~

  # References:
  - https://www.digitalocean.com/community/tutorials/how-to-configure-nginx-with-ssl-as-a-reverse-proxy-for-jenkins
