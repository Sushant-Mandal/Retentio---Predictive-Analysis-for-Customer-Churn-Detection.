pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Retentio CI pipeline started.'
                checkout scm
            }
        }

        stage('Verify Tools') {
            steps {
                bat 'git --version'
                bat 'docker --version'
                bat '"C:\\Users\\DELL\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker-compose.exe" version'
            }
        }

        stage('Inspect Workspace') {
            steps {
                bat 'cd'
                bat 'dir'
                bat 'if exist docker-compose.yml (echo docker-compose.yml found) else (echo ERROR: docker-compose.yml missing & exit /b 1)'
            }
        }

        stage('Build Docker Images') {
            steps {
                bat '"C:\\Users\\DELL\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker-compose.exe" -f docker-compose.yml build'
            }
        }
    }

    post {
        success {
            echo 'Retentio CI pipeline succeeded.'
        }
        failure {
            echo 'Retentio CI pipeline failed. Check Console Output.'
        }
    }
}