pipeline {
    agent {
        docker  {
            image 'maven:3.8.1-adoptopenjdk-11' 
            args '-v /root/.m2:/root/.m2' 
        }
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
    
