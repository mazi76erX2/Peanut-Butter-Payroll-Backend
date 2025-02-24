pipeline {
    agent any
    
    environment {
        AWS_ACCOUNT_ID = credentials('AWS_ACCOUNT_ID')
        AWS_DEFAULT_REGION = 'af-south-1'
        IMAGE_REPO_NAME = 'peanut-butter-payroll-backend:latest'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        REPOSITORY_URI = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${IMAGE_REPO_NAME}"
        ECS_CLUSTER = 'peanut-butter-payroll-backend'
        ECS_SERVICE = 'peanut-butter-payroll-backend-service'
        TASK_DEFINITION_NAME = 'peanut-butter-payroll-backend-task'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install AWS CLI') {
            steps {
                sh '''
                    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
                    unzip awscliv2.zip
                    sudo ./aws/install
                '''
            }
        }
        
        stage('Configure AWS credentials') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', 
                                credentialsId: 'aws-credentials',
                                accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                                secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                    sh 'aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID'
                    sh 'aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY'
                    sh 'aws configure set default.region ${AWS_DEFAULT_REGION}'
                }
            }
        }
        
        stage('Login to ECR') {
            steps {
                sh 'aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com'
            }
        }
        
        stage('Build and Push Docker Image') {
            steps {
                dir('docker/backend') {
                    sh '''
                        docker build -t ${IMAGE_REPO_NAME}:${IMAGE_TAG} .
                        docker tag ${IMAGE_REPO_NAME}:${IMAGE_TAG} ${REPOSITORY_URI}:${IMAGE_TAG}
                        docker push ${REPOSITORY_URI}:${IMAGE_TAG}
                    '''
                }
            }
        }
        
        stage('Update ECS Task Definition') {
            steps {
                script {
                    def taskDef = sh(
                        script: "aws ecs describe-task-definition --task-definition ${TASK_DEFINITION_NAME} --region ${AWS_DEFAULT_REGION}",
                        returnStdout: true
                    ).trim()
                    
                    def updatedTaskDef = taskDef.replaceAll(
                        "image\": \"${REPOSITORY_URI}:[a-zA-Z0-9._-]+\"",
                        "image\": \"${REPOSITORY_URI}:${IMAGE_TAG}\""
                    )
                    
                    sh """
                        echo '${updatedTaskDef}' > task-definition.json
                        aws ecs register-task-definition \
                            --cli-input-json file://task-definition.json \
                            --region ${AWS_DEFAULT_REGION}
                    """
                }
            }
        }
        
        stage('Deploy to ECS') {
            steps {
                sh """
                    aws ecs update-service \
                        --cluster ${ECS_CLUSTER} \
                        --service ${ECS_SERVICE} \
                        --task-definition ${TASK_DEFINITION_NAME} \
                        --force-new-deployment \
                        --region ${AWS_DEFAULT_REGION}
                """
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}