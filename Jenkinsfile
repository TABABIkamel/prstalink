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
                bat "mvn sonar:sonar -Dsonar.projectKey=eureka -Dsonar.host.url=http://localhost:9000 -Dsonar.login=b7a99e3c7eeea8ceffc3984d5508fa18222c76f4"
            }
        }
        stage('livraison') {      
            steps { 
                bat "docker login --username 1901199891 --password Tunis19981998"
                bat "docker build -t 1901199891/ms_eureka ."
                bat "docker push 1901199891/ms_eureka"
            }
        }
        
    }
        
    }
    
