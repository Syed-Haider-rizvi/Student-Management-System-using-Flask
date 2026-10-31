pipeline {
    agent any

    environment {
        APP_NAME    = "Student Management System using Flask"
        DEPLOY_PATH = "C:\\inetpub\\wwwroot\\Student Management System using Flask"
        VENV        = ".venv"
        PYTHON      = "C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python310\\python.exe"
        APP_POOL    = "Student Management System using Flask"
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

                    "%VENV%\\Scripts\\python.exe" -m pip install --upgrade pip
                    "%VENV%\\Scripts\\python.exe" -m pip install -r requirements.txt
                    "%VENV%\\Scripts\\python.exe" -m pip install pytest==7.4.2
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    powershell -NoProfile -ExecutionPolicy Bypass -Command "$tests = Get-ChildItem -Path . -Recurse -File -Filter 'test_*.py' | Where-Object { $_.FullName -notmatch '(\\.venv|\\.git)' }; if ($tests) { & '.\\.venv\\Scripts\\python.exe' -m pytest --maxfail=1 --disable-warnings; exit $LASTEXITCODE } else { Write-Host 'No test files found. Skipping tests.' }"
                '''
            }
        }

        stage('Deploy to IIS') {
            steps {
                echo "Copying Flask project files to IIS..."
                bat '''
                    if not exist "%DEPLOY_PATH%" mkdir "%DEPLOY_PATH%"

                    :: Robocopy files excluding venv, git, and test/cache folders
                    :: Robocopy returns exit codes 0-7 on success; anything > 7 is an error
                    robocopy . "%DEPLOY_PATH%" /E /XD .venv venv .git __pycache__ .pytest_cache /XF Jenkinsfile *.log
                    if %ERRORLEVEL% LEQ 7 (exit /b 0) else (exit /b %ERRORLEVEL%)
                '''

                echo "Recycling IIS Application Pool..."
                bat '''
                    %windir%\\system32\\inetsrv\\appcmd.exe recycle apppool /apppool.name:"%APP_POOL%"
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful for '${env.APP_NAME}'!"
            echo "Application available at IIS site mapped to '${env.APP_POOL}'."
        }
        failure {
            echo "❌ Pipeline failed for '${env.APP_NAME}'. Check the console logs above."
        }
    }
}
