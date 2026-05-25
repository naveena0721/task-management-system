pipeline {
    agent any

    stages {

        stage('Build') {
            steps {
                bat 'docker build -t taskflow-ai .'
            }
        }

        stage('Stop Old Container') {
            steps {
                bat 'docker stop taskflow-container || exit 0'
                bat 'docker rm taskflow-container || exit 0'
            }
        }

        stage('Run New Container') {
            steps {
                bat 'docker run -d -p 5000:5000 --name taskflow-container taskflow-ai'
            }
        }

    }
}