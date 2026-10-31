pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        skipDefaultCheckout(true)
    }

    environment {
        APP_NAME    = "StudentManagementFlask"
        REPO_URL    = "https://github.com/Syed-Haider-rizvi/Student-Management-System-using-Flask.git"
        BRANCH      = "main"
        DEPLOY_PATH = "C:\\inetpub\\wwwroot\\Student Management System using Flask"
        VENV        = "C:\\inetpub\\wwwroot\\Student Management System using Flask\\venv"
        PYTHON      = "C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python310\\python.exe"
        APP_POOL    = "Student Management System using Flask"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Cloning Student Management System Repository..."
                git branch: "${BRANCH}",
                    url: "${REPO_URL}"
            }
        }

        stage('Validate Project') {
            steps {
                bat '''
                    if not exist "%WORKSPACE%\\app.py" (
                        echo ERROR: app.py not found in workspace
                        exit /b 1
                    )

                    if not exist "%WORKSPACE%\\requirements.txt" (
                        echo ERROR: requirements.txt not found in workspace
                        exit /b 1
                    )

                    echo [SUCCESS] Flask project files verified.
                '''
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                echo "Configuring Python Virtual Environment..."
                bat '''
                    if not exist "%PYTHON%" (
                        echo ERROR: Python executable not found at %PYTHON%
                        exit /b 1
                    )

                    if not exist "%VENV%\\Scripts\\python.exe" (
                        "%PYTHON%" -m venv "%VENV%"
                    )

                    "%VENV%\\Scripts\\python.exe" -m pip install --upgrade pip
                    "%VENV%\\Scripts\\python.exe" -m pip install -r "%WORKSPACE%\\requirements.txt"
                    "%VENV%\\Scripts\\python.exe" -m pip install waitress pytest==7.4.2
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running Unit Tests..."
                bat '''
                    cd /d "%WORKSPACE%"

                    if exist tests (
                        "%VENV%\\Scripts\\python.exe" -m pytest tests --maxfail=1 --disable-warnings
                    ) else (
                        echo [INFO] No tests directory found. Skipping tests.
                        exit /b 0
                    )

                    :: Handle pytest exit codes
                    if errorlevel 6 exit /b %ERRORLEVEL%
                    if errorlevel 5 (
                        echo [INFO] No tests collected (exit code 5). Continuing pipeline...
                        exit /b 0
                    )
                    if errorlevel 1 exit /b %ERRORLEVEL%
                    exit /b 0
                '''
            }
        }

        stage('Deploy Files') {
            steps {
                echo "Deploying application files to IIS (${DEPLOY_PATH})..."
                bat '''
                    if not exist "%DEPLOY_PATH%" mkdir "%DEPLOY_PATH%"

                    :: Robocopy files excluding git, venv, cache and log files
                    robocopy "%WORKSPACE%" "%DEPLOY_PATH%" /E /XD .git .venv venv __pycache__ .pytest_cache /XF Jenkinsfile *.log
                    if %ERRORLEVEL% LEQ 7 (exit /b 0) else (exit /b %ERRORLEVEL%)
                '''
            }
        }

        stage('Restart Flask Service') {
            steps {
                echo "Restarting Flask Windows Service (${APP_NAME})..."
                bat '''
                    powershell -NoProfile -ExecutionPolicy Bypass -Command "$svc = Get-Service -Name '%APP_NAME%' -ErrorAction SilentlyContinue; if ($svc) { Restart-Service -Name '%APP_NAME%' -Force; Write-Host 'Service %APP_NAME% restarted successfully.' } else { Write-Warning 'Service %APP_NAME% is not installed on this machine. If using a Windows Service for Waitress, install it using NSSM. Continuing pipeline...' }"
                '''
            }
        }

        stage('Restart IIS App Pool') {
            steps {
                echo "Recycling IIS App Pool (${APP_POOL})..."
                bat '''
                    %windir%\\system32\\inetsrv\\appcmd.exe recycle apppool /apppool.name:"%APP_POOL%"
                '''
            }
        }

        stage('Deployment Verification') {
            steps {
                echo "Verifying application availability..."
                bat '''
                    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Sleep -Seconds 2; try { $res = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/' -UseBasicParsing -TimeoutSec 10; Write-Host ('Backend Status: ' + $res.StatusCode) } catch { Write-Warning ('Backend check: ' + $_.Exception.Message) }"
                '''
            }
        }
    }

    post {
        success {
            echo "=========================================================="
            echo "✅ Deployment Successful!"
            echo "Application: Student Management System"
            echo "IIS Path:    ${env.DEPLOY_PATH}"
            echo "Reverse Proxy URL: http://localhost:8085/"
            echo "Direct Flask URL:  http://localhost:8000/"
            echo "=========================================================="
        }

        failure {
            echo "❌ Deployment Failed! Please check the Jenkins console output."
        }
    }
}
