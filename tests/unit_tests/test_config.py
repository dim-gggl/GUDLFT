import pytest
import os
from config import Config, config
from unittest.mock import patch


########################################################
# CONFIG TESTS
########################################################

class TestConfig:
    """Unit tests for the configuration"""
    
    def test_default_secret_key(self):
        """Test the default secret key"""
        config_obj = Config()
        assert config_obj.SECRET_KEY == 'something_special'
    
    def test_custom_secret_key_from_env(self):
        """Test the secret key from environment variables"""
        with patch.dict(os.environ, {'SECRET_KEY': 'custom_secret_key'}):
            config_obj = Config()
            assert config_obj.SECRET_KEY == 'custom_secret_key'
    
    def test_debug_default(self):
        """Test the default debug mode"""
        config_obj = Config()
        assert config_obj.DEBUG is True
    
    def test_debug_from_env_false(self):
        """Test the debug mode from environment variables (false)"""
        with patch.dict(os.environ, {'FLASK_DEBUG': '0'}):
            config_obj = Config()
            assert config_obj.DEBUG is False
    
    def test_debug_from_env_true(self):
        """Test the debug mode from environment variables (true)"""
        with patch.dict(os.environ, {'FLASK_DEBUG': '1'}):
            config_obj = Config()
            assert config_obj.DEBUG is True
    
    def test_run_port_default(self):
        """Test the default port"""
        config_obj = Config()
        assert config_obj.RUN_PORT == '5000'
    
    def test_run_port_from_env(self):
        """Test the port from environment variables"""
        with patch.dict(os.environ, {'FLASK_RUN_PORT': '8080'}):
            config_obj = Config()
            assert config_obj.RUN_PORT == '8080'
    
    def test_testing_default(self):
        """Test the default testing mode"""
        config_obj = Config()
        assert config_obj.TESTING is False


class TestConfigDict:
    """Unit tests for the configuration dictionary"""
    
    def test_config_structure(self):
        """Test the structure of the configuration dictionary"""
        assert "default" in config
        assert isinstance(config["default"], type(Config))
    
    def test_config_default_is_config_class(self):
        """Test that the default configuration is the Config class"""
        assert config["default"] == Config