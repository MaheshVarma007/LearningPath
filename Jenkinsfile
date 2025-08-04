pipeline {
    agent any

    environment {
        // Use a Jenkins usernamePassword credential with ID 'dockerhub'
        DOCKERHUB_USER = credentials('dockerhub', variable: 'USERNAME')
        DOCKERHUB_PASS = credentials('dockerhub', variable: 'PASSWORD')
        IMAGE_NAME = 's3_cli_app'
    }
    // Optional: Add a pre-check stage to verify tool versions and workspace
    stages {
        stage('Pre-check') {
            steps {
                echo "========== [STAGE: Pre-check] =========="
                sh 'python3 --version || true'
                sh 'pip --version || true'
                sh 'docker --version || true'
                sh 'ls -l aws/Projects/S3_CLI || true'
                echo "========================================"
            }
        }

    stages {
        stage('Checkout') {
            steps {
                echo "========== [STAGE: Checkout] =========="
                echo "[STEP] Starting: Checkout SCM"
                checkout scm
                echo "[STEP] Completed: Checkout SCM"
                echo "========================================"
            }
        }

        stage('Install dependencies') {
            steps {
                echo "========== [STAGE: Install dependencies] =========="
                dir('aws/Projects/S3_CLI') {
                    echo "[STEP] Starting: Upgrade pip"
                    sh 'python3 -m pip install --upgrade pip'
                    echo "[STEP] Completed: Upgrade pip"
                    echo "[STEP] Starting: Install requirements"
                    sh 'pip install -r requirements.txt'
                    echo "[STEP] Completed: Install requirements"
                }
                echo "========================================"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "========== [STAGE: Build Docker Image] =========="
                dir('aws/Projects/S3_CLI') {
                    echo "[STEP] Starting: Get short commit hash"
                    script {
                        def shortCommit = sh(
                            returnStdout: true,
                            script: "git rev-parse --short HEAD"
                        ).trim()
                        env.IMAGE_TAG = "${DOCKERHUB_USER}/${IMAGE_NAME}:${shortCommit}"
                    }
                    echo "[STEP] Completed: Get short commit hash"
                    echo "[STEP] Starting: Build Docker image"
                    sh 'docker build -t ${IMAGE_TAG} .'
                    echo "[STEP] Completed: Build Docker image"
                }
                echo "========================================"
            }
        }

        stage('Push Docker Image') {
            steps {
                echo "========== [STAGE: Push Docker Image] =========="
                dir('aws/Projects/S3_CLI') {
                    echo "[STEP] Starting: Docker login"
                    sh 'echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin'
                    echo "[STEP] Completed: Docker login"
                    echo "[STEP] Starting: Push Docker image with commit tag"
                    sh 'docker push ${IMAGE_TAG}'
                    echo "[STEP] Completed: Push Docker image with commit tag"
                    echo "[STEP] Starting: Tag Docker image as latest"
                    sh 'docker tag ${IMAGE_TAG} ${DOCKERHUB_USER}/${IMAGE_NAME}:latest'
                    echo "[STEP] Completed: Tag Docker image as latest"
                    echo "[STEP] Starting: Push Docker image as latest"
                    sh 'docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:latest'
                    echo "[STEP] Completed: Push Docker image as latest"
                }
                echo "========================================"
            }
        }
    }

    post {
        success {
            echo "========== [POST] Pipeline completed successfully. Docker image: ${IMAGE_TAG} =========="
        }
        failure {
            echo "========== [POST] Pipeline failed. Check logs for details. =========="
        }
    }
}