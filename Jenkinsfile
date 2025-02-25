pipeline {
    agent any

    environment {
        AWS_ACCOUNT_ID     = '905418310640'
        AWS_DEFAULT_REGION = 'af-south-1'
        IMAGE_REPO_NAME    = 'peanut-butter-payroll-backend'
        IMAGE_TAG          = "${env.BUILD_NUMBER}"
        REPOSITORY_URI     = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${IMAGE_REPO_NAME}"

        RENDER_SERVICE_ID  = 'srv_cuuq5itsvqrc73dplbd0'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image ${IMAGE_REPO_NAME}:${IMAGE_TAG}"
                    sh "docker build -t ${IMAGE_REPO_NAME}:${IMAGE_TAG} ."
                }
            }
        }
        
        stage('Login to AWS ECR and Push Image') {
            steps {
                script {
                    echo "Logging in to AWS ECR..."
                    sh """
                       aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | \
                           docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com
                    """
                    echo "Tagging and pushing image to AWS ECR..."
                    sh "docker tag ${IMAGE_REPO_NAME}:${IMAGE_TAG} ${REPOSITORY_URI}:${IMAGE_TAG}"
                    sh "docker push ${REPOSITORY_URI}:${IMAGE_TAG}"
                }
            }
        }
        
        stage('Trigger Deployment on Render') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'render-api-key', variable: 'RENDER_API_KEY')]) {
                        echo "Triggering deployment on Render for service ${RENDER_SERVICE_ID}..."
                        def response = sh(
                            script: """
                            curl -X POST \\
                              -H "Accept: application/json" \\
                              -H "Authorization: Bearer ${RENDER_API_KEY}" \\
                              -H "Content-Type: application/json" \\
                              -d '{"clearCache": false}' \\
                              https://api.render.com/v1/deploy/${RENDER_SERVICE_ID}/trigger
                            """,
                            returnStdout: true
                        ).trim()
                        echo "Render deployment response: ${response}"
                    }
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}
