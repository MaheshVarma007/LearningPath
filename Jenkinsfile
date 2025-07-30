pipeline {
    agent any

    environment {
        // DockerHub credentials (configure these in Jenkins)
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
                sh 'python3 -m pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest -v --maxfail=1 --disable-warnings'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Use short commit SHA as version tag
                    def shortCommit = sh(
                        returnStdout: true,
                        script: "git rev-parse --short HEAD"
                    ).trim()

                    env.IMAGE_TAG = "${DOCKERHUB_USER}/${IMAGE_NAME}:${shortCommit}"
                }

                sh "docker build -t ${IMAGE_TAG} ."
            }
        }

        stage('Push Docker Image') {
            steps {
                sh "echo ${DOCKERHUB_PASS} | docker login -u ${DOCKERHUB_USER} --password-stdin"
                sh "docker push ${IMAGE_TAG}"

                // Also tag 'latest'
                sh "docker tag ${IMAGE_TAG} ${DOCKERHUB_USER}/${IMAGE_NAME}:latest"
                sh "docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:latest"
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
