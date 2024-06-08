pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('5f8b634a-148a-4067-b996-07b4b3276fba')
        SCANNER_HOME= tool 'sonar-scanner'
        DOCKERHUB_USERNAME = 'idrisniyi94'
        DEPLOYMENT_NAME = 'devops-mentorship-site'
        IMAGE_TAG = "v.0.${env.BUILD_NUMBER}"
        IMAGE_NAME = "${DOCKERHUB_USERNAME}/${DEPLOYMENT_NAME}:${IMAGE_TAG}"
        NVDAPIKEY = credentials('ed62b912-6db4-4d3a-a445-a1799077253e')
        NAMESPACE = 'mentorship'
        BRANCH_NAME = "${GIT_BRANCH.split('/')[1]}"
    }

    stages {
        stage('Clean workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/dev'], [name: '*/staging'], [name: '*/prod']], userRemoteConfigs: [[url: 'https://github.com/stwins60/devops-mentorship-site.git']]])
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
                dependencyCheck additionalArguments: "--scan ./ --disableYarnAudit --disableNodeAudit --nvdApiKey ${env.NVDAPIKEY}", odcInstallation: 'DP-Check'
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
                    sh "docker build -t $IMAGE_NAME --build-arg SENDGRID_API_KEY=$SENDGRID_API_KEY ."
                    echo "Image built successful"
                }
            }
        }
        stage("Trivy Image Scan") {
            steps {
                script {
                    sh "trivy image $IMAGE_NAME"
                }
            }
        }
        stage("Docker Push") {
            steps {
                script {
                    sh "docker push $IMAGE_NAME"
                }
            }
        }
        stage("Deploy") {
            steps {
                script {
                    dir('k8s') {
                        kubeconfig(credentialsId: '3f12ff7b-93cb-4ea5-bc21-79bcf5fb1925', serverUrl: '') {
                            if (env.BRANCH_NAME == 'dev') {
                                sh "sed -i 's|IMAGE_NAME|${IMAGE_NAME}|g' overlays/dev/kustomization.yaml"
                                sh "kubectl build overlays/dev | kubectl apply -f -"
                                slackSend channel: '#alerts', color: 'good', message: "DevOps Mentorship Site Deployed Successfully with image tag ${IMAGE_TAG} \n URL: https://devops-mentorship-lab.africantech.dev \n More Info ${env.BUILD_URL}"
                            } else if (env.BRANCH_NAME == 'staging') {
                                sh "sed -i 's|IMAGE_NAME|${IMAGE_NAME}|g' overlays/staging/kustomization.yaml"
                                sh "kubectl build overlays/staging | kubectl apply -f -"
                                slackSend channel: '#alerts', color: 'good', message: "DevOps Mentorship Site Deployed Successfully with image tag ${IMAGE_TAG} \n URL: https://devops-mentorship-staging.africantech.dev \n More Info ${env.BUILD_URL}"
                            } else if (env.BRANCH_NAME == 'prod') {
                                sh "sed -i 's|IMAGE_NAME|${IMAGE_NAME}|g' overlays/prod/kustomization.yaml"
                                sh "kubectl build overlays/prod | kubectl apply -f -"
                                slackSend channel: '#alerts', color: 'good', message: "DevOps Mentorship Site Deployed Successfully with image tag ${IMAGE_TAG} \n URL: https://devops-mentorship.africantech.dev \n More Info ${env.BUILD_URL}"
                            } else {
                                slackSend channel: '#alerts', color: 'danger', message: "Deployment failed. Branch name not found"
                            }
                        }
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