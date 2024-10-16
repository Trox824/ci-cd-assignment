pipeline {
    agent any

    environment {
        VENV_PATH = 'Application/Backend/venv'
        PATH = "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:${env.PATH}"
        EC2_USER = 'ec2-user'
        EC2_INSTANCE_DNS = 'ec2-52-200-216-255.compute-1.amazonaws.com'
        AWS_DEFAULT_REGION = 'us-east-1'
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
                
                }
        stage('Debug Info') {
            steps {
                echo "Current branch: ${env.GIT_BRANCH}"
                echo "All environment variables:"
                sh 'env | sort'
            }
        }

//         stage('Deploy to Production') {
//             when {
//                 expression { 
//                     env.GIT_BRANCH == 'origin/main' || env.GIT_BRANCH == 'origin/master'
//                 }
//             }
//             steps {
//                 echo "Attempting to deploy to production"
//                 sshagent(credentials: ['ec2-ssh-key']) {
//                     sh '''
//                         set -xe
//                         ssh -o StrictHostKeyChecking=no -v ${EC2_USER}@${EC2_INSTANCE_DNS} << EOF
// echo "Successfully connected to EC2 instance"
// cd ~/ci-cd-assignment || { echo "Failed to change directory"; exit 1; }
// git pull origin main || { echo "Failed to pull latest changes"; exit 1; }
// docker-compose down || { echo "Failed to stop existing containers"; exit 1; }
// docker-compose up -d --build || { echo "Failed to start new containers"; exit 1; }
// EOF
//                     '''
//                 }
//             }
//         }
            stage('Deploy to Production') {
                when {
                    expression { 
                        env.GIT_BRANCH == 'origin/main' || env.GIT_BRANCH == 'origin/master'
                    }
                }
                steps {
                    echo "Attempting to deploy to production"
                    script {
                        try {
                            echo "Fetching instance IDs..."
                            def instanceIds = sh(
                                script: "aws ec2 describe-instances --filters 'Name=tag:Name,Values=auto-scaling-instance' 'Name=instance-state-name,Values=running' --query 'Reservations[*].Instances[*].InstanceId' --output text",
                                returnStdout: true
                            ).trim().split()
                            
                            echo "Found ${instanceIds.size()} instances: ${instanceIds.join(', ')}"
                            
                            instanceIds.each { instanceId ->
                                echo "Processing instance: ${instanceId}"
                                sshagent(credentials: ['ec2-ssh-key']) {
                                    echo "Fetching IP address for instance ${instanceId}..."
                                    def instanceIp = sh(
                                        script: "aws ec2 describe-instances --instance-ids ${instanceId} --query 'Reservations[*].Instances[*].PublicIpAddress' --output text",
                                        returnStdout: true
                                    ).trim()
                                    
                                    echo "Instance ${instanceId} IP: ${instanceIp}"
                                    
                                    echo "Deploying to instance ${instanceId} (${instanceIp})..."
                                    def deploymentResult = sh(
                                        script: """
                                            ssh -o StrictHostKeyChecking=no -v ec2-user@${instanceIp} << 'ENDSSH'
                                                set -xe
                                                echo "Connected to instance ${instanceId}"
                                                cd ~/ci-cd-assignment || { echo "Failed to change directory"; exit 1; }
                                                echo "Setting correct permissions..."
                                                sudo chown -R ec2-user:ec2-user /home/ec2-user/ci-cd-assignment
                                                sudo chmod -R 755 /home/ec2-user/ci-cd-assignment
                                                sudo chmod -R 775 /home/ec2-user/ci-cd-assignment/.git
                                                echo "Adding safe directory..."
                                                git config --global --add safe.directory /home/ec2-user/ci-cd-assignment
                                                echo "Handling local changes..."
                                                git reset --hard HEAD
                                                echo "Pulling latest changes..."
                                                git pull origin main || { echo "Failed to pull latest changes"; exit 1; }
                                                echo "Stopping existing containers..."
                                                docker-compose down || { echo "Failed to stop containers"; exit 1; }
                                                echo "Building and starting new containers..."
                                                docker-compose up -d --build || { echo "Failed to start new containers"; exit 1; }
                                                echo "Cleaning up Docker system..."
                                                docker system prune -af || { echo "Failed to clean up Docker system"; exit 1; }
                                                echo "Deployment to instance ${instanceId} completed successfully"
                                            ENDSSH
                                        """,
                                        returnStatus: true
                                    )
                                    
                                    if (deploymentResult == 0) {
                                        echo "Deployment to instance ${instanceId} (${instanceIp}) successful"
                                    } else {
                                        error "Deployment to instance ${instanceId} (${instanceIp}) failed"
                                    }
                                }
                            }
                            echo "All deployments completed successfully"
                        } catch (Exception e) {
                            error "Deployment failed: ${e.getMessage()}"
                        }
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
