pipeline {
    agent any

    environment {
        // Kiwi TCMS – nazwa usługi w Docker Compose
        TCMS_URL   = "https://kiwi_web:8443"
        TCMS_PLAN  = "1"
        // Używamy numeru bieżącego builda w Jenkins
        TCMS_BUILD = "${env.BUILD_NUMBER}"
        // Poświadczenia do Kiwi (zdefiniowane w Jenkins → Credentials → ID: kiwi-credentials)
        TCMS_CRED  = credentials('KIWI_TESTER')
    }

    stages {
        stage('Checkout') {
            steps {
                // Pobieramy z Jenkins Credentials:
                // GIT_USER = "oauth2", GIT_TOKEN = (Twój PAT)
                withCredentials([usernamePassword(
                    credentialsId: 'GIT',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_TOKEN'
                )]) {
                    // Czyścimy workspace, żeby móc klonować do "."
                    deleteDir()

                    // Klonujemy repo za pomocą oauth2:TOKEN
                    sh '''
                        git clone https://${GIT_USER}:${GIT_TOKEN}@git.e-science.pl/micbla4466_dpp_2025/hex_ci.git .
                    '''
                }
            }
        }


        stage('Install dependencies') {
            steps {
                sh '''
                    # Jeżeli trzeba wejść do katalogu projektu (jeśli powstał subfolder hex_ci)
                    # cd hex_ci

                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run tests and send to Kiwi') {
            steps {
                sh '''
                    # cd hex_ci   # odkomentuj, jeśli wciąż w podfolderze

                    . venv/bin/activate

                    # Rozbijamy login:password z TCMS_CRED (dostaliśmy je w environment)
                    IFS=":" read -r TCMS_USER TCMS_PASSWORD <<< "${TCMS_CRED}"

                    # Uruchamiamy pytest z wtyczką Kiwi TCMS
                    pytest web_tests \
                        --tcms-url=${TCMS_URL} \
                        --tcms-plan=${TCMS_PLAN} \
                        --tcms-build=${TCMS_BUILD} \
                        --tcms-user=${TCMS_USER} \
                        --tcms-password=${TCMS_PASSWORD} \
                        --tcms-insecure
                '''
            }
            post {
                always {
                    // Zbieramy ewentualne raporty JUnit (jeśli generujesz)
                    junit 'web_tests/**/*.xml'
                }
            }
        }
    }

    post {
        success {
            echo '✅ Testy zakończone sukcesem. Wyniki zostały przesłane do Kiwi TCMS.'
        }
        failure {
            echo '❌ Przynajmniej jeden test nie przeszedł. Wyniki zostały przesłane do Kiwi TCMS (status Fail).'
        }
    }
}
