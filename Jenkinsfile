pipeline {
    agent any

    environment {
        AWS_ACCOUNT_ID    = '905418310640'
        AWS_DEFAULT_REGION= 'af-south-1'
        IMAGE_REPO_NAME   = 'peanut-butter-payroll-backend'
        IMAGE_TAG         = "${env.BUILD_NUMBER}"
        REPOSITORY_URI    = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${IMAGE_REPO_NAME}"
        ECS_CLUSTER       = 'peanut-butter-payroll-backend'
        ECS_SERVICE       = 'peanut-butter-payroll-backend-service'
        TASK_DEFINITION   = 'peanut-butter-payroll-backend'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Configure AWS credentials') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding', 
                    credentialsId: 'aws-credentials',
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    sh '''
                      aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                      aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                      aws configure set default.region ${AWS_DEFAULT_REGION}
                    '''
                }
            }
        }
        
        stage('Login to ECR') {
            steps {
                sh '''
                    aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | \
                      docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com
                '''
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_REPO_NAME}:${IMAGE_TAG} -f docker/backend/Dockerfile .
                    docker tag ${IMAGE_REPO_NAME}:${IMAGE_TAG} ${REPOSITORY_URI}:${IMAGE_TAG}
                    docker push ${REPOSITORY_URI}:${IMAGE_TAG}
                '''
            }
        }

        stage('Update ECS Task Definition') {
            steps {
                script {
                    // Extract the inner task definition and remove keys that ECS doesn't allow.
                    def filteredTaskDef = sh(
                        script: """
                            aws ecs describe-task-definition --task-definition ${TASK_DEFINITION} --region ${AWS_DEFAULT_REGION} | \
                            jq '.taskDefinition | del(.taskDefinitionArn, .revision, .status, .requiresAttributes, .compatibilities, .registeredAt, .registeredBy)'
                        """,
                        returnStdout: true
                    ).trim()

                    // Optionally, verify the top-level keys (for debugging):
                    sh "echo '${filteredTaskDef}' | jq 'keys'"

                    // Write the filtered JSON to a file.
                    writeFile file: 'task-definition.json', text: filteredTaskDef

                    // Register the new task definition.
                    sh """
                        aws ecs register-task-definition \
                            --cli-input-json file://task-definition.json \
                            --region ${AWS_DEFAULT_REGION}
                    """
                }
            }
        }
        
        stage('Deploy to ECS') {
            steps {
                sh '''
                    aws ecs update-service \
                        --cluster ${ECS_CLUSTER} \
                        --service ${ECS_SERVICE} \
                        --task-definition ${TASK_DEFINITION} \
                        --force-new-deployment \
                        --region ${AWS_DEFAULT_REGION}
                '''
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}
