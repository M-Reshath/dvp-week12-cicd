pipeline {
    agent { label 'vm-docker' }

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
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements.txt
                    python -m pytest -q
                '''
            }
        }

        stage('SonarQube Analysis + Quality Gate') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh "${tool 'sonar-scanner'}/bin/sonar-scanner -Dsonar.qualitygate.wait=true"
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t $IMAGE:$TAG -t $IMAGE:latest .'
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                 usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
                    sh 'echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin'
                    sh 'docker push $IMAGE:$TAG'
                    sh 'docker push $IMAGE:latest'
                }
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker rm -f dvp-week12-app || true'
                sh 'docker run -d --name dvp-week12-app -p 5000:5000 $IMAGE:latest'
            }
        }
    }

    post {
        always { sh 'docker logout || true' }
    }
}