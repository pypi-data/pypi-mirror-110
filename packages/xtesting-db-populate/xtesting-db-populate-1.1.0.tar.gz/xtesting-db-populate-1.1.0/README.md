# xtesting-db-populate

Script to populate xtesting-db with project, tests cases and pods.

This application read local xtesting files and variables to populate
test databases.

## Requirements

To create projects and populate tests cases, `testcases.yaml` file
is **Mandatory**

To get the testapi url, the **Mandatory** variable `TEST_DB_URL` must
be set with the value of the test api url
(`https://testapi.test/api/v1/`)

To set pods, **One of** the two must be set:

- an environment variable `NODE_NAME` must be set to the pod value
(`pod1`)
- a file `pods.yaml` that should be like:
  ```yaml
  ---
  pods:
    - pod1
    - pod2
  ```

## Usage

```bash
 !  ~/D/v/a/v/xtesting_project   testing-db-populate
🎯 get testapi url [success]
📤 read pods.yaml [success]
🤖 populate pod "pod1" [skipped]
🤖 populate pod "pod2" [skipped]
📤 read testcases.yaml [success]
📦 populate project "project1" [skipped]
📋 populate case "test 1" [skipped]
📋 populate case "test 2" [skipped]
📋 populate case "test 3" [skipped]
📋 populate case "test 4" [skipped]
```
