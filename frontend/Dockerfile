FROM nginx:alpine

# Copy static assets
COPY static /usr/share/nginx/html/static

# Copy Nginx configuration template
COPY nginx.conf.template /etc/nginx/templates/default.conf.template


# Nginx 1.19+ automatically runs envsubst on templates in /etc/nginx/templates/
# So we don't need a custom entrypoint script!

EXPOSE 80
