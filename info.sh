kubectl get pods
POD_NAME=$(kubectl get pods --selector=app=multi-service-app --output=jsonpath='{.items[0].metadata.name}')
kubectl logs $POD_NAME
kubectl exec -it $POD_NAME -- ls
kubectl exec -it $POD_NAME -- cat app.log