pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout the source code from your repository
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv Application/Backend/venv
                    . Application/Backend/venv/bin/activate
                    pip install -r Application/Backend/requirements.txt
                '''
            }
        }


        stage('Install Dependencies') {
            steps {
                // Install backend dependencies for FastAPI
                sh 'pip install -r Application/Backend/requirements.txt'
                
                // Install frontend dependencies for React
                dir('Application/Frontend') {
                    sh 'npm install'
                }
            }
        }

        stage('Run Backend Tests') {
            steps {
                // Run any backend tests you have (e.g., using pytest)
                sh 'pytest'
            }
        }

        stage('Build Frontend') {
            steps {
                // Build the React frontend
                dir('Application/Frontend') {
                    sh 'npm run build'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                // Build the Docker image
                sh 'docker build -t myapp:latest .'
            }
        }

        stage('Deploy to Production') {
            steps {
                // Push Docker image to your Docker registry (Docker Hub or any other registry)
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'docker login -u $DOCKER_USER -p $DOCKER_PASS'
                    sh 'docker tag myapp:latest tuanhungnguyen189/myapp:latest'
                    sh 'docker push tuanhungnguyen189/myapp:latest'
                }
                
                // Optionally deploy to your production environment, for example, using Docker Compose or Kubernetes
                // sh 'docker-compose up -d'
            }
        }
    }

    post {
        always {
            // Clean up workspace after build
            cleanWs()
        }
        failure {
            // Send notification on failure (e.g., email or Slack)
            echo "Build failed!"
        }
        success {
            // Notify that the build succeeded
            echo "Build succeeded!"
        }
    }
}
