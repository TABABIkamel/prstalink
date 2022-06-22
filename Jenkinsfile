pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                
                bat "mvn compile -Dmaven.test.failure.ignore=true clean install package"

            }
        }
        stage('tests unitaires') {
            steps {

                bat "mvn test"
            }
        }
        
    }
        
    }
    
