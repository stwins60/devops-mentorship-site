pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('d4506f04-b98c-47db-95ce-018ceac27ba6')
        SCANNER_HOME= tool 'sonar-scanner'
        IMAGE_NAME = 'idrisniyi94/devops-mentorship-lab'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Clean workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/stwins60/devops-mentorship-site.git'
            }
        }
        stage('Sonarqube Analysis') {
            steps {
                script {
                    withSonarQubeEnv('sonar-server') {
                        sh "$SCANNER_HOME/bin/sonar-scanner -Dsonar.projectKey=devops-mentorship-site -Dsonar.projectName=devops-mentorship-site"
                    }
                }
            }
        }
        stage('Quality Gate') {
            steps {
                script {
                    withSonarQubeEnv('sonar-server') {
                        waitForQualityGate abortPipeline: false, credentialsId: 'sonar-token'
                    }
                }
            }
        }
        // stage('Pytest') {
        //     steps {
        //         script {
        //             sh "pip install -r requirements.txt --no-cache-dir"
        //             sh "python3 -m pytest --cov=app --cov-report=xml --cov-report=html"
        //         }
        //     }
        // }
        stage('OWASP') {
            steps {
                dependencyCheck additionalArguments: '--scan ./ --disableYarnAudit --disableNodeAudit --nvdApiKey 4bdf4acc-8eae-45c1-bfc4-844d549be812', odcInstallation: 'DP-Check'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }
        stage('Trivy FS Scan') {
            steps {
                script {
                    sh "trivy fs ."
                }
            }
        }
        stage("Login to DockerHub") {
            steps {
                sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
                echo "Login Successful"
            }
        }
        stage("Docker Build") {
            steps {
                script {
                    sh "docker build -t $IMAGE_NAME:$IMAGE_TAG ."
                    echo "Image built successful"
                }
            }
        }
        stage("Trivy Image Scan") {
            steps {
                script {
                    sh "trivy image $IMAGE_NAME:$IMAGE_TAG"
                }
            }
        }
        stage("Docker Push") {
            steps {
                script {
                    sh "docker push $IMAGE_NAME:$IMAGE_TAG"
                }
            }
        }
        stage("Deploy") {
            steps {
                script {
                    def containerName = 'devops-mentorship-site'
                    def previousTag = sh(script: "docker ps -a | grep ${containerName} | awk '{print $2}'", returnStdout: true).trim()
                    def isRunning = sh(script: "docker ps -a | grep ${containerName}", returnStatus: true)
                    if(isRunning == 0) {
                        sh "docker rm -f ${containerName}"
                        slackSend channel: '#alerts', color: 'danger', message: "${containerName} with version ${previousTag} has been removed and replaced with version ${IMAGE_TAG}"
                        sh "docker run -d --name ${containerName} -p 5430:5000 --restart unless-stopped $IMAGE_NAME:$IMAGE_TAG"
                        slackSend channel: '#alerts', color: 'good', message: "${containerName} with version ${IMAGE_TAG} has been deployed successfully and currently running at https://devops-mentorship-lab.africantech.dev/"
                    }
                    else {
                        sh "docker run -d --name ${containerName} -p 5430:5000 --restart unless-stopped $IMAGE_NAME:$IMAGE_TAG"
                       slackSend channel: '#alerts', color: 'good', message: "${containerName} with version ${IMAGE_TAG} has been deployed successfully and currently running at https://devops-mentorship-lab.africantech.dev/"
                    }
                }
            }
        }
    }
    post {
        success {
           
            slackSend channel: '#alerts', color: 'good', message: "${currentBuild.currentResult}: \nJOB_NAME: ${env.JOB_NAME} \nBUILD_NUMBER: ${env.BUILD_NUMBER} \nBRANCH_NAME: ${env.BRANCH_NAME}. \n More Info ${env.BUILD_URL}"
        }
        failure {

            slackSend channel: '#alerts', color: 'danger', message: "${currentBuild.currentResult}: \nJOB_NAME: ${env.JOB_NAME} \nBUILD_NUMBER: ${env.BUILD_NUMBER} \nBRANCH_NAME: ${env.BRANCH_NAME}. \n More Info ${env.BUILD_URL}"
        }
    }
}