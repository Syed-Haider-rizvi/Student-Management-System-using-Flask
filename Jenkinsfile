pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        skipDefaultCheckout(true)
    }

    environment {
        APP_NAME = "StudentManagementFlask"
        REPO_URL = "https://github.com/Syed-Haider-rizvi/Student-Management-System-using-Flask.git"
        BRANCH = "main"
        PROJECT_DIR = "Student Management System using Flask"
        DEPLOY_PATH = "C:\\inetpub\\wwwroot\\Student Management System using Flask"
        VENV = "C:\\inetpub\\wwwroot\\Student Management System using Flask\\venv"
        PYTHON = "C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python310\\python.exe"
        APP_POOL = "Student Management System using Flask"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Cloning Student Management System Repository..."
                git branch: "${BRANCH}", url: "${REPO_URL}"
            }
        }

        stage('Validate Project') {
            steps {
                bat """
                    if not exist "%WORKSPACE%\\%PROJECT_DIR%\\app.py" (
                        echo ERROR: app.py not found
                        exit /b 1
                    )

                    if not exist "%WORKSPACE%\\%PROJECT_DIR%\\requirements.txt" (
                        echo ERROR: requirements.txt not found
                        exit /b 1
                    )
                """
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                echo "Creating Python Virtual Environment..."
                bat """
                    if not exist "%PYTHON%" (
                        echo ERROR: Python not found
                        exit /b 1
                    )

                    if not exist "%VENV%\\Scripts\\python.exe" (
                        "%PYTHON%" -m venv "%VENV%"
                    )

                    "%VENV%\\Scripts\\python.exe" -m pip install --upgrade pip
                    "%VENV%\\Scripts\\python.exe" -m pip install -r "%WORKSPACE%\\%PROJECT_DIR%\\requirements.txt"
                    "%VENV%\\Scripts\\python.exe" -m pip install waitress
                """
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running Flask Project Tests..."
                bat """
                    cd /d "%WORKSPACE%\\%PROJECT_DIR%"

                    if exist tests (
                        "%VENV%\\Scripts\\python.exe" -m pip install pytest==7.4.2
                        "%VENV%\\Scripts\\python.exe" -m pytest tests --maxfail=1 --disable-warnings
                    ) else (
                        echo No tests folder found. Skipping tests.
                    )
                """
            }
        }

        stage('Deploy Files') {
            steps {
                echo "Deploying Student Management System to IIS..."
                bat """
                    if not exist "%DEPLOY_PATH%" (
                        mkdir "%DEPLOY_PATH%"
                    )

                    xcopy "%WORKSPACE%\\%PROJECT_DIR%\\*" "%DEPLOY_PATH%\\" /E /I /Y
                """
            }
        }

        stage('Restart Flask Service') {
            steps {
                echo "Restarting Flask Windows Service..."
                bat """
                    powershell -NoProfile -ExecutionPolicy Bypass -Command "Restart-Service -Name '%APP_NAME%' -Force -ErrorAction Stop"
                """
            }
        }

        stage('Restart IIS App Pool') {
            steps {
                echo "Restarting Student Management System using Flask App Pool..."

                bat """
                    powershell -NoProfile -ExecutionPolicy Bypass -Command "Import-Module WebAdministration; Restart-WebAppPool -Name '%APP_POOL%' -ErrorAction Stop"
                """
            }
        }

        stage('Deployment Verification') {
            steps {
                echo "Checking Flask Application..."
                bat """
                    powershell -NoProfile -ExecutionPolicy Bypass -Command "try { \$response = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/' -UseBasicParsing -TimeoutSec 20; exit 0 } catch { Write-Error \$_; exit 1 }"
                """
            }
        }
    }

    post {
        success {
            echo "Deployment Successful!"
            echo "Application: Student Management System"
            echo "IIS Path: C:\\inetpub\\wwwroot\\Student Management System using Flask"
            echo "URL: http://localhost:8085/"
        }

        failure {
            echo "Deployment Failed! Check Jenkins Console Output."
        }
    }
}
