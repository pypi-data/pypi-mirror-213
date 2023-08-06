from pathlib import Path
import shutil

lollms_path = Path(__file__).parent
lollms_default_cfg_path = lollms_path / "configs/config.yaml"
lollms_bindings_zoo_path = lollms_path/"bindings_zoo"
lollms_personalities_zoo_path = lollms_path/"personalities_zoo"


lollms_personal_path = Path.home()/"Documents/lollms"
lollms_personal_configuration_path = Path.home()/"Documents/lollms/configs"
lollms_personal_models_path = Path.home()/"Documents/lollms/models"

lollms_personal_path.mkdir(parents=True, exist_ok=True)
lollms_personal_configuration_path.mkdir(parents=True, exist_ok=True)
lollms_personal_models_path.mkdir(parents=True, exist_ok=True)

if not(lollms_personal_configuration_path/"local_config.yaml").exists():
    shutil.copy(lollms_path / "configs/config.yaml", str(lollms_personal_configuration_path/"local_config.yaml"))
