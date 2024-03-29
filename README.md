# elkstackApplicationTest
docker build -t flask-api-jowett .
docker build -t frontend-jowett .

## ingress stuff
- ingress constroller
- https://kubernetes.github.io/ingress-nginx/deploy/
- `kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.3.0/deploy/static/provider/cloud/deploy.yaml`
- `kubectl apply -f .\ingress-service.yaml`

## minikube settings 
- `minikube -p minikube docker-env --shell powershell | Invoke-Expression`
- `minikube addons enable ingress`
- `minikube tunnel`

## virtual enviroment (python venv)
tutorial-env\Scripts\activate.bat


## other instructions 
# Deploying a Flask API and MySQL server on Kubernetes

This repo contains code that 
1) Deploys a MySQL server on a Kubernetes cluster
2) Attaches a persistent volume to it, so the data remains contained if pods are restarting
3) Deploys a Flask API to add, delete and modify users in the MySQL database

## Prerequisites
1. Have `Docker` and the `Kubernetes CLI` (`kubectl`) installed together with `Minikube` (https://kubernetes.io/docs/tasks/tools/)

## Getting started
1. Clone the repository
2. Configure `Docker` to use the `Docker daemon` in your kubernetes cluster via your terminal: `eval $(minikube docker-env)`
3. Pull the latest mysql image from `Dockerhub`: `Docker pull mysql`
4. Build a kubernetes-api image with the Dockerfile in this repo: `docker build -t jowettc/flask-api-jowett .`

## Secrets
`Kubernetes Secrets` can store and manage sensitive information. For this example we will define a password for the
`root` user of the `MySQL` server using the `Opaque` secret type. For more info: https://kubernetes.io/docs/concepts/configuration/secret/

1. Encode your password in your terminal: `echo -n super-secret-passwod | base64`
2. Add the output to the `secrets.yml` file at the `db_root_password` field

## Deployments
Get the secrets, persistent volume in place and apply the deployments for the `MySQL` database and `Flask API`

1. Add the secrets to your `kubernetes cluster`: `kubectl apply -f secrets.yml`
2. Create the `persistent volume` and `persistent volume claim` for the database: `kubectl apply -f mysql-pv.yml`
3. Create the `MySQL` deployment: `kubectl apply -f mysql-deployment.yml`
4. Create the `Flask API` deployment: `kubectl apply -f flaskapp-deployment.yml`

You can check the status of the pods, services and deployments.

## Creating database and schema
The API can only be used if the proper database and schemas are set. This can be done via the terminal.
1. Connect to your `MySQL database` by setting up a temporary pod as a `mysql-client`: 
   `kubectl run -it --rm --image=mysql --restart=Never mysql-client -- mysql --host mysql --password=<super-secret-password>`
   make sure to enter the (decoded) password specified in the `secrets.yml`
2. Create the database and table
   1. `CREATE DATABASE mydb_shop;`
    2. `USE mydb_shop;`
    3. `CREATE TABLE shop(shop_id INT PRIMARY KEY AUTO_INCREMENT, shop_name VARCHAR(255), location VARCHAR(255));`
    
## Expose the API
The API can be accessed by exposing it using minikube: `minikube service flask-service-jowett`. This will return a `URL`. If you paste this to your browser you will see the `hello world` message. You can use this `service_URL` to make requests to the `API`

## Start making requests
Now you can use the `API` to `CRUD` your database
1. add a user: `curl -H "Content-Type: application/json" -d '{"name": "<user_name>", "email": "<user_email>", "pwd": "<user_password>"}' <service_URL>/create`
2. get all users: `curl <service_URL>/users`
3. get information of a specific user: `curl <service_URL>/user/<user_id>`
4. delete a user by user_id: `curl -H "Content-Type: application/json" <service_URL>/delete/<user_id>`
5. update a user's information: `curl -H "Content-Type: application/json" -d {"name": "<user_name>", "email": "<user_email>", "pwd": "<user_password>", "user_id": <user_id>} <service_URL>/update`


## ELK stack

### installation
- `helm install elasticsearch elastic/elasticsearch  -f values.yaml --namespace=elk  --create-namespace --wait`
- `helm install kibana elastic/kibana --namespace=elk --wait`
- `helm install filebeat elastic/filebeat --namespace=elk --wait`

### port forwarding
- kibana runs on 5601 port `kubectl port-forward deployment/kibana-kibana 5601 --namespace=elk`
- elk runs on 9200 port `kubectl port-forward service/elasticsearch-master 9200  --namespace=elk`

## set config of kubernetes
- `$Env:KUBECONFIG=("C:\Users\PM\OneDrive\Documents\GitHub\elkstackApplicationTest\kubeconfig-jowett-tkg.yml")`

### password for elastic search 
- `hb53toMlm1g9x135HQ8uOX22`
- `curl -u "elastic:hb53toMlm1g9x135HQ8uOX22" -k "https://localhost:9200"`
- `rm alias:curl`
- `hb53toMlm1g9x135HQ8uOX22`
`jowett.cnasg.net`