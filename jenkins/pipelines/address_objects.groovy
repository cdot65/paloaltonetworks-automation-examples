pipeline {
    agent {
        kubernetes {
            label 'dynamic-agent'
            defaultContainer 'jnlp'
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: jenkins-agent
spec:
  serviceAccountName: jenkins-agent-sa
  containers:
    - name: jnlp
      image: ghcr.io/cdot65/jenkins-kubectl:latest
      resources:
        requests:
          cpu: "500m"
          memory: "512Mi"
        limits:
          cpu: "1"
          memory: "1024Mi"
      volumeMounts:
        - name: workspace-volume
          mountPath: /home/jenkins/agent
    - name: python
      image: ghcr.io/cdot65/pan-os-docker:python
      command:
        - cat
      tty: true
      workingDir: /home/jenkins/agent
      volumeMounts:
        - name: workspace-volume
          mountPath: /home/jenkins/agent
  volumes:
    - name: workspace-volume
      emptyDir: {}
"""
        }
    }
    parameters {
        string(name: 'HOSTNAME', defaultValue: 'panorama1.cdot.io', description: 'Panorama password')
        string(name: 'USERNAME', defaultValue: 'officehours', description: 'Panorama username')
        string(name: 'PASSWORD', defaultValue: 'paloalto123', description: 'Panorama password')
        string(name: 'DEVICE_GROUP', defaultValue: '', description: 'Panorama device group')
        string(name: 'ADDRESS_NAME', defaultValue: '', description: 'Address object name')
        string(name: 'ADDRESS_TYPE', defaultValue: '', description: 'Address object type')
        string(name: 'ADDRESS_VALUE', defaultValue: '', description: 'Address object value')
        string(name: 'ADDRESS_DESCRIPTION', defaultValue: '', description: 'Address description')
        string(name: 'ADDRESS_TAGS', defaultValue: '', description: 'Address tags')
    }
    environment {
        NAMESPACE = "jenkins-pipeline-${env.BUILD_NUMBER}"
    }
    stages {
        stage('Setup Workspace') {
            steps {
                container('jnlp') {
                    script {
                        sh '''
                            git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
                        '''
                    }
                }
            }
        }
        stage('Run Python Script') {
            steps {
                container('python') {
                    script {
                        sh """
                            cd paloaltonetworks-automation-examples/python/pan-os-configure-security-policies
                            string(name: 'HOSTNAME', defaultValue: 'panorama1.cdot.io', description: 'Panorama password')
                            string(name: 'USERNAME', defaultValue: 'officehours', description: 'Panorama username')
                            string(name: 'PASSWORD', defaultValue: 'paloalto123', description: 'Panorama password')
                            string(name: 'DEVICE_GROUP', defaultValue: '', description: 'Panorama device group')
                            string(name: 'ADDRESS_NAME', defaultValue: '', description: 'Address object name')
                            string(name: 'ADDRESS_TYPE', defaultValue: '', description: 'Address object type')
                            string(name: 'ADDRESS_VALUE', defaultValue: '', description: 'Address object value')
                            string(name: 'ADDRESS_DESCRIPTION', defaultValue: '', description: 'Address description')
                            string(name: 'ADDRESS_TAGS', defaultValue: '', description: 'Address tags')

                            PARAM_HOSTNAME="--hostname '${HOSTNAME}'"
                            PARAM_USERNAME="--username '${USERNAME}'"
                            PARAM_PASSWORD="--password '${PASSWORD}'"
                            PARAM_DEVICE_GROUP="--device-group '${DEVICE_GROUP}'"
                            PARAM_ADDRESS_NAME="--address-name '${ADDRESS_NAME}'"
                            PARAM_ADDRESS_TYPE="--address-type '${ADDRESS_TYPE}'"
                            PARAM_ADDRESS_TAGS="--address-tags '${ADDRESS_TAGS}'"
                            PARAM_ADDRESS_VALUE="--address-value '${ADDRESS_VALUE}'"
                            PARAM_ADDRESS_DESCRIPTION="--address-description '${ADDRESS_DESCRIPTION}'"

                            python3 app.py \\
                                \$PARAM_HOSTNAME \\
                                \$PARAM_USERNAME \\
                                \$PARAM_PASSWORD \\
                                \$PARAM_DEVICE_GROUP \\
                                \$PARAM_ADDRESS_NAME \\
                                \$PARAM_ADDRESS_TYPE \\
                                \$PARAM_ADDRESS_TAGS \\
                                \$PARAM_ADDRESS_VALUE \\
                                \$PARAM_ADDRESS_DESCRIPTION > output.json
                        """
                        // Read the output JSON
                        def jsonOutput = readFile('paloaltonetworks-automation-examples/python/pan-os-configure-security-policies/output.json').trim()
                        // Parse the JSON
                        def json = readJSON text: jsonOutput
                        // Use the JSON object as needed
                        echo "Script Output: ${json}"
                    }
                }
            }
        }
        // Include previous stages like 'Setup Namespace' and 'Run Workload' if needed
    }
    post {
        always {
            script {
                // Cleanup resources if applicable
                sh "kubectl delete namespace ${NAMESPACE} || true"
            }
        }
    }
}
