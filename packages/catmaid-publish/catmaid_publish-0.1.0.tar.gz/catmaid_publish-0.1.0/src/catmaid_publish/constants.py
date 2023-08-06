import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


PROJECT_DIR = Path(__file__).parent.parent.parent

data_var_name = "CATMAID_PUBLISH_DATA"

data_dir_env = os.environ.get(data_var_name)
if data_dir_env is None:
    DATA_DIR = PROJECT_DIR / "data"
else:
    DATA_DIR = Path(data_dir_env)
    logger.info("DATA_DIR set to %s based on %s variable", DATA_DIR, data_var_name)

CREDENTIALS_DIR = PROJECT_DIR / "credentials"

CACHE_SIZE = 1024
README_FOOTER_KEY = "readme_footer"
