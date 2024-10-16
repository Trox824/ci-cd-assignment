pipeline {
    agent any

    tools {
        nodejs 'NodeJS 16' // Ensure this matches the name in Jenkins Global Tool Configuration
    }

    environment {
        VENV_PATH = 'Application/Backend/venv'
        // Remove EC2 related variables as they're not needed for local deployment
        // TEST_ENV_IP and TEST_ENV_USER are also not needed
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Test') {
            steps {
                // Enable Docker
                sh 'systemctl start docker || true'  // Use '|| true' to prevent failure if Docker is already running
                sh 'systemctl enable docker || true'
                sh 'docker-compose build'
                sh 'docker-compose run --rm backend python -m pytest Application/Backend/test_app.py'
            }
        }

        stage('Deploy to Test Environment') {
            steps {
                script {
                    // Stop any existing containers
                    sh 'docker-compose down'

                    // Build and start the containers
                    sh 'docker-compose up -d --build'

                    // Wait for services to start (adjust time as needed)
                    sh 'sleep 30'

                    // Run integration tests or smoke tests
                    sh '''
                        # Add your integration test commands here
                        # For example:
                        # docker-compose exec app pytest integration_tests/
                    '''
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
