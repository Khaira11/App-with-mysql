pipeline{
    agent any
       environment{
        VERSION = "${env.BUILD_ID}"
       }
    stages{
        stage("docker build and push"){
            steps{
                script{
                    withCredentials([string(credentialsId: 'docker_pass', variable: 'docker_p')]) {
                        sh '''
                         docker build -t 192.168.117.137:9797/harpreet:${VERSION} .
                         echo $docker_p | docker login -u admin --password-stdin 192.168.117.137:9797 
                         docker push 192.168.117.137:9797/harpreet:${VERSION} 
                         docker rmi 192.168.117.137:9797/harpreet:${VERSION}            
                        '''
                    }
                }
            } 
        }
     }
  }
