# elkstackApplicationTest
docker build -t jowettc/shopms ./
docker run -p 5000:5000 

## Project setup
ingress constroller
https://kubernetes.github.io/ingress-nginx/deploy/
`kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.3.0/deploy/static/provider/cloud/deploy.yaml`
`kubectl apply -f .\ingress-service.yaml`

## minikube settings 
`minikube -p minikube docker-env --shell powershell | Invoke-Expression`
`minikube addons enable ingress`
`minikube tunnel`

## virtual enviroment (python venv)
tutorial-env\Scripts\activate.bat