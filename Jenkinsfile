pipeline{
    agent any
       environment{
        VERSION = "${env.BUILD_ID}"
       }
    stages{
        stage("docker build and push"){
            steps{
                script{
                    withCredentials([string(credentialsId: 'Docker_hub', variable: 'DOC_PASS')]) {
                        sh '''
                         docker build -t khaira23/testapp:${VERSION} .
                         echo $DOC_PASS  | docker login -u khaira23 --password-stdin  
                         docker push khaira23/testapp:${VERSION} 
                         docker rmi khaira23/testapp:${VERSION}            
                        '''
                    }
                 }
              } 
           }
        }  
    } 
