pipeline {
    agent any

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
                    // Check if Docker is running
                    
                    // Wait for Docker to start if it wasn't running
                    sh 'sudo systemctl start docker'
                    sh 'sudo systemctl enable docker'

                    // Build and run containers
                    sh 'sudo docker-compose up -d --build'

                    // Run backend tests
                    sh 'sudo docker-compose run --rm backend pip install -r Backend/requirements.txt'
                    sh 'sudo docker-compose run --rm backend python -m pytest Application/Backend/test_app.py'

                    // Ensure all containers are stopped after tests
                    sh 'sudo docker-compose down'
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
            node {
                cleanWs()
            }
        }
        success {
            echo "Build succeeded!"
        }
        failure {
            echo "Build failed!"
        }
    }
}
