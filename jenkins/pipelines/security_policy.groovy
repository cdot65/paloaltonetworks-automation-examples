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
        choice(name: 'DEVICE_GROUP', choices: ['shared', 'Magnolia-Proxmox', 'Magnolia-Edge', 'Dallas'], description: 'Panorama device group')
        string(name: 'SEC_RULE_NAME', defaultValue: '', description: 'Name of the security rule')
        string(name: 'SEC_RULE_DESCRIPTION', defaultValue: '', description: 'Description of the security rule')
        string(name: 'SEC_RULE_TAG', defaultValue: 'Jenkins', description: 'Tags, space-separated list')
        booleanParam(name: 'SEC_RULE_DISABLED', defaultValue: false, description: 'Set the policy as disabled')
        string(name: 'SEC_RULE_FROM_ZONE', defaultValue: 'any', description: 'Source security zone(s), space-separated list')
        string(name: 'SEC_RULE_TO_ZONE', defaultValue: 'any', description: 'Destination security zone, space-separated list')
        string(name: 'SEC_RULE_SOURCE', defaultValue: 'any', description: 'Source addresses, space-separated list')
        string(name: 'SEC_RULE_DESTINATION', defaultValue: 'any', description: 'Destination addresses, space-separated list')
        string(name: 'SEC_RULE_APPLICATION', defaultValue: 'any', description: 'App-ID, space-separated list')
        string(name: 'SEC_RULE_SERVICE', defaultValue: 'any', description: 'TCP/UDP services, space-separated list')
        string(name: 'SEC_RULE_CATEGORY', defaultValue: 'any', description: 'URL Categories, space-separated list')
        string(name: 'SEC_RULE_SECURITY_PROFILE_GROUP', defaultValue: '', description: 'Security profile group associated to rule')
        string(name: 'SEC_RULE_LOG_SETTING', defaultValue: '', description: 'Log forwarding profile')
        choice(name: 'SEC_RULE_ACTION', choices: ['allow', 'deny', 'drop', 'reset-both', 'reset-client', 'reset-server'], description: 'Action for the rule')
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
                        def ruleDisabledFlag = SEC_RULE_DISABLED ? '--rule-disabled' : ''
                        sh '''
                            cd paloaltonetworks-automation-examples/python/pan-os-configure-security-policies

                            set -e
                            python3 app.py \
                                --hostname "$HOSTNAME" \
                                --username "$USERNAME" \
                                --password "$PASSWORD" \
                                --device-group "$DEVICE_GROUP" \
                                --rule-name "$SEC_RULE_NAME" \
                                --rule-description "$SEC_RULE_DESCRIPTION" \
                                --rule-tag $SEC_RULE_TAG \
                                ${ruleDisabledFlag} \
                                --rule-from-zone $SEC_RULE_FROM_ZONE \
                                --rule-to-zone $SEC_RULE_TO_ZONE \
                                --rule-source $SEC_RULE_SOURCE \
                                --rule-destination $SEC_RULE_DESTINATION \
                                --rule-application $SEC_RULE_APPLICATION \
                                --rule-service $SEC_RULE_SERVICE \
                                --rule-category $SEC_RULE_CATEGORY \
                                --rule-security-profile-group "$SEC_RULE_SECURITY_PROFILE_GROUP" \
                                --rule-log-setting "$SEC_RULE_LOG_SETTING" \
                                --rule-action "$SEC_RULE_ACTION" > output.json
                        '''

                        try {
                            def jsonOutput = readFile('paloaltonetworks-automation-examples/python/pan-os-configure-security-policies/output.json').trim()
                            def json = readJSON text: jsonOutput
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
