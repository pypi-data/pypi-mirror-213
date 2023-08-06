from pathlib import Path
home = str(Path.home())
BP_CONFIG_PATH = home+'/.bp'
BP_CONFIG_PATH_FILE_NAME = 'config'
USER_LOGIN_URI = 'api/v1/user/login/'
USER_LOGOUT_URI = 'api/v1/user/logout/'
BP_MANIFEST_APPLY_URI = 'api/v1/bp/manifest/'
BP_YAML = 'bp.yaml'
BP_YML = 'bp.yml'
# error messages
INVALID_FILETYPE_MSG = "Error: Invalid file format. %s must be bp.yaml or bp.yml file."
INVALID_PATH_MSG = "Error: Invalid file path/name. Path %s does not exist."
