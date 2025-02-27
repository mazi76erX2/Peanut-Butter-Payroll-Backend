pipeline {
    agent any

    environment {
        RENDER_APP_ID = 'srv-cuvqbhogph6c73e1tda0'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Trigger Deployment on Render') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'render-api-key', variable: 'RENDER_API_KEY')]) {
                        echo "Triggering deployment on Render for app ${RENDER_APP_ID}..."
                        def response = sh(
                            script: """
                            curl -X POST \\
                              -H "Content-Type: application/json" \\
                              -H "Authorization: Bearer ${RENDER_API_KEY}" \\
                              -d '{"clearCache": false}' \\
                              https://api.render.com/v1/deploy/${RENDER_APP_ID}/trigger
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
