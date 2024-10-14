pipeline {
    agent any

    tools {
        nodejs 'NodeJS 16' // Replace with the name you provided in Global Tool Configuration
    }

    environment {
        VENV_PATH = 'Application/Backend/venv'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the source code from your repository
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh """
                    python3 -m venv ${VENV_PATH}
                    . ${VENV_PATH}/bin/activate
                    pip install --upgrade pip
                    pip install -r Application/Backend/requirements.txt
                """
            }
        }

        stage('Install Dependencies') {
            steps {
                // Install Python dependencies
                sh """
                    . ${VENV_PATH}/bin/activate
                    pip install -r Application/Backend/requirements.txt
                """

                // Install Node.js dependencies
                dir('Application/Frontend') {
                    sh 'npm install'
                }
            }
        }

        stage('Run Backend Tests') {
            steps {
                sh """
                    . ${VENV_PATH}/bin/activate
                    pytest Application/Backend
                """
            }
        }

        stage('Build Frontend') {
            steps {
                dir('Application/Frontend') {
                    sh 'npm run build'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("your-docker-image-name:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Deploy to Production') {
            steps {
                // Add your deployment steps here
                echo 'Deploying to production...'
            }
        }
    }

    post {
        always {
            // Clean up workspace after build
            cleanWs()
        }
        success {
            // Notify that the build succeeded
            echo "Build succeeded!"
        }
        failure {
            // Send notification on failure (e.g., email or Slack)
            echo "Build failed!"
        }
    }
}
