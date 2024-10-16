pipeline {
    agent any

    environment {
        VENV_PATH = 'Application/Backend/venv'
        PATH = "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:${env.PATH}"
        EC2_USER = 'ec2-user'
        EC2_INSTANCE_DNS = 'ec2-52-200-216-255.compute-1.amazonaws.com'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build and Test') {
                    steps {
                        script {
                            // Start Docker if it's not running (assuming it's already configured to start without sudo)
                            sh 'docker info || (systemctl start docker && systemctl enable docker)'
                            
                            // Stop any running containers and remove them
                            sh 'docker-compose down --remove-orphans'
                            
                            // Build and run containers
                            sh 'docker-compose up -d --build'

                            // Run backend tests
                            sh 'docker-compose run --rm backend pip install -r Backend/requirements.txt'
                            sh 'docker-compose run --rm backend python -m pytest Application/Backend/test_app.py'

                            // Ensure all containers are stopped after tests
                            sh 'docker-compose down'
                        }
                    }
                front end tests
                }
        stage('Debug Info') {
            steps {
                echo "Current branch: ${env.GIT_BRANCH}"
                echo "All environment variables:"
                sh 'env | sort'
            }
        }

        stage('Deploy to Production') {
            when {
                expression { 
                    env.GIT_BRANCH == 'origin/main' || env.GIT_BRANCH == 'origin/master'
                }
            }
            steps {
                echo "Attempting to deploy to production"
                sshagent(credentials: ['ec2-ssh-key']) {
                    sh '''
                        set -xe
                        ssh -o StrictHostKeyChecking=no -v ${EC2_USER}@${EC2_INSTANCE_DNS} << EOF
echo "Successfully connected to EC2 instance"
cd ~/ci-cd-assignment || { echo "Failed to change directory"; exit 1; }
git pull origin main || { echo "Failed to pull latest changes"; exit 1; }
docker-compose down || { echo "Failed to stop existing containers"; exit 1; }
docker-compose up -d --build || { echo "Failed to start new containers"; exit 1; }
EOF
                    '''
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo "Build succeeded!"
        }
        failure {
            echo "Build failed!"
        }
    }
}
