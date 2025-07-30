pipeline {
    agent any

    environment {
        DOCKERHUB_USER = credentials('maheshvarma007')
        DOCKERHUB_PASS = credentials('Manju@123')
        IMAGE_NAME = 's3_cli_app'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                dir('aws/Projects/S3_CLI') {
                    sh 'python3 -m pip install --upgrade pip'
                    sh 'pip install -r requirements.txt'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('aws/Projects/S3_CLI') {
                    script {
                        def shortCommit = sh(
                            returnStdout: true,
                            script: "git rev-parse --short HEAD"
                        ).trim()
                        env.IMAGE_TAG = "${DOCKERHUB_USER}/${IMAGE_NAME}:${shortCommit}"
                    }
                    sh 'docker build -t ${IMAGE_TAG} .'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                dir('aws/Projects/S3_CLI') {
                    sh 'echo ${DOCKERHUB_PASS} | docker login -u ${DOCKERHUB_USER} --password-stdin'
                    sh 'docker push ${IMAGE_TAG}'
                    sh 'docker tag ${IMAGE_TAG} ${DOCKERHUB_USER}/${IMAGE_NAME}:latest'
                    sh 'docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:latest'
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully. Docker image: ${IMAGE_TAG}"
        }
        failure {
            echo "Pipeline failed. Check logs for details."
        }
    }
}