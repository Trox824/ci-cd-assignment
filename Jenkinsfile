pipeline {
    agent any

    tools {
        nodejs 'NodeJS 16' // Ensure this matches the name in Jenkins Global Tool Configuration
    }

    environment {
        VENV_PATH = 'Application/Backend/venv'
        PATH = "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:${env.PATH}"
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
                    // Check if Docker is running
                    sh 'docker info || (echo "Docker is not running. Please start Docker." && exit 1)'
                    
                    // Enable Docker on macOS if not running
                    if (isUnix() && sh(script: 'uname', returnStdout: true).trim() == 'Darwin') {
                        sh '''
                            if ! docker info > /dev/null 2>&1; then
                                echo "Docker is not running. Attempting to start Docker..."
                                open -a Docker
                                # Wait for Docker to start (adjust timeout as needed)
                                timeout=60
                                while ! docker info > /dev/null 2>&1 && [ $timeout -gt 0 ]; do
                                    sleep 1
                                    ((timeout--))
                                done
                                if [ $timeout -eq 0 ]; then
                                    echo "Failed to start Docker. Please start it manually."
                                    exit 1
                                else
                                    echo "Docker started successfully."
                                fi
                            else
                                echo "Docker is already running."
                            fi
                        '''
                    }
                    sh 'docker-compose up -d --build'
                    // Run backend tests
                    sh 'docker-compose run --rm backend pip install -r Backend/requirements.txt'
                    sh 'docker-compose run --rm backend python -m pytest Application/Backend/test_app.py'

                    // Ensure all containers are stopped after tests
                    sh 'docker-compose down'
                }
            }
            //front end tests
        }
        


        // stage('Deploy to Production') {
        //     when {
        //         expression { 
        //             return env.GIT_BRANCH == 'main' || env.GIT_BRANCH == 'master'
        //         }
        //     }
        //     steps {
        //         script {
        //             sshagent(credentials: ['ec2-ssh-key']) {
        //                 // Copy the project to production
        //                 sh "scp -r -o StrictHostKeyChecking=no ./* ${EC2_USER}@${EC2_INSTANCE_IP}:~/app"

        //                 // SSH into production and run docker-compose
        //                 sh """
        //                     ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_INSTANCE_IP} '
        //                         cd ~/app
        //                         docker-compose down
        //                         docker-compose up -d --build
        //                     '
        //                 """
        //             }
        //         }
        //     }
        // }
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
