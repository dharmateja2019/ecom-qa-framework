pipeline {
    agent any

    environment {
        PATH = "/usr/local/bin:/opt/homebrew/bin:${env.PATH}"
        DOCKER_HOST = "unix:///Users/dharmateja/.orbstack/run/docker.sock"
        COMPOSE_PROJECT_NAME = "qaecommerce"
        PYTHONUNBUFFERED = "1"
    }

    parameters {
        choice(
            name: 'TEST_SUITE',
            choices: ['SMOKE', 'REGRESSION', 'API', 'DB', 'UI', 'ALL'],
            description: 'Select test suite to execute'
        )
    }

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '15'))
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Verify Docker') {
            steps {
                sh '''
                    docker version
                    docker compose version
                '''
            }
        }

        stage('Build Container') {
            steps {
                sh 'docker compose build --no-cache'
            }
        }

        stage('Run Selected Tests') {
            steps {
                script {

                    def cmd = ""

                    if (params.TEST_SUITE == "SMOKE") {
                        cmd = "pytest tests/ -m smoke -n auto --alluredir=allure-results --reruns 2 --reruns-delay 1"
                    }
                    else if (params.TEST_SUITE == "REGRESSION") {
                        cmd = "pytest tests/ -m regression -n auto --alluredir=allure-results --reruns 2 --reruns-delay 1"
                    }
                    else if (params.TEST_SUITE == "API") {
                        cmd = "pytest tests/api -n auto --alluredir=allure-results --reruns 2 --reruns-delay 1"
                    }
                    else if (params.TEST_SUITE == "DB") {
                        cmd = "pytest tests/db -n auto --alluredir=allure-results --reruns 2 --reruns-delay 1"
                    }
                    else if (params.TEST_SUITE == "UI") {
                        cmd = "pytest tests/ui -n auto --alluredir=allure-results --reruns 2 --reruns-delay 1"
                    }
                    else {
                        cmd = "pytest tests/ -n auto --alluredir=allure-results --reruns 2 --reruns-delay 1"
                    }

                    sh """
                        docker compose run --rm qa-tests ${cmd}
                    """
                }
            }
        }
    }

    post {

        success {
            echo "✅ ${params.TEST_SUITE} tests passed successfully."
        }

        failure {
            echo "❌ ${params.TEST_SUITE} tests failed."
        }

        always {
            sh '''
                docker compose down -v || true
                docker system prune -f || true
            '''
            archiveArtifacts artifacts: 'reports/**/*,allure-results/**/*', allowEmptyArchive: true
            echo "Build Result: ${currentBuild.currentResult}"
        }
    }
}