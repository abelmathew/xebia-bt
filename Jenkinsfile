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
                        dockerImage = docker.build registry + ":$BUILD_NUMBER"
                    }
                }
            }
        }
        stage('Publish') {
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
        stage ('XL Deploy') {
            steps {
                xldCreatePackage artifactsPath: './', darPath: '$BUILD_NUMBER.dar', manifestPath: './deployit-manifest.xml'
                xldPublishPackage serverCredentials: 'xld', darPath: '$BUILD_NUMBER.dar'
            }
        }
        
        stage ('XL Release') {
            steps {
                xlrCreateRelease releaseTitle: 'Release for $BUILD_TAG', serverCredentials: 'xlr', startRelease: true, template: 'Samples & Tutorials/Sample Release Template with XL Deploy', variables: [[propertyName: 'packageId', propertyValue: 'Applications/BacktraceApp/$BUILD_NUMBER'], [propertyName: 'application', propertyValue: 'BacktraceApp'], [propertyName: 'packageVersion', propertyValue: '$BUILD_NUMBER'], [propertyName: 'ACC environment', propertyValue: 'Environments/dev'], [propertyName: 'QA environment', propertyValue: 'Environments/dev']]
            }
        }
    }
}
