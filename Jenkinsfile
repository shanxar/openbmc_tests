pipeline {
    agent any

    /*
     * These values are entered when starting a Jenkins build.
     */
    parameters {

        string(
            name: 'BMC_HOST',
            defaultValue: '',
            description: 'BMC hostname/IP and port, e.g. 127.0.0.1:2443'
        )

        string(
            name: 'BMC_USERNAME',
            defaultValue: '',
            description: 'BMC username'
        )

        password(
            name: 'BMC_PASSWORD',
            defaultValue: '',
            description: 'BMC password'
        )

        choice(
            name: 'TEST_MARKER',
            choices: [
                'smoke',
                'redfish',
                'ipmi',
                'reboot',
                'all'
            ],
            description: 'Select which pytest test group to execute'
        )
    }

    /*
     * General Jenkins pipeline options.
     */
    options {

        // Show timestamps in Jenkins console output
        timestamps()

        // Stop the build if it runs longer than 15 minutes
        timeout(
            time: 15,
            unit: 'MINUTES'
        )
    }

    stages {

        /*
         * Jenkins checks out the repository configured
         * in the Jenkins job.
         */
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        /*
         * Make sure the required BMC parameters were entered.
         */
        stage('Validate Parameters') {
            steps {
                sh '''
                    set -e

                    if [ -z "$BMC_HOST" ]; then
                        echo "ERROR: BMC_HOST is required"
                        exit 1
                    fi

                    if [ -z "$BMC_USERNAME" ]; then
                        echo "ERROR: BMC_USERNAME is required"
                        exit 1
                    fi

                    if [ -z "$BMC_PASSWORD" ]; then
                        echo "ERROR: BMC_PASSWORD is required"
                        exit 1
                    fi

                    echo "BMC parameters are present."
                    echo "BMC_HOST: $BMC_HOST"
                    echo "BMC_USERNAME: $BMC_USERNAME"
                '''
            }
        }

        /*
         * Create Python virtual environment and install
         * the dependencies required by the project.
         */
        stage('Setup Python Environment') {
            steps {
                sh '''
                    set -e

                    echo "Creating Python virtual environment..."

                    python3 -m venv .venv

                    echo "Upgrading pip..."

                    .venv/bin/python -m pip install --upgrade pip

                    echo "Installing project dependencies..."

                    .venv/bin/python -m pip install -r requirements.txt

                    echo "Creating report and log directories..."

                    mkdir -p reports
                    mkdir -p logs
                '''
            }
        }

        /*
         * Run the pytest tests selected by TEST_MARKER.
         *
         * The actual HTML and JUnit report options are defined
         * in pytest.ini.
         */
        stage('Run Tests') {
            steps {
                sh '''
                    set +e

                    echo "Selected test marker: $TEST_MARKER"

                    if [ "$TEST_MARKER" = "all" ]; then

                        echo "Running all pytest tests..."

                        .venv/bin/python -m pytest

                    else

                        echo "Running pytest marker: $TEST_MARKER"

                        .venv/bin/python -m pytest -m "$TEST_MARKER"

                    fi

                    TEST_EXIT_CODE=$?

                    echo "Pytest exit code: $TEST_EXIT_CODE"

                    exit $TEST_EXIT_CODE
                '''
            }
        }
    }

    /*
     * These steps run after the pipeline finishes,
     * whether the tests pass or fail.
     */
    post {

        always {

            /*
             * Publish JUnit XML results.
             *
             * Jenkins will display:
             * - passed tests
             * - failed tests
             * - skipped tests
             * - test trends
             */
            junit(
                testResults: 'reports/junit.xml',
                allowEmptyResults: true
            )

            /*
             * Keep the report files as downloadable Jenkins artifacts.
             */
            archiveArtifacts(
                artifacts: 'reports/**,logs/**',
                allowEmptyArchive: true
            )

            /*
             * Publish the HTML report inside Jenkins.
             */
            publishHTML(
                target: [
                    reportName: 'OpenBMC Pytest HTML Report',
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    keepAll: true,
                    alwaysLinkToLastBuild: true,
                    allowMissing: true
                ]
            )
        }
    }
}