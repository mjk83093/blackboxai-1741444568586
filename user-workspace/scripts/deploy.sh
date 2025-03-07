#!/bin/bash

# Exit on error
set -e

# Configuration
APP_NAME="work-production-ai"
ECR_REPO="your-aws-account.dkr.ecr.region.amazonaws.com"
CLUSTER_NAME="work-production-cluster"
K8S_NAMESPACE="work-production"

# Check required tools
echo "🔍 Checking required tools..."
command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed. Aborting." >&2; exit 1; }
command -v kubectl >/dev/null 2>&1 || { echo "❌ kubectl is required but not installed. Aborting." >&2; exit 1; }
command -v aws >/dev/null 2>&1 || { echo "❌ AWS CLI is required but not installed. Aborting." >&2; exit 1; }

# Load environment variables
if [ -f .env ]; then
    echo "📥 Loading environment variables..."
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "❌ .env file not found"
    exit 1
fi

# Build Docker image
echo "🏗️ Building Docker image..."
docker build -t ${APP_NAME}:latest .

# Login to AWS ECR
echo "🔐 Logging in to AWS ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO}

# Tag and push image
echo "📤 Pushing image to ECR..."
docker tag ${APP_NAME}:latest ${ECR_REPO}/${APP_NAME}:latest
docker tag ${APP_NAME}:latest ${ECR_REPO}/${APP_NAME}:$(date +%Y%m%d_%H%M%S)
docker push ${ECR_REPO}/${APP_NAME}:latest
docker push ${ECR_REPO}/${APP_NAME}:$(date +%Y%m%d_%H%M%S)

# Update Kubernetes configs
echo "📝 Updating Kubernetes configurations..."

# Create namespace if it doesn't exist
kubectl get namespace ${K8S_NAMESPACE} || kubectl create namespace ${K8S_NAMESPACE}

# Update ConfigMap with environment variables
echo "🔄 Updating ConfigMap..."
kubectl create configmap ${APP_NAME}-config \
    --from-env-file=.env \
    --namespace=${K8S_NAMESPACE} \
    -o yaml --dry-run=client | kubectl apply -f -

# Apply Kubernetes configurations
echo "🚀 Applying Kubernetes configurations..."
kubectl apply -f deployment/kubernetes.yml --namespace=${K8S_NAMESPACE}

# Wait for deployment to complete
echo "⏳ Waiting for deployment to complete..."
kubectl rollout status deployment/api --namespace=${K8S_NAMESPACE}

# Check deployment status
if [ $? -eq 0 ]; then
    echo """
    ✅ Deployment completed successfully!
    
    To monitor the deployment:
    - View pods: kubectl get pods -n ${K8S_NAMESPACE}
    - View logs: kubectl logs -f deployment/api -n ${K8S_NAMESPACE}
    - View services: kubectl get svc -n ${K8S_NAMESPACE}
    
    Application should be accessible at:
    $(kubectl get svc api -n ${K8S_NAMESPACE} -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
    """
else
    echo "❌ Deployment failed"
    exit 1
fi

# Monitor deployment health
echo "🏥 Monitoring deployment health..."
kubectl get pods -n ${K8S_NAMESPACE}
kubectl top pods -n ${K8S_NAMESPACE}

# Setup monitoring
echo "📊 Setting up monitoring..."
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/main/bundle.yaml

# Create service account for monitoring
kubectl create serviceaccount monitoring -n ${K8S_NAMESPACE}
kubectl create clusterrolebinding monitoring --clusterrole=cluster-admin --serviceaccount=${K8S_NAMESPACE}:monitoring

# Get monitoring dashboard token
echo """
🔑 Monitoring dashboard token:
$(kubectl -n ${K8S_NAMESPACE} create token monitoring)

Access the Kubernetes dashboard at:
http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
"""

# Make the script executable
chmod +x scripts/deploy.sh
