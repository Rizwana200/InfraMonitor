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
                    docker build -t arizwana/inframonitor:jenkins .
                '''
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_TOKEN'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_TOKEN" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push arizwana/inframonitor:jenkins
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    helm upgrade --install inframonitor ./helm \
                    --set image.repository=arizwana/inframonitor \
                    --set image.tag=jenkins

                    kubectl rollout status deployment/inframonitor
                '''
            }
        }
    }
}
