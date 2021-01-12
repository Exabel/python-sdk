#!/usr/bin/env/groovy

// Make sure this build gets a unique label
String label = "buildpod.${env.JOB_NAME}.${env.BUILD_NUMBER}".replaceAll(/[^\w-]/, '_')

// Sets special branch locations
String officialMaster = 'git@github.com:Exabel/python-sdk.git:master'

// Build levels
BUILD_NONE = 0    // Build nothing -- assuming no code changes
BUILD_PUBLISH = 1 // Build only what's needed to publish maven artifacts
BUILD_ALL = 2     // Build, test and publish everything

// List of files that do not contain any code
Collection<String> fileRegexNoCode = [/.*[.]md/, /LICENSE/]

// Returns a list of changed files since the previous successful build.
Collection<String> getChangedFilesList() {
  Collection<String> files = new HashSet()
  def build = currentBuild
  while (build != null && build.result != 'SUCCESS') {
    files.addAll(
      build.getChangeSets().collectMany { it.collectMany { it.getAffectedFiles().collect { it.getPath() }}})
    build = build.previousBuild
  }
  if (build != null) {
    echo "Previous successful build: $build.displayName"
    return files
  }

  echo 'No previous successful builds'
  if (env.CHANGE_ID) {
    // This is a PR, return the files as reported by GitHub.
    return pullRequest.files.collect { it.filename }
  } else {
    // This is a pure branch build, return something that will build everything.
    return ['__first_build__']
  }
}

podTemplate(label: label, yaml: """
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: jnlp
      env:
      - name: GKE_NODE_NAME
        valueFrom:
          fieldRef:
            fieldPath: spec.nodeName
""",
  containers: [
    containerTemplate(
      name: 'python', image: 'eu.gcr.io/jenkins-exabel/python-build:v6',
      ttyEnabled: true, command: 'cat',

      resourceRequestCpu: '2.5', resourceLimitCpu: '3.5',
      resourceRequestMemory: '6Gi', resourceLimitMemory: '8Gi',
    ),
  ],
  volumes: [
    hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock'),
  ]) {

  node(label) {
    try {
      stage('Checkout') {
        echo "*** Running on node ${env.GKE_NODE_NAME} ***"
        checkout([
                $class           : 'GitSCM',
                branches         : scm.branches,
                extensions       : scm.extensions + [
                        [$class: 'SubmoduleOption', parentCredentials: true, recursiveSubmodules: true],
                        [$class: 'LocalBranch', localBranch: BRANCH_NAME],
                ],
                userRemoteConfigs: scm.userRemoteConfigs
        ])
      }

      stage('Get git environment') {
        gitRemote = sh(returnStdout: true, script: 'git config remote.origin.url').trim()
        gitBranch = BRANCH_NAME
        gitCommit = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
        tagName = (gitBranch + '.' + gitCommit).replaceAll(/[^\w-\.]/, '_')
        ON_MASTER = (gitRemote + ':' + gitBranch == officialMaster)

        changed = getChangedFilesList()
        echo 'Changed files: ' + changed

        if (changed.every { f -> fileRegexNoCode.any { f ==~ it } }) {
          echo 'No code changes -- do not build anything.'
          buildLevel = BUILD_NONE
        } else {
          echo 'Full build.'
          buildLevel = BUILD_ALL
        }
      }

      if (buildLevel >= BUILD_PUBLISH) {
        container('python') {
          stage('Python build and verify') {
            sh 'pip3 install grpcio pandas protobuf'
            sh './build.sh'
          }
        }
      }

      if (!ON_MASTER) {
        notifySlack('#40b59b', 'SUCCESS')
      }
    } catch (org.jenkinsci.plugins.workflow.steps.FlowInterruptedException e) {
      notifySlack('#ffaa00', 'CANCELLED')
      throw e
    } catch (Exception e) {
      notifySlack('#f51767', 'FAILURE')
      throw e
    }
  }
}

String getSlackUser() {
  echo "Finding slack user for: ${env.CHANGE_AUTHOR}"
  echo "Slack user mapping: ${env.SLACK_USER_MAPPING}"
  map = env.SLACK_USER_MAPPING.split(';').collectEntries { entry ->
    def pair = entry.split(':')
    [(pair.first()): pair.last()]
  }
  return map.get(env.CHANGE_AUTHOR)
}

String getChannel() {
  if (ON_MASTER) {
    return '#jenkins-ci'
  }
  return "@${getSlackUser()}"
}

def notifySlack(String color, String message) {
  pull_request_info = env.CHANGE_ID ? "\nPull request: https://github.com/Exabel/python-sdk/pull/${env.CHANGE_ID}" : ''
  slackSend channel: getChannel(),
          color: color,
          message: "${message}: `${env.JOB_NAME}` #${env.BUILD_NUMBER}:\n${env.BUILD_URL}${pull_request_info}"
}
