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
                bat "mvn sonar:sonar -Dsonar.projectKey=configuration -Dsonar.host.url=http://localhost:9000 -Dsonar.login=db9b523a9966e67292b7874eef045503f8a18c0e"
            }
        }
        stage('livraison') {      
            steps {  
                bat "docker login --username 1901199891 --password Tunis19981998"
                bat "docker build -t 1901199891/ms-configuration ."
                bat "docker push 1901199891/ms-configuration"
            }
        }
        
    }
        
    }
    
