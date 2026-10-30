pipeline {
    agent any

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
                bat '''
                    if not exist app.py (
                        echo ERROR: app.py not found
                        exit /b 1
                    )

                    if not exist requirements.txt (
                        echo ERROR: requirements.txt not found
                        exit /b 1
                    )

                    echo Flask project files found.
                '''
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                bat '''
                    if not exist "%VENV%" (
                        "%PYTHON%" -m venv "%VENV%"
                    )

                    "%WORKSPACE%\\.venv\\Scripts\\python.exe" -m pip install --upgrade pip

                    "%WORKSPACE%\\.venv\\Scripts\\python.exe" -m pip install -r requirements.txt

                    "%WORKSPACE%\\.venv\\Scripts\\python.exe" -m pip install pytest==7.4.2
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    powershell -NoProfile -ExecutionPolicy Bypass -Command "$tests = Get-ChildItem -Path . -Recurse -File -Filter 'test_*.py' | Where-Object { $_.FullName -notmatch '\\\\.venv\\\\|\\\\.git\\\\' }; if ($tests) { & '.\\.venv\\Scripts\\python.exe' -m pytest --maxfail=1 --disable-warnings; exit $LASTEXITCODE } else { Write-Host 'No test files found. Skipping tests.' }"
                '''
            }
        }

        stage('Deploy to IIS') {
            steps {
                echo "Copying Flask project files to IIS..."

                bat '''
                    if not exist "%DEPLOY_PATH%" mkdir "%DEPLOY_PATH%"

                    robocopy "%WORKSPACE%" "%DEPLOY_PATH%" /E /XD .git .venv venv __pycache__ /XF Jenkinsfile

                    if %ERRORLEVEL% GEQ 8 exit /b %ERRORLEVEL%
                '''

                echo "Restarting IIS App Pool..."

                bat '''
                    powershell -NoProfile -ExecutionPolicy Bypass -Command "Import-Module WebAdministration; Restart-WebAppPool -Name '%APP_POOL%' -ErrorAction Stop"
                '''
            }
        }

        stage('Deployment Verification') {
            steps {
                echo "Checking IIS application..."

                bat '''
                    powershell -NoProfile -ExecutionPolicy Bypass -Command "try { $r = Invoke-WebRequest -Uri 'http://127.0.0.1:8085/' -UseBasicParsing -TimeoutSec 20; Write-Host ('HTTP Status: ' + $r.StatusCode); if ($r.StatusCode -ne 200) { exit 1 } } catch { Write-Host $_.Exception.Message; exit 1 }"
                '''
            }
        }
    }

    post {
        success {
            echo "Deployment successful! URL: http://localhost:8085/"
        }

        failure {
            echo "Pipeline failed. Please check Jenkins console output."
        }
    }
}
