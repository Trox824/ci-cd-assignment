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

        // stage('Build and Test') {
        //     steps {
        //         script {
        //             // Start Docker if it's not running (assuming it's already configured to start without sudo)
        //             sh 'docker info || (systemctl start docker && systemctl enable docker)'

        //             // Build and run containers
        //             sh 'docker-compose up -d --build'

        //             // Run backend tests
        //             sh 'docker-compose run --rm backend pip install -r Backend/requirements.txt'
        //             sh 'docker-compose run --rm backend python -m pytest Application/Backend/test_app.py'

        //             // Ensure all containers are stopped after tests
        //             sh 'docker-compose down'
        //         }
        //     }
        //     //front end tests
        // }
        


        stage('Deploy to Production') {
            when {
                expression { 
                    return env.GIT_BRANCH == 'main' || env.GIT_BRANCH == 'master'
                }
            }
            steps {
                script {
                    sshagent(credentials: ['ec2-ssh-key']) {
                        // Copy the project to production
                        sh "scp -r -o StrictHostKeyChecking=no ./* ${EC2_USER}@${EC2_INSTANCE_IP}:~/app"

                        // SSH into production and run docker-compose
                        sh """
                            ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_INSTANCE_IP} '
                                cd ~/ci-cd-assignment
                                docker-compose down
                                docker-compose up -d --build
                            '
                        """
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
