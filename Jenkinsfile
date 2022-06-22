pipeline {
    agent any
    tools {
        maven 'Maven 3.3.9'
        jdk 'jdk11'
    }
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
    
