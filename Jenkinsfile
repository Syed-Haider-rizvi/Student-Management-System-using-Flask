pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        APP_NAME = "Student Management System using Flask"

        DEPLOY_PATH = "C:\\inetpub\\wwwroot\\Student Management System using Flask"

        VENV = ".venv"

        PYTHON = "C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python310\\python.exe"

        APP_POOL = "Student Management System using Flask"
    }

    stages {

        stage('Validate Project') {
            steps {
                echo "Checking Flask Project Files..."

                bat """
                    if not exist "%WORKSPACE%\\app.py" (
                        echo ERROR: app.py not found
                        exit /b 1
                    )

                    if not exist "%WORKSPACE%\\requirements.txt" (
                        echo ERROR: requirements.txt not found
                        exit /b 1
                    )
                """
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                echo "Setting up Python Virtual Environment..."

                bat """
                    if not exist "%PYTHON%" (
                        echo ERROR: Python not found
                        exit /b 1
                    )

                    if not exist "%WORKSPACE%\\%VENV%\\Scripts\\python.exe" (
                        "%PYTHON%" -m venv "%WORKSPACE%\\%VENV%"
                    )

                    "%WORKSPACE%\\%VENV%\\Scripts\\python.exe" -m pip install --upgrade pip

                    "%WORKSPACE%\\%VENV%\\Scripts\\python.exe" -m pip install -r "%WORKSPACE%\\requirements.txt"

                    "%WORKSPACE%\\%VENV%\\Scripts\\python.exe" -m pip install pytest==7.4.2
                """
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running Flask Project Tests..."

                bat """
                    cd /d "%WORKSPACE%"

                    "%WORKSPACE%\\%VENV%\\Scripts\\python.exe" -m pytest --maxfail=1 --disable-warnings
                """
            }
        }

        stage('Deploy to IIS') {
            steps {
                echo "Copying Flask Project Files to IIS..."

                bat """
                    if not exist "%DEPLOY_PATH%" (
                        mkdir "%DEPLOY_PATH%"
                    )

                    robocopy "%WORKSPACE%" "%DEPLOY_PATH%" /E /XD "%WORKSPACE%\\.git" "%WORKSPACE%\\.venv" "%WORKSPACE%@tmp" /XF "Jenkinsfile"

                    if %ERRORLEVEL% GEQ 8 exit /b %ERRORLEVEL%
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
                    powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'http://127.0.0.1:8085/' -UseBasicParsing -TimeoutSec 20"
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
