# Bloomreach Exponea API challenge

## Getting started
 ### There are three ways to run the app:
 #### **To run it from the source code:**
* Clone the repository to a local machine
* From *./bloomreach_interview/api* directory 
* execute `pip install -r requirements.txt` 
* run `main.py` or execute `uvicorn main:app`
 #### **To run it with docker:**
* Clone the repository to a local machine
* From *./bloomreach_interview/api* directory
* Execute commands: 
* `docker build -t bloomreach_api .`
* `docker run -p 8000:8000 --name bloomreach_api bloomreach_api`
 #### **To run it with docker compose:**
 This will also start Prometheus and Grafana services
* Clone the repository to a local machine
* Execute command: 
* `docker-compose up`
## Fetching the API
Send an HTTP GET request to endpoint
> http://127.0.0.1:8000/api/smart?timeout=1500

- For accessing OpenApi documentation: `localhost:8000/`
- JSON OpenApi endpoint: `localhost:8000/openapi.json`
- FastAPI metrics endpoint: `localhost:8000/metrics`
- Prometheus endpoint: `localhost:9090`
- Grafana Endpoint: `localhost:3000`

## Configuring
* To configure the server check the **docker-compose.yml** file and set the environmental variables to your liking. If you don't want to use docker compose, you can change the default variables in the config.py directly
* To configure Grafana credentials check **env.example** file and rename it to env. You can also modify dashboard with **dashbords/fastapi-dashboard.json**
* To configure Prometheus check **datasource.yml**

## Additional Information
### Terraform
There is a script for creating ec2 t2.micro server on AWS, and installing all the packages needed to run this app with docker-compose. All the commands for executing this are listed below:

>``terraform init``

> ``terraform validate``

> ``terraform plan``

>``terraform apply``

Responsible file - **init.tf**, and **instructions.sh** for bash initialization script

## Technologies used
* Python 3.10
* FastAPI framework
* Various libraries for python: httpx, asyncio, pytest, prometheus-fastapi-instrumentator, uvicorn
* Prometheus image for monitoring the system
* Grafana for analytics and dashboards
* Terraform for quicker deployment on dev servers in the cloud
* Docker with docker-compose plugin for containerization and deployment
* GitHub as repository host

## Logs
Logs can be checked in the shell where you ran the app, or in api.log file with better formatting.

To set log-level check **LOGLEVEL** variable in **config.py** file.

## Testing
### Check the **report** directory, I hope it's self explanatory.
Testing was done using jMeter with plugins for *Transactions per Second* and *Requests per Second* metrics.

I regret not having more time to add unit and integration testing for the project. I would have added various tests covering smart endpoint and it's behaviour in different circumstances, such as low/high timeout parameter values, simulating low system resources avaliability, etc.

### For proteching the server from being overloaded: Cloudflare or similar DDos mitigation software, and adding horizontal scalability with LoadBalancing.