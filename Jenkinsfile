pipeline {
    agent any

    environment {
        // DigitalOcean Container Registry settings
        DO_REGISTRY       = "registry.digitalocean.com"
        DO_REGISTRY_NAME  = "peanut-butter-payroll"
        IMAGE_REPO_NAME   = "peanut-butter-payroll-backend"
        IMAGE_TAG         = "${env.BUILD_NUMBER}"
        REPOSITORY_URI    = "${DO_REGISTRY}/${DO_REGISTRY_NAME}/${IMAGE_REPO_NAME}"
        
        // DigitalOcean App Platform settings
        DO_APP_ID         = "3d885442-a322-402b-8b6b-3c5570903ed0"
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
        
        stage('Login to DigitalOcean Container Registry and Push Image') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'do-api-key', variable: 'DO_API_KEY')]) {
                        echo "Logging in to DigitalOcean Container Registry..."
                        // DigitalOcean uses the literal username "do" with your API token as the password.
                        sh """
                        echo $DO_API_KEY | docker login ${DO_REGISTRY} -u do --password-stdin
                        """
                    }
                    echo "Tagging image as ${REPOSITORY_URI}:${IMAGE_TAG}"
                    sh "docker tag ${IMAGE_REPO_NAME}:${IMAGE_TAG} ${REPOSITORY_URI}:${IMAGE_TAG}"
                    echo "Pushing image to DigitalOcean Container Registry..."
                    sh "docker push ${REPOSITORY_URI}:${IMAGE_TAG}"
                }
            }
        }
        
        stage('Trigger Deployment on DigitalOcean App Platform') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'do-api-key', variable: 'DO_API_KEY')]) {
                        echo "Triggering deployment on DigitalOcean App Platform for app ${DO_APP_ID}..."
                        def response = sh (
                            script: """
                            curl -X POST \\
                              -H "Content-Type: application/json" \\
                              -H "Authorization: Bearer ${DO_API_KEY}" \\
                              -d '{"force_build": true}' \\
                              https://api.digitalocean.com/v2/apps/${DO_APP_ID}/deployments
                            """,
                            returnStdout: true
                        ).trim()
                        echo "Deployment response: ${response}"
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
