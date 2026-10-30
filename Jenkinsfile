pipeline {
    agent any

    environment {
        APP_NAME = "Student Management System using Flask"
        DEPLOY_PATH = "C:\inetpub\wwwroot\Student Management System using Flask"
        VENV = "venv"
        PYTHON = "C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python310\\python.exe"
    }

    stages {

        stage('Setup Virtual Environment') {
            steps {
                // Create virtual environment
                bat """
                    if not exist %VENV% (
                        %PYTHON% -m venv %VENV%
                    )
                """

                // Upgrade pip
                bat "%VENV%\\Scripts\\python -m pip install --upgrade pip"

                // Install requirements including pytest
                bat "%VENV%\\Scripts\\pip install -r requirements.txt"
                bat "%VENV%\\Scripts\\pip install pytest==7.4.2"
            }
        }

        stage('Run Tests') {
            steps {
                // Run pytest and ensure failures break pipeline
                bat """
                    %VENV%\\Scripts\\python -m pytest --maxfail=1 --disable-warnings
                """
            }
        }

        stage('Deploy to IIS') {
            steps {
                echo "Restarting IIS App Pool..."
                bat "powershell Restart-WebAppPool -Name 'Student Management System using Flask'"

                echo "Copying files..."
                bat '''
        xcopy /E /I /Y * "C:\\inetpub\\wwwroot\\Student Management System using Flask\\"          
        '''
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful! URL: http://localhost:8085/"
        }
        failure {
            echo "❌ Pipeline failed. Check logs."
        }
    }
}

