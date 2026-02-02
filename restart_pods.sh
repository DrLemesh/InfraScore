#!/bin/bash

echo "🔄 Restarting all InfraScore deployments in 'infrascore' namespace..."

# Backend
kubectl rollout restart deployment infrascore-backend-backend-chart -n infrascore
echo "  - Backend restarted"

# Frontend
kubectl rollout restart deployment infrascore-frontend-frontend-chart -n infrascore
echo "  - Frontend restarted"

# pgAdmin
kubectl rollout restart deployment infrascore-pgadmin-pgadmin-chart -n infrascore
echo "  - pgAdmin restarted"

# Database
kubectl rollout restart deployment infrascore-db-database-chart -n infrascore
echo "  - Database restarted"

# Ingress Controller
kubectl rollout restart deployment ingress-nginx-controller -n infrascore
echo "  - Ingress Controller restarted"

echo "✅ All rollouts initiated."
