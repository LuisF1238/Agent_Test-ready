"""
Configuration Management Module

Handles system configuration, settings, and environment variables.
"""

import os
import yaml
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, fields


@dataclass
class SystemConfig:
    """System configuration data class"""
    # API Configuration
    openai_api_key: Optional[str] = None
    openai_base_url: Optional[str] = None
    
    # Logging Configuration
    log_level: str = "INFO"
    log_file: str = "agent_system.log"
    
    # Session Configuration
    session_persistence: bool = True
    session_db_path: str = "sessions.db"
    
    # Tracing Configuration
    enable_tracing: bool = True
    trace_file: str = "logs/agent_trace.jsonl"
    
    # Agent Configuration
    max_turns: int = 10
    timeout_seconds: int = 120
    
    # Rate Limiting
    rate_limit_requests_per_minute: int = 60
    
    # System Limits
    max_sessions: int = 1000
    session_cleanup_hours: int = 24
    session_cleanup_days: int = 30  # Alternative config name


class ConfigManager:
    """Manages system configuration and settings"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or "config.yaml"
        self.logger = logging.getLogger(__name__)
        self._config = None
        self._initialize_config()
    
    def _initialize_config(self):
        """Initialize configuration from file and environment"""
        # Start with default config
        config_dict = {}
        
        # Load from YAML file if exists
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    file_config = yaml.safe_load(f) or {}
                    config_dict.update(file_config)
                self.logger.info(f"Loaded configuration from {self.config_file}")
            except Exception as e:
                self.logger.warning(f"Could not load config file {self.config_file}: {e}")
        
        # Override with environment variables
        env_overrides = self._get_env_overrides()
        config_dict.update(env_overrides)
        
        # Handle legacy config names
        if 'session_cleanup_days' in config_dict and 'session_cleanup_hours' not in config_dict:
            config_dict['session_cleanup_hours'] = config_dict['session_cleanup_days'] * 24
        
        # Filter out unknown config keys
        valid_keys = {field.name for field in fields(SystemConfig)}
        filtered_dict = {k: v for k, v in config_dict.items() if k in valid_keys}
        
        # Create config object
        self._config = SystemConfig(**filtered_dict)
        
        # Setup logging based on config
        self._setup_logging()
        
        self.logger.info("Configuration manager initialized")
    
    def _get_env_overrides(self) -> Dict[str, Any]:
        """Get configuration overrides from environment variables"""
        env_map = {
            'OPENAI_API_KEY': 'openai_api_key',
            'OPENAI_BASE_URL': 'openai_base_url',
            'LOG_LEVEL': 'log_level',
            'SESSION_DB_PATH': 'session_db_path',
            'ENABLE_TRACING': 'enable_tracing',
            'MAX_TURNS': 'max_turns',
            'TIMEOUT_SECONDS': 'timeout_seconds'
        }
        
        overrides = {}
        for env_var, config_key in env_map.items():
            value = os.getenv(env_var)
            if value is not None:
                # Convert string values to appropriate types
                if config_key in ['enable_tracing']:
                    overrides[config_key] = value.lower() in ('true', '1', 'yes')
                elif config_key in ['max_turns', 'timeout_seconds']:
                    try:
                        overrides[config_key] = int(value)
                    except ValueError:
                        self.logger.warning(f"Invalid integer value for {env_var}: {value}")
                else:
                    overrides[config_key] = value
        
        return overrides
    
    def _setup_logging(self):
        """Setup logging based on configuration"""
        log_level = getattr(logging, self._config.log_level.upper(), logging.INFO)
        
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(self._config.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self._config.log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger.info(f"Logging configured: level={self._config.log_level}, file={self._config.log_file}")
    
    def get_config(self) -> SystemConfig:
        """Get the current configuration"""
        return self._config
    
    def update_config(self, **kwargs):
        """Update configuration values"""
        for key, value in kwargs.items():
            if hasattr(self._config, key):
                setattr(self._config, key, value)
                self.logger.info(f"Updated config: {key} = {value}")
            else:
                self.logger.warning(f"Unknown config key: {key}")
    
    def save_config(self, file_path: Optional[str] = None):
        """Save current configuration to file"""
        save_path = file_path or self.config_file
        
        # Convert config to dictionary
        config_dict = {
            key: value for key, value in self._config.__dict__.items()
            if not key.startswith('_')
        }
        
        try:
            with open(save_path, 'w') as f:
                yaml.dump(config_dict, f, default_flow_style=False)
            self.logger.info(f"Configuration saved to {save_path}")
        except Exception as e:
            self.logger.error(f"Could not save config to {save_path}: {e}")
    
    def validate_config(self) -> bool:
        """Validate current configuration"""
        issues = []
        
        # Check required directories exist
        for path_attr in ['session_db_path', 'trace_file']:
            path = getattr(self._config, path_attr)
            directory = os.path.dirname(path)
            if directory and not os.path.exists(directory):
                try:
                    os.makedirs(directory, exist_ok=True)
                except Exception as e:
                    issues.append(f"Cannot create directory for {path_attr}: {e}")
        
        # Check API key format if provided
        if self._config.openai_api_key and not self._config.openai_api_key.startswith('sk-'):
            issues.append("OpenAI API key should start with 'sk-'")
        
        # Log issues
        for issue in issues:
            self.logger.warning(f"Config validation issue: {issue}")
        
        return len(issues) == 0