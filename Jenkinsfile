
pipeline {
    agent any
    stages {
        stage('Clone') {
    steps {
        git url: 'https://github.com/hoangnhobe/ecommerce-app.git', branch: 'main'
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
