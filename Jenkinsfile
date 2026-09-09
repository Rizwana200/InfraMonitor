pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    python3 -m venv .jenkins-venv
                    . .jenkins-venv/bin/activate
                    pip install -r src/requirements.txt
                    pytest
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    . .jenkins-venv/bin/activate
                    flake8 src/app src/run.py
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build -t inframonitor:jenkins .
                '''
            }
        }
    }
}
