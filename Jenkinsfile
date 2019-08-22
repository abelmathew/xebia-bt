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
                    if (Integer.valueOf(env.BUILD_ID) % 3 != 0) {
                        error("Build failed.")
                    }
                }
            }
        }
        stage('Create docker image..') {
            steps {
                echo 'Building..'
                script {
                    docker.withServer('tcp://ip-172-31-42-192.ec2.internal:2375') {
                        dockerImage = docker.build registry + ":$BUILD_NUMBER"
                    }
                }
            }
        }
        stage('Publish docker image..') {
            steps {
               script {
                   docker.withServer('tcp://ip-172-31-42-192.ec2.internal:2375') {
                       docker.withRegistry('', registryCredential ) {
                           dockerImage.push()
                       }
                   }
                }
            }
        }
        stage ('Register deployment metadata') {
            steps {
                sh "./xlw apply -v --values=PACKAGE_NAME=Applications/BacktraceApp/$BUILD_NUMBER --values=IMAGE=vlussenburg/backtrace-webapp:$BUILD_NUMBER --values=APPLICATION_VERSION=$BUILD_NUMBER -f xebialabs.yaml"
            }
        }
        
        stage ('Kick off release') {
            steps {
                xlrCreateRelease releaseTitle: 'Release for $BUILD_TAG', serverCredentials: 'xlr', startRelease: true, template: 'Samples & Tutorials/Sample Release Template with XL Deploy', variables: [[propertyName: 'packageId', propertyValue: 'Applications/BacktraceApp/$BUILD_NUMBER'], [propertyName: 'application', propertyValue: 'BacktraceApp'], [propertyName: 'packageVersion', propertyValue: '$BUILD_NUMBER'], [propertyName: 'ACC environment', propertyValue: 'Environments/dev'], [propertyName: 'QA environment', propertyValue: 'Environments/dev']]
            }
        }
    }
}
