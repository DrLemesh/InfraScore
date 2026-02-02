#!/bin/bash

echo "🚀 Starting InfraScore Upgrade Process..."

# 1. Update Secrets (Global)
echo "🔒 Applying Secrets..."
if [ -f "./helm/secrets.yaml" ]; then
    # We pass secrets to charts usually, but if there are global secrets applied directly:
    # kubectl apply -f ./helm/secret-manifests.yaml (if any exist independently)
    # Since we use --values ./helm/secrets.yaml for charts, we just verify it exists.
    echo "✅ Found secrets.yaml"
else
    echo "❌ secrets.yaml not found! Please create it from templates."
    exit 1
fi

# 1.5. Ingress Controller (System)
echo "🚦 Upgrading Ingress Controller..."
helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
    -n infrascore --create-namespace \
    --wait


# 2. Database
echo "🗄️  Upgrading Database..."
helm upgrade --install infrascore-db ./helm/database-chart \
    -f ./helm/secrets.yaml \
    -n infrascore --create-namespace \
    --wait

# 3. Backend
echo "⚙️  Upgrading Backend..."
helm upgrade --install infrascore-backend ./helm/backend-chart \
    -f ./helm/secrets.yaml \
    -n infrascore --create-namespace \
    --wait

# 4. Frontend
echo "💻 Upgrading Frontend..."
helm upgrade --install infrascore-frontend ./helm/frontend-chart \
    -n infrascore --create-namespace \
    --wait

# 5. pgAdmin
echo "🐘 Upgrading pgAdmin..."
helm upgrade --install infrascore-pgadmin ./helm/pgadmin-chart \
    -f ./helm/secrets.yaml \
    -n infrascore --create-namespace \
    --wait

# 6. Ingress
echo "🌐 Applying Ingress Configuration..."
kubectl apply -f ./helm/ingress.yaml -n infrascore

echo "✨ All upgrades completed successfully! Access your app at http://localhost"
