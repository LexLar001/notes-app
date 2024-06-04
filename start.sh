kubectl apply -f postgres-pv.yaml
kubectl apply -f postgres-pvc.yaml

kubectl apply -f postgres-deployment.yaml
kubectl apply -f postgres-service.yaml

echo "Waiting for PostgreSQL pod to be in running state..."
while [[ $(kubectl get pods --selector=app=postgres --output=jsonpath='{.items[0].status.phase}') != "Running" ]]; do
  sleep 5
  echo "Waiting for PostgreSQL pod to be in running state..."
done

kubectl apply -f app-deployment.yaml
kubectl apply -f app-service.yaml

echo "Waiting for application pod to be in running state..."
while [[ $(kubectl get pods --selector=app=multi-service-app --output=jsonpath='{.items[0].status.phase}') != "Running" ]]; do
  sleep 5
  echo "Waiting for application pod to be in running state..."
done

POD_NAME=$(kubectl get pods --selector=app=multi-service-app --output=jsonpath='{.items[0].metadata.name}')

if [ -z "$POD_NAME" ]; then
  echo "No pod found for multi-service-app. Exiting."
  exit 1
fi

echo "Using pod: $POD_NAME"

kubectl port-forward deployment/multi-service-app 5000:5000 &
PORT_FORWARD_PID=$!
