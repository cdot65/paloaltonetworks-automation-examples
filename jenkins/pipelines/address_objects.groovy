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
        string(name: 'ADDRESS_TAGS', defaultValue: '', description: 'Address tags')
        string(name: 'ADDRESS_VALUE', defaultValue: '', description: 'Address object value')
        string(name: 'ADDRESS_DESCRIPTION', defaultValue: '', description: 'Address description')
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
                        sh '''
                            cd paloaltonetworks-automation-examples/python/pan-os-configure-security-policies

                            python3 app.py \
                                --hostname "${HOSTNAME}" \
                                --username "${USERNAME}" \
                                --password "${PASSWORD}" \
                                --device-group "${DEVICE_GROUP}" \
                                --address-name "${ADDRESS_NAME}" \
                                --address-type "${ADDRESS_TYPE}" \
                                --address-value "${ADDRESS_VALUE}" \
                                --address-description "${ADDRESS_DESCRIPTION}" \
                                --address-tags ${ADDRESS_TAGS} > output.json
                        '''
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
