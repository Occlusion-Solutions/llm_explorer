SHELL=/bin/bash
devops_state = main
working_dir = `pwd`
datadog_api_key = ""

install: install_python_dependencies

local_build_and_deploy: 
	pip uninstall llm_explorer -y \
	&& python setup.py install \
	&& llm_explorer

package_build:
	python -m build

package_list:
	unzip -l dist/*.whl  

set_env:
	source /astro/$(devops_state).env

setup_docker:
	sudo apt-get install ca-certificates curl gnupg lsb-release make \
	&& curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg \
	&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null \
	&& sudo apt-get update \
	&& sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose \

setup_superset:
	sudo apt-get install build-essential libssl-dev libffi-dev python3-dev python3-pip libsasl2-dev libldap2-dev default-libmysqlclient-dev -y \
	&& pip install apache-superset \
	&& superset db upgrade \
	&& export FLASK_APP=superset \
	&& superset fab create-admin \
	&& superset load_examples \
	&& superset init \
	&& superset run -p 8088 --with-threads --reload --debugger

setup_jupyter:
	sudo apt-get update && sudo apt-get install python3-pip python3-dev \
	&& sudo -H pip3 install --upgrade pip && sudo -H pip3 install virtualenv \
	&& cd environments && mkdir jupyter_server && cd jupyter_server \
	&& virtualenv jupyter_server_env && source jupyter_server_env/bin/activate \
	&& pip install jupyter

jupyter_service:
	source environments/jupyter_server/jupyter_server_env/bin/activate \
	&& nohup jupyter-notebook --no-browser --port=8888 &> /environments/jupyter_server/server_logs/jupyter_server.out & \
	
vscode_service:
	curl -fsSL https://code-server.dev/install.sh | sh \
	&& sudo nohup code-server --auth=none --bind-addr=127.0.0.1:8090 &> /environments/jupyter_server/server_logs/vscode_server.out &

datadog_setup:
	DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=${datadog_api_key} DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"

setup_kind:
	curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.14.0/kind-linux-amd64 \
	&& chmod +x ./kind \
	&& sudo mv ./kind /usr/local/bin/kind

setup_miniconda:
	curl -Lo ./miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
	&& chmod +x ./miniconda.sh \

miniconda_create_llm_explorer:
	conda create  --yes -n llm_explorer python=3.10 \
	&& conda init bash

miniconda_create_adb_connect:
	conda create --name adb_connect python=3.8 \
	&& conda activate adb_connect

miniconda_configure_adb_connect:
	pip uninstall pyspark \
	&& pip install -U databricks-connect \


install_python_dependencies:
	pip install -r ./requirements.txt

setup_java:
	sudo apt-get install openjdk-8-jdk

java_correct_jdk:
	sudo update-alternatives --config java

setup_kubectl:
	curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
	&& sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

setup_airflow:
	curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.3.3/docker-compose.yaml'

airflow_start:
	cd airflow \
	&& sudo docker-compose up airflow-init -d \
	&& sudo docker-compose up -d

airflow_kill:
	cd /airflow \
	&& sudo docker compose down --volumes --rmi all   

docker_exec_root:
	docker exec -u root -it airflow-airflow-scheduler-1 bash

setup_helm:
	curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 \
	&& chmod 700 get_helm.sh \
	&& ./get_helm.sh

helm_repos:
	helm repo add datadog https://helm.datadoghq.com \
	&& helm repo add stable https://charts.helm.sh/stable \
	&& helm repo add airflow-stable https://airflow-helm.github.io/charts \
	&& helm repo update

setup_kompose:
	curl -L https://github.com/kubernetes/kompose/releases/download/v1.26.0/kompose-linux-amd64 -o kompose \
	&& chmod +x kompose \
	&& sudo mv ./kompose /usr/local/bin/kompose

kompose_convert:
	cd visualization \
	&& kompose convert