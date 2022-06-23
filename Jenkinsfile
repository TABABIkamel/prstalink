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
                bat "mvn sonar:sonar -Dsonar.projectKey=com.prestalink.tb:ao-service -Dsonar.host.url=http://localhost:9000   -Dsonar.login=e373b00107cf3748fec2e60202b5831d7d426f73"
            }
        }
        stage('livraison') {   
            steps {
                bat "docker build -t 1901199891/ms-appel-offree ."
                bat "docker push 1901199891/ms-appel-offree"
                bat "docker-compose up"
            }
        }
        
    }
        
    }
    
