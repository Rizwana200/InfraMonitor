pipeline {
    agent any
    environment {
        IMAGE_NAME = "arizwana/inframonitor"
        IMAGE_TAG = "${GIT_COMMIT}"
    }

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
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
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
                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                        docker logout
                    '''
                }
            }
        }

        stage('Update Helm Image') {
            steps {
                withCredentials([
                    gitUsernamePassword(
                        credentialsId: 'github-credentials',
                        gitToolName: 'Default'
                    )
                ]) {
                    sh '''
                        sed -i "s/^  tag: .*/  tag: ${IMAGE_TAG}/" helm/values.yaml

                        git config user.name "Jenkins"
                        git config user.email "jenkins@localhost"

                        git add helm/values.yaml
                        git commit -m "Update InfraMonitor image to ${IMAGE_TAG} [skip ci]" || true

                        git push origin HEAD:main
                    '''
                }
            }
        }
    }
}
