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
                    docker.build registry + ":$BUILD_NUMBER"
                }
            }
        }
    }
}
