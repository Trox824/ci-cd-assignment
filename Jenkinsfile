pipeline {
    agent any

    tools {
        nodejs 'NodeJS 16' // Ensure this matches the name in Jenkins Global Tool Configuration
    }

    environment {
        VENV_PATH = 'Application/Backend/venv'
        DOCKER_IMAGE = 'tuanhungnguyen189/myapp'
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
                // Verify pytest installation and version
                sh """
                    . ${VENV_PATH}/bin/activate
                    which pytest
                    pytest --version
                """
                // Install httpx for testing
                sh """
                    . ${VENV_PATH}/bin/activate
                    pip install httpx
                """
                // Run pytest in verbose mode
                sh """
                    . ${VENV_PATH}/bin/activate
                    cd Application/Backend
                    pytest test_app.py -v
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${env.BUILD_NUMBER}", "-f Dockerfile .")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-credentials') {
                        docker.image("${DOCKER_IMAGE}:${env.BUILD_NUMBER}").push()
                        docker.image("${DOCKER_IMAGE}:${env.BUILD_NUMBER}").push('latest')
                    }
                }
            }
        }

        stage('Deploy to Production') {
            steps {
                // Add your deployment steps here
                echo 'Deploying to production...'
                // Example: Update your deployment with the new image
                // sh "kubectl set image deployment/myapp myapp=${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
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
