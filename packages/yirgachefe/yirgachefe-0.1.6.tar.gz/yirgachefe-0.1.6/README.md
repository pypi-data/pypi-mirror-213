# Yirgachefe
A library for the convenience of configuring environment variables, configuration files, and logger.

## Prerequisite
- Python 3.9.x or higher

## Quick start
The configuration file format is JSON, and the default location is [CWD]/configure.json.
* CWD: Current working directory (you can get it with 'os.getcwd()')

### Example configure.json
```json
{
  "API_PORT": 8100,
  "STORAGE_ID": "storage_1"
}
```

### Example Code
```python
from yirgachefe import config, logger

logger.debug(config['API_PORT'])
logger.info(config.API_PORT)

config['NEW'] = 'new value'
config.NEW2 = 'new value2'
```

## Custom Usage

### Default configure.json.
* This value is set internally and is used even if the file doesn't exist.
* You can use the changed value by explicitly setting it in the file.
```json
{
  "debug": true,
  "log_level": "DEBUG",
  "log_format": "%(asctime)s,%(msecs)03d %(process)d %(thread)d %(levelname)s %(filename)s(%(lineno)d) %(message)s",
  "log_path": "Yirgachefe.log",
  "log_when": "d",
  "log_interval": 1,
  "log_backup_count": 5
}
```
* debug: Set stream handler to logging with coloredlog.
* log_level: Log level for logging.
* log_format: Log format for logging.
* log_path: Write a file log if present (optional)

### Optional configuration for RotatingFileHandler.
* yirgachefe supports time-based log file rotating.
* Each option is as follows.
* Rotating works when all values are present.
```json
{
  "log_when": "d",
  "log_interval": 1,
  "log_backup_count": 10
}
```
* log_when: rotating unit s | m | h | d | w0-w6 (see. 'logging.handler')
* log_interval: rotating period
* log_backup_count: log backup count.

### Make and Save configure.json
* After creating an empty config class, you can set the config value and save it as a file.

```python
from yirgachefe import Config

config = Config()
config.NEW = 'new value'
config.write_config()
```
