# Endpoints

## projects
ENDPOINT_URL_PROJECTS = "/api/nemo-projects/projects"
ENDPOINT_URL_PROJECT_PROPERTIES = "/api/nemo-persistence/ProjectProperty/{request}"
ENDPOINT_URL_PROJECT_FILE_RE_UPLOAD_INITIALIZE = "/api/nemo-projects/file-re-upload/initialize"
ENDPOINT_URL_PROJECT_FILE_RE_UPLOAD_KEEP_ALIVE = "/api/nemo-projects/projects/{projectId}/upload/{uploadId}/keep-alive"
ENDPOINT_URL_PROJECT_FILE_RE_UPLOAD_FINALIZE ="/api/nemo-projects/file-re-upload/finalize"
ENDPOINT_URL_PROJECT_FILE_RE_UPLOAD_ABORT = "/api/nemo-projects/file-re-upload/abort"

## reports
ENDPOINT_URL_REPORT_RESULT = "/api/nemo-report/report_results"

FILE_UPLOAD_CHUNK_SIZE = 5 * 1024 * 1024  # 5MB
