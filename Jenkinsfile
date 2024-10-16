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

        stage('Build, Test, and Deploy to Test Environment') {
            steps {
                script {
                    // Check if Docker is running
                    sh 'docker info || (echo "Docker is not running. Please start Docker." && exit 1)'
                    
                    // Stop any existing containers and remove them
                    sh 'docker-compose down --remove-orphans'
                    
                    // Kill any process using port 3000 (use with caution)
                    sh 'lsof -ti:3000 | xargs kill -9 || true'
                    
                    // Wait a moment for the port to be released
                    sh 'sleep 5'

                    // Build images and start containers
                    sh 'docker-compose up -d --build'

                    // Wait for services to start (adjust time as needed)
                    sh 'sleep 30'

                    // Run backend tests
                    sh 'docker-compose exec -T backend pip install -r Backend/requirements.txt'
                    sh 'docker-compose exec -T backend python -m pytest Application/Backend/test_app.py'

                    // Run integration tests or smoke tests
                    sh '''
                        docker-compose exec -T backend pytest Application/Backend/test_app.py
                    '''

                    // Stop containers after tests
                    sh 'docker-compose down --remove-orphans'
                }
            }
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
