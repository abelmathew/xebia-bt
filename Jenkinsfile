pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                script {
                    if (Integer.valueOf(env.BUILD_ID) % 3 != 0) {
                        error("Build failed.")
                    }
                }
            }
        }
    }
}
