
pipeline {
    agent any
    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/yourusername/ecommerce-app.git'
            }
        }
        stage('Build and Deploy') {
            steps {
                sh 'docker-compose down || true'
                sh 'docker-compose build'
                sh 'docker-compose up -d'
            }
        }
    }
}
