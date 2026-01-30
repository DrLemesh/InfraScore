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

# 2. Database
echo "🗄️  Upgrading Database..."
helm upgrade --install infrascore-db ./helm/database-chart \
    -f ./helm/secrets.yaml \
    --wait

# 3. Backend
echo "⚙️  Upgrading Backend..."
helm upgrade --install infrascore-backend ./helm/backend-chart \
    -f ./helm/secrets.yaml \
    --wait

# 4. Frontend
echo "💻 Upgrading Frontend..."
helm upgrade --install infrascore-frontend ./helm/frontend-chart \
    --wait

# 5. pgAdmin
echo "🐘 Upgrading pgAdmin..."
helm upgrade --install infrascore-pgadmin ./helm/pgadmin-chart \
    -f ./helm/secrets.yaml \
    --wait

# 6. Ingress
echo "🌐 Applying Ingress Configuration..."
kubectl apply -f ./helm/ingress.yaml

echo "✨ All upgrades completed successfully! Access your app at http://localhost"
