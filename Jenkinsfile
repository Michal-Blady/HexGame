pipeline {
    agent any

    environment {
        KIWI_URL      = 'https://host.docker.internal:8443'
        KIWI_PLAN_ID  = '1'
        KIWI_BUILD_ID = '2'
        WORKDIR       = '/workspace'  // to jest C:/Users/Michał/Desktop/DPP/lab07/HEX
    }

    stages {
        stage('Install Python & Git (jednorazowo)') {
            steps {
                sh '''
                   # jeśli brakuje python3 lub git – doinstaluj
                   command -v python3 >/dev/null 2>&1 || NEED_PKGS=1
                   command -v git      >/dev/null 2>&1 || NEED_PKGS=1

                   if [ "$NEED_PKGS" = "1" ]; then
                       echo '>>> Instaluję python3, venv, pip i git w kontenerze Jenkinsa'
                       apt-get update -qq
                       DEBIAN_FRONTEND=noninteractive \
                       apt-get install -y python3 python3-venv python3-pip git
                   fi
                '''
            }
        }

        stage('Run pytest → Kiwi') {
            steps {
                dir("${WORKDIR}") {
                    withCredentials([usernamePassword(
                        credentialsId: 'KIWI_TESTER',
                        usernameVariable: 'KIWI_USER',
                        passwordVariable: 'KIWI_PASS')]) {

                        sh '''
                          # Utwórz i aktywuj venv
                          python3 -m venv venv
                          . venv/bin/activate

                          # Zaktualizuj pip
                          pip install -q --upgrade pip

                          # Zainstaluj klienta API Kiwi TCMS
                          pip install -q tcms-api

                          # Ręcznie sklonuj plugin pytest-tcms z GitHuba
                          rm -rf pytest-tcms
                          git clone https://github.com/kiwitcms/pytest-tcms.git pytest-tcms

                          # Zainstaluj lokalnie plugin do aktywnego venv
                          pip install -q pytest-tcms

                          # Teraz zainstaluj resztę zależności projektu
                          pip install -q -r requirements.txt

                          # Utwórz folder na raporty
                          mkdir -p reports

                          # Uruchom pytest z argumentami dla Kiwi TCMS
                          pytest web_tests \
                             --junitxml=reports/junit.xml \
                             --tcms-url=$KIWI_URL \
                             --tcms-plan=$KIWI_PLAN_ID \
                             --tcms-build=$KIWI_BUILD_ID \
                             --tcms-user=$KIWI_USER \
                             --tcms-password=$KIWI_PASS \
                             --tcms-insecure
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            // Wczytaj raport JUnit (albo zignoruj, jeśli go nie ma)
            junit allowEmptyResults: true, testResults: 'reports/junit.xml'
        }
    }
}
