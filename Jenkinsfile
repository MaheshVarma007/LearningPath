pipeline {
  agent any

  options {
    timestamps()
    ansiColor('xterm')
  }

  environment {
    // Optional: set your default AWS region for terraform
    AWS_DEFAULT_REGION = 'us-east-1'

    // If you store AWS creds in Jenkins, uncomment and set IDs:
    // AWS_ACCESS_KEY_ID     = credentials('aws-access-key-id')
    // AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')

    BUILDER_IMAGE = 'lambda-zip-builder:latest'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Sanity & Tools') {
      steps {
        sh '''
          echo "Jenkins workspace: $(pwd)"
          docker version >/dev/null 2>&1 || { echo "Docker not available"; exit 1; }
          terraform -version || { echo "Terraform not available"; exit 1; }
        '''
      }
    }

    stage('(Optional) Unit Tests') {
      when { expression { return fileExists('requirements-test.txt') || fileExists('pytest.ini') || fileExists('tests') } }
      steps {
        sh '''
          python3 -m pip install --upgrade pip
          # install whatever you use for tests; customize as needed
          if [ -f requirements-test.txt ]; then pip install -r requirements-test.txt; fi
          # Example (uncomment if you have tests):
          # pip install pytest moto
          # pytest -q
          echo "Skipping actual tests placeholder. Add pytest here."
        '''
      }
    }

    stage('Build builder image') {
      steps {
        sh 'docker build -f Dockerfile.build -t ${BUILDER_IMAGE} .'
      }
    }

    stage('Package Lambdas (ZIP)') {
      steps {
        sh 'docker run --rm -v "$PWD":/workspace ${BUILDER_IMAGE}'
      }
    }

    stage('Archive Artifacts') {
      steps {
        sh 'ls -lh build || true'
        archiveArtifacts artifacts: 'build/*.zip', fingerprint: true, onlyIfSuccessful: true
      }
    }

    stage('Terraform Init/Plan') {
      steps {
        dir('infra') {
          sh '''
            terraform init -input=false
            terraform plan -out=tfplan -input=false
          '''
        }
      }
    }

    stage('Terraform Apply') {
      steps {
        input message: 'Apply Terraform changes?', ok: 'Apply'
        dir('infra') {
          sh 'terraform apply -input=false -auto-approve tfplan'
        }
      }
    }
  }

  post {
    success {
      echo '✅ CI/CD finished successfully. Lambdas packaged and infra applied.'
    }
    failure {
      echo '❌ Pipeline failed. Check the stage logs above.'
    }
    always {
      cleanWs()
    }
  }
}
