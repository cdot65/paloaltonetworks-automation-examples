pipeline {
    agent {
        kubernetes {
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
      imagePullPolicy: Always
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
        string(name: 'HOSTNAME', defaultValue: 'panorama1.cdot.io', description: 'Panorama hostname')
        string(name: 'USERNAME', defaultValue: 'officehours', description: 'Panorama username')
        password(name: 'PASSWORD', defaultValue: 'paloalto123', description: 'Panorama password')
        string(name: 'DEVICE_GROUP', defaultValue: '', description: 'Panorama device group')
        string(name: 'SEC_RULE_NAME', defaultValue: '', description: 'Name of the security rule')
        string(name: 'SEC_RULE_DESCRIPTION', defaultValue: '', description: 'Description of the security rule')
        string(name: 'SEC_RULE_TAG', defaultValue: '', description: 'Tags, comma seperated list')
        string(name: 'SEC_RULE_DISABLED', defaultValue: '', description: 'Set the policy as disabled')
        string(name: 'SEC_RULE_FROM_ZONE', defaultValue: '', description: 'Source security zone, comma seperated list')
        string(name: 'SEC_RULE_TO_ZONE', defaultValue: '', description: 'Destination security zone, comma seperated list')
        string(name: 'SEC_RULE_SOURCE', defaultValue: '', description: 'Source addresses, comma seperated list')
        string(name: 'SEC_RULE_DESTINATION', defaultValue: '', description: 'Destination address, comma seperated list')
        string(name: 'SEC_RULE_APPLICATION', defaultValue: '', description: 'App-ID, comma seperated list')
        string(name: 'SEC_RULE_SERVICE', defaultValue: '', description: 'TCP/UDP services, comma seperated list')
        string(name: 'SEC_RULE_CATEGORY', defaultValue: '', description: 'URL Categories, comma seperated list')
        string(name: 'SEC_RULE_SECURITY_PROFILE_GROUP', defaultValue: '', description: 'Security profile group associated to rule')
        string(name: 'SEC_RULE_LOG_SETTING', defaultValue: '', description: 'Log forwarding profile')
        string(name: 'SEC_RULE_ACTION', defaultValue: '', description: 'Allow, Deny, Drop, Reset Both, Reset Client, Reset Server')
    }
    stages {
        stage('Setup Workspace') {
            steps {
                container('jnlp') {
                    sh '''
                        git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
                    '''
                }
            }
        }
        stage('Run Python Script') {
            steps {
                container('python') {
                    script {
                        sh '''
                            cd paloaltonetworks-automation-examples/python/pan-os-configure-security-policies

                            set -e
                            python3 app.py \
                                --hostname "${HOSTNAME}" \
                                --username "${USERNAME}" \
                                --password "${PASSWORD}" \
                                --device-group "${DEVICE_GROUP}" \
                                --rule-name "${SEC_RULE_NAME}" \
                                --rule-description "${SEC_RULE_DESCRIPTION}" \
                                --rule-tag "${SEC_RULE_TAG}" \
                                --rule-disabled "${SEC_RULE_DISABLED}" \
                                --rule-from-zone "${SEC_RULE_FROM_ZONE}" \
                                --rule-to-zone "${SEC_RULE_TO_ZONE}" \
                                --rule-source "${SEC_RULE_SOURCE}" \
                                --rule-destination "${SEC_RULE_DESTINATION}" \
                                --rule-application "${SEC_RULE_APPLICATION}" \
                                --rule-service "${SEC_RULE_SERVICE}" \
                                --rule-category "${SEC_RULE_CATEGORY}" \
                                --rule-security-profile-group "${SEC_RULE_SECURITY_PROFILE_GROUP}" \
                                --rule-log-setting "${SEC_RULE_LOG_SETTING}" \
                                --rule-action ${SEC_RULE_ACTION} > output.json
                        '''
                        try {
                            // Read the output JSON
                            def jsonOutput = readFile('paloaltonetworks-automation-examples/python/pan-os-configure-security-policies/output.json').trim()
                            // Parse the JSON
                            def json = readJSON text: jsonOutput
                            // Use the JSON object as needed
                            echo "Script Output: ${json}"
                        } catch (Exception e) {
                            echo "Failed to parse JSON output: ${e}"
                            currentBuild.result = 'FAILURE'
                            error("Pipeline aborted due to JSON parsing error.")
                        }
                    }
                }
            }
        }
    }
}
