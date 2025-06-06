pipeline {
    agent any

    environment {
        // Zakładamy, że w Jenkinsie w sekcji „Credentials” mamy dwa wpisy:
        // ID: kiwi-credentials, typu „Username with password”
        // w ten sposób możemy w prosty sposób pobrać zarówno TCMS_USER, jak i TCMS_PASSWORD
        TCMS_URL      = "https://localhost:8443"
        TCMS_PLAN     = "1"
        TCMS_BUILD    = "2"
        TCMS_CRED     = credentials('KIWI_TESTER')
    }

    stages {
        stage('Checkout') {
            steps {
                // Pobierz kod z repozytorium (np. Git)
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
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
                    # Aktywuj wirtualne środowisko
                    . venv/bin/activate

                    # Pobranie TCMS_USER/TCMS_PASSWORD:
                    # Jenkins rozdziela po „colon” wartości z credentials->username:password
                    IFS=":" read -r TCMS_USER TCMS_PASSWORD <<< "${TCMS_CRED}"

                    # Uruchomienie pytest z wtyczką Kiwi. Wyniki wysłane do Kiwi
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
                    // Możemy zebrać artefakty, np. logi czy raporty JUnit,
                    // chociaż główną informacją jest to, że wyniki poszły do Kiwi
                    junit 'web_tests/**/*.xml' // jeśli generujemy raport JUnit
                }
            }
        }
    }

    post {
        success {
            echo 'Testy zostały uruchomione i wyniki przesłane do Kiwi TCMS.'
        }
        failure {
            echo 'Przynajmniej jeden test nie przeszedł. Wyniki również zostały przesłane do Kiwi TCMS (status Fail).'
        }
    }
}
