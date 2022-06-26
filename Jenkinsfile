pipeline {
    agent any
    tools {
        maven 'M3'
    }
    stages {
        stage('Build') {
            steps {
                
                bat "mvn compile -Dmaven.test.failure.ignore=true clean install package"

            }
        }
        stage('tests static') {
            steps {
                bat "mvn sonar:sonar -Dsonar.projectKey=api-gateway -Dsonar.host.url=http://localhost:9000 -Dsonar.login=e48ddf3b448c7e87eb3f020516f104cb25dcbc4d"
            }
        }
        stage('livraison') {      
            steps { 
                bat "docker login --username 1901199891 --password Tunis19981998"
                bat "docker build -t 1901199891/ms-apigateway ."
                bat "docker push 1901199891/ms-apigateway"
            }
        }
        
    }
        
    }
    
