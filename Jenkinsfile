pipeline {
    agent any // Specifies that the pipeline can run on any available agent

    environment {
        flask_image = "atuldockerhub/flask-app-container:flask-gunicorn-sqllite" // Docker image name for the Flask app
        nginx_image = "atuldockerhub/flask-app-container:nginx" // Docker image name for the Nginx server
        custom_agent = "atuldockerhub/python-custom-scan-image:latest" // Custom python docker agent image for scans
    }

    stages {
        stage('Checkout code') {
            steps {
                git url: 'git@github.com:atul-yadav-git/public-flask-portfolio', branch: 'master', credentialsId: 'github-ssh-keys'
                echo "Jenkinsfile found in this path: ${workspace}"
            }
        }

        stage('Check for Changes') {
            steps {
                script {
                    def flask_code_change = sh(script: "git diff --name-only HEAD~1 HEAD | grep -q '^flask_gunicorn_app/'", returnStatus: true) == 0
                    def nginx_code_change = sh(script: "git diff --name-only HEAD~1 HEAD | grep -q '^nginx_server_configurations/'", returnStatus: true) == 0

                    if (flask_code_change) {
                        writeFile file: "flask_code_change.txt", text: "true"
                        echo "Changes detected in Flask app."
                    } else {
                        writeFile file: "flask_code_change.txt", text: "false"
                        echo "No changes detected in Flask app."
                    }

                    if (nginx_code_change) {
                        writeFile file: "nginx_code_change.txt", text: "true"
                        echo "Changes detected in nginx server code."
                    } else {
                        writeFile file: "nginx_code_change.txt", text: "false"
                        echo "No changes detected in nginx server code."
                    }

                    stash name: 'envVars', includes: 'flask_code_change.txt,nginx_code_change.txt'
                }
            }
        }

        stage('Pull Latest Flask Custom Image') {
            steps {
                script {
                    sh "docker pull ${custom_agent}"
                    echo "Pulled latest Flask custom image."
                }
            }
        }

        stage('Run Security Scans for Flask') {
            agent {
                docker {
                    image 'atuldockerhub/python-custom-scan-image:latest'
                }
            }
            steps {
                script {
                    unstash 'envVars'
                    def Built_flask_image = readFile("flask_code_change.txt").trim()

                    if (Built_flask_image == "true") {
                        echo "Running security scans on Flask app"
                        echo "1. Running package vulnerability test with pip-audit"
                        sh "pip-audit -r flask_gunicorn_app/requirements.txt > pip-audit-report.txt"
                        echo "2. Running static code security test with Bandit"
                        sh "bandit -r flask_gunicorn_app --severity-level high --format json > bandit-report.json"
                        echo "3. Running flake8 for best practices linting check"
                        try {
                            sh "flake8 flask_gunicorn_app > flake8-report.txt"
                        } catch (Exception e) {
                            echo "Flake8 linting failed, but continuing with the pipeline"
                        }
                        echo "4. Running basic unit tests (smoke tests) with pytest"
                        try {
                            sh "pytest flask_gunicorn_app/test_app.py --junitxml=pytest-report.xml"
                        } catch (Exception e) {
                            echo "pytest failed as all app dependencies not in custom agent; continuing pipeline"
                        }
                        archiveArtifacts artifacts: "/**", allowEmptyArchive: true
                    } else {
                        echo "No changes in Flask app; skipping security scans."
                    }
                }
            }
        }

        stage('Build Flask App Image') {
            steps {
                script {
                    unstash 'envVars'
                    def Built_flask_image = readFile("flask_code_change.txt").trim()

                    if (Built_flask_image == "true") {
                        echo "Building Flask Docker image"
                        sh "docker build -t ${flask_image} -f flask_gunicorn_app/Dockerfile.flask_gunicorn_app flask_gunicorn_app/"
                        echo "Flask image built."
                    } else {
                        echo "Flask image not built, no code changes detected."
                    }
                }
            }
        }

        stage('Build Nginx Server Image') {
            steps {
                script {
                    unstash 'envVars'
                    def Built_nginx_image = readFile("nginx_code_change.txt").trim()

                    if (Built_nginx_image == "true") {
                        echo "Building Nginx Docker image"
                        sh "sudo docker build -t ${nginx_image} -f nginx_server_configurations/Dockerfile.nginx nginx_server_configurations/"
                        echo "Nginx image built."
                    } else {
                        echo "Nginx image not built, no code changes detected."
                    }
                }
            }
        }

        stage('Run Security Scan on newly built docker images') {
            steps {
                script {
                    unstash 'envVars'
                    def Built_flask_image = readFile("flask_code_change.txt").trim()
                    def Built_nginx_image = readFile("nginx_code_change.txt").trim()

                    if (Built_flask_image == "true") {
                        echo "Running security scan on Flask app"
                        try {
                            sh """
                                docker run --rm \
                                -v /var/run/docker.sock:/var/run/docker.sock \
                                aquasec/trivy:latest \
                                image --quiet ${flask_image} > trivy_flask_report.txt
                            """
                            echo "Trivy scan for Flask app completed."
                            archiveArtifacts artifacts: "trivy_flask_report.txt", fingerprint: true
                        } catch (Exception e) {
                            echo "Trivy scan for Flask app failed due to: ${e.getMessage()}"
                        }
                        } else {
                              echo "No changes in Flask app; skipping Flask security scan."
                        }

                        if (Built_nginx_image == "true") {
                            echo "Running security scan on Nginx app"
                            try {
                                sh """
                                    docker run --rm \
                                    -v /var/run/docker.sock:/var/run/docker.sock \
                                    aquasec/trivy:latest \
                                    image --quiet ${nginx_image} > trivy_nginx_report.txt
                                """
                                echo "Trivy scan for Nginx app completed."
                                archiveArtifacts artifacts: "trivy_nginx_report.txt", fingerprint: true
                            } catch (Exception e) {
                                echo "Trivy scan for Nginx app failed due to: ${e.getMessage()}"
                            }
                            } else {
                                echo "No changes in Nginx app; skipping Nginx security scan."
                             }
                        }
                }
        }


        stage('Push Images to Docker Hub') {
            steps {
                script {
                    unstash 'envVars'
                    def Built_nginx_image = readFile("nginx_code_change.txt").trim()
                    def Built_flask_image = readFile("flask_code_change.txt").trim()

                    if (Built_flask_image == "true" || Built_nginx_image == "true") {
                        echo "Logging into Docker Hub"

                        withDockerRegistry([credentialsId: 'dockerhub-login', url: 'https://index.docker.io/v1/']) {
                            echo "Successfully logged in"

                            if (Built_flask_image == "true") {
                                echo "Pushing Flask image to Docker Hub"
                                sh "docker push ${flask_image}"
                                echo "Flask image pushed to Docker Hub."
                            } else {
                                echo "Flask image not pushed, no code changes detected"
                            }

                            if (Built_nginx_image == "true") {
                                echo "Pushing Nginx image to Docker Hub"
                                sh "docker push ${nginx_image}"
                                echo "Nginx image pushed to Docker Hub."
                            } else {
                                echo "Nginx image not pushed, no code changes detected"
                            }
                        }
                    } else {
                        echo "No image to push, no code changes detected"
                    }
                }
            }
        }

        stage('Deploy to EC2 - Continuous Deployment') {
            steps {
                script {
                    unstash 'envVars'

                    def Built_nginx_image = readFile("nginx_code_change.txt").trim()
                    def Built_flask_image = readFile("flask_code_change.txt").trim()

                    if (Built_flask_image == "true" || Built_nginx_image == "true") {
                        echo "Logging into EC2"

                        withCredentials([usernamePassword(credentialsId: 'dockerhub-login',
                                                         usernameVariable: 'DOCKER_HUB_USERNAME',
                                                         passwordVariable: 'DOCKER_HUB_PASSWORD')]) {

                            sshagent(['jenkins-ec2-keys']) {
                                sh """
                                ssh -o StrictHostKeyChecking=no ec2-user@public-ip '

                                echo "Navigating to docker-compose directory"
                                cd /home/ec2-user/ &&

                                echo "Logging in to Docker Hub"
                                echo $DOCKER_HUB_PASSWORD | docker login -u $DOCKER_HUB_USERNAME --password-stdin &&

                                echo "Pulling latest images"
                                docker-compose pull &&

                                echo "Stopping old containers"
                                docker-compose down &&

                                echo "Starting new containers"
                                docker-compose up -d
                                '
                                """
                            }
                        }
                    } else {
                        echo "No changes detected, skipping deployment"
                    }
                }
            }
        }
    }
}


