pipeline {
    agent any

    environment {
        IMAGE = "reshath/dvp-week12-app"
        TAG   = "${env.BUILD_NUMBER}"
    }

    triggers { githubPush() }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Build & Test') {
            steps {
                bat 'python -m pip install -r requirements.txt'
                bat 'python -m pytest -q'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    bat "${tool 'sonar-scanner'}\\bin\\sonar-scanner.bat"
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Docker Build') {
            steps {
                bat "docker build -t %IMAGE%:%TAG% -t %IMAGE%:latest ."
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                 usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
                    bat 'echo %DH_PASS% | docker login -u %DH_USER% --password-stdin'
                    bat "docker push %IMAGE%:%TAG%"
                    bat "docker push %IMAGE%:latest"
                }
            }
        }

        stage('Deploy') {
            steps {
                bat 'docker rm -f dvp-week12-app 2>nul || exit 0'
                bat "docker run -d --name dvp-week12-app -p 5000:5000 %IMAGE%:latest"
            }
        }
    }

    post {
        always { bat 'docker logout' }
    }
}