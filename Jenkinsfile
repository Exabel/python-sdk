#!/usr/bin/env/groovy

// Make sure this build gets a unique label
String label = "buildpod.${env.JOB_NAME}.${env.BUILD_NUMBER}".replaceAll(/[^\w-]/, '_')

// Sets special branch locations
String officialMain = 'git@github.com:Exabel/python-sdk.git:main'

// Build levels
BUILD_NONE = 0    // Build nothing -- assuming no code changes
BUILD_PUBLISH = 1 // Build only what's needed to publish maven artifacts
BUILD_ALL = 2     // Build, test and publish everything

// List of files that do not contain any code
Collection<String> fileRegexNoCode = [/.*[.]md/, /LICENSE/]

// Returns the full list of changed files in the pull request
Collection<String> getAllChangedFilesList() {
  if (env.CHANGE_ID) {
    // This is a PR, return the files as reported by GitHub.
    return pullRequest.files.collect { it.filename }
  } else {
    // This is a pure branch build, return something that will build everything.
    return ['__first_build__']
  }
}

// Returns the list of changed files between the current commit and another commit
Collection<String> getChangedFiles(String commit) {
  return sh(returnStdout: true, script: "git --no-pager diff --name-only $commit").trim().split('\n')
}

// Returns a list of changed files since the previous successful build.
Collection<String> getChangedFilesList() {
  def build = currentBuild.previousSuccessfulBuild
  if (build == null) {
    echo 'No previous successful builds'
    return getAllChangedFilesList()
  }
  echo "Previous successful build: #$build.id"
  def buildData = build.rawBuild.getAction(hudson.plugins.git.util.BuildData.class)
  String commit = buildData.lastBuiltRevision.sha1String
  if (commit == null) {
    echo 'No previous build commit found'
    return getAllChangedFilesList()
  }
  echo "Previous successful commit: $commit"
  if (!env.CHANGE_ID) {
    // This is a pure branch build, just use the diff since the previous
    return getChangedFiles(commit)
  } else {
    // This is a PR, ignore changes in the base branch by doing a temporary merge from the previous success
    if (sh(returnStatus: true, script: "git -c advice.detachedHead=false checkout $commit")) {
      // Checkout failed, was it force pushed?
      return getAllChangedFilesList()
    } else if (sh(returnStatus: true, script: "git merge origin/${pullRequest.base} -m 'Tmp diff commit'")) {
      // Merge failed, just use the diff without merging
      sh "git -c advice.detachedHead=false checkout $gitCommit"
      return getChangedFiles(commit)
    } else {
      // Merge successful. Grab the diff with the actual commit
      def files = getChangedFiles(gitCommit)
      sh "git -c advice.detachedHead=false checkout $gitCommit"
      return files
    }
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
      name: 'jnlp', image: 'eu.gcr.io/jenkins-exabel/jenkins-k8s-slave:v4',
      args: '${computer.jnlpmac} ${computer.name}',
      resourceRequestCpu: '0.1', resourceLimitCpu: '3.0',
      resourceRequestMemory: '150Mi', resourceLimitMemory: '6Gi'
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
        TAG_NAME = "${gitBranch}.${gitCommit}".replaceAll(/[^\w-\.]/, '_')
        ON_MAIN = (gitRemote + ':' + gitBranch == officialMain)

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
        stage('Python build and verify') {
          sh "docker build -t python-sdk-build:${TAG_NAME} ."
          sh "docker run python-sdk-build:${TAG_NAME} pipenv run ./build.sh"
        }
      }

      if (!ON_MAIN) {
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
  if (ON_MAIN) {
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
