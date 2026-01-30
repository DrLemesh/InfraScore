#!/bin/bash

echo "🔄 Restarting all InfraScore deployments..."

# Backend
kubectl rollout restart deployment infrascore-backend-backend-chart
echo "  - Backend restarted"

# Frontend
kubectl rollout restart deployment infrascore-frontend-frontend-chart
echo "  - Frontend restarted"

# pgAdmin
kubectl rollout restart deployment infrascore-pgadmin-pgadmin-chart
echo "  - pgAdmin restarted"

# Database
kubectl rollout restart deployment infrascore-db-database-chart
echo "  - Database restarted"

echo "✅ All rollouts initiated."
