
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out Retentio repository'
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
                bat 'echo Current directory:'
                bat 'cd'
                bat 'echo Repository files:'
                bat 'dir'
                bat 'echo Searching for Compose configuration:'
                bat 'where /r . docker-compose.yml'
                bat 'where /r . compose.yaml'
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
            echo 'Pipeline failed. Check the workspace inspection output.'
        }
    }
}
