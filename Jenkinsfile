pipeline {
    agent any

    stages {
        stage('Pre-build') {
            steps {
                echo 'Pip install'
                sh  '''
                    #!/bin/bash
                    echo "instal start"
                    whoami
                    python3.7 -m pip install --user virtualenv

                    python3.7 -m virtualenv venv
                    source venv/bin/activate

                    pip install --upgrade pip
                    pip install aws-sam-cli
                    pip install pandas
                    pip install sklearn
                    pip install mlflow
                    pip install bentoml
                    pip install pickle5

                    '''
            }
        }
        stage('Build') {
            steps {
                echo 'Download and pack model'
                sh  '''
                    #!/bin/bash

                    source venv/bin/activate

                    if [[ -d "./pack_and_deploy" ]]
                    then
                        echo "Repo pack_and_push is already cloned" 
                        rm -rf pack_and_deploy
                        git clone https://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@github.com/michaelhDS/pack_and_deploy.git

                    else
                        echo "Clone Repo pack_and_deploy"
                        git clone https://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@github.com/michaelhDS/pack_and_deploy.git

                    fi

                    cd pack_and_deploy
                    bash script.sh
                    cd bentoml

                    token=$(jq .databricks_token config.json -r)
                    host=$(jq .databricks_host config.json -r)

                    export MLFLOW_TRACKING_URI=databricks
                    export DATABRICKS_TOKEN=$token
                    export DATABRICKS_HOST=$host

                    python download_model.py
                    python pack_and_save.py
                    '''
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
                sh  '''
                    #!/bin/bash
                    source venv/bin/activate

                    pwd
                    echo | python -V
                    cd pack_and_deploy/aws-lambda-deploy
                    pip install --upgrade pip
                    pip install -r requirements.txt

                    BENTO_BUNDLE_PATH=$(python3.7 -m bentoml get Master:latest --print-location -q)

                    aws_access_key=$(jq .aws_access_key ../bentoml/config.json -r)
                    aws_secret_access_key=$(jq .aws_secret_access_key ../bentoml/config.json -r)
                    aws_default_region=$(jq .aws_default_region ../bentoml/config.json -r)

                    export AWS_ACCESS_KEY_ID=$aws_access_key
                    export AWS_SECRET_ACCESS_KEY=$aws_secret_access_key
                    export AWS_DEFAULT_REGION=$aws_default_region

                    python3.7 -m bentoml list
                    python3.7 -m bentoml containerize Master:latest

                    stack_name=$(jq .aws_stack_name ../bentoml/config.json -r)


                    python3.7 -m deploy $BENTO_BUNDLE_PATH $stack_name lambda_config.json
                    python describe.py $stack_name
                    '''
            }
        }
    }
}