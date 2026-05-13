pipeline {
    agent any

    stages {

        stage('Clone') {
            steps {
                echo 'Project Ready'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t task-system .'
            }
        }

        stage('Run Container') {
            steps {
                bat 'docker run -d -p 5000:5000 task-system'
            }
        }

    }
}