
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
                bat 'docker compose version'
            }
        }

        stage('Build Docker Images') {
            steps {
                bat 'docker compose build'
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
