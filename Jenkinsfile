pipeline {
    agent any
    
  environment {
    registry = "vlussenburg/backtrace-webapp"
    registryCredential = 'docker-login'
  }

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                script {
                    docker.withServer('tcp://ip-172-31-42-192.ec2.internal:2375') {
                        docker.build registry + ":$BUILD_NUMBER"
                    }
                }
            }
        }
    }
}
