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
        with patch.dict(os.environ, {}, clear=True):
            config_obj = Config()
            assert config_obj.SECRET_KEY == 'something_special'
    
    def test_secret_key_is_loaded_from_env(self):
        """Test the secret key from environment variables"""
        with patch.dict(os.environ, {'SECRET_KEY': 'custom_secret_key'}, clear=True):
            config_obj = Config()
            assert config_obj.SECRET_KEY == 'custom_secret_key'
    
    def test_debug_mode_is_default(self):
        """Test the default debug mode"""
        with patch.dict(os.environ, {}, clear=True):
            config_obj = Config()
            assert config_obj.DEBUG is True
    
    def test_debug_mode_with_env_false(self):
        """Test the debug mode from environment variables (false)"""
        with patch.dict(os.environ, {'FLASK_DEBUG': '0'}, clear=True):
            config_obj = Config()
            assert config_obj.DEBUG is False
    
    def test_debug_mode_with_env_true(self):
        """Test the debug mode from environment variables (true)"""
        with patch.dict(os.environ, {'FLASK_DEBUG': '1'}, clear=True):
            config_obj = Config()
            assert config_obj.DEBUG is True
    
    def test_run_port_is_default(self):
        """Test the default port"""
        with patch.dict(os.environ, {}, clear=True):
            config_obj = Config()
            assert config_obj.RUN_PORT == '5000'
    
    def test_run_port_is_loaded_from_env(self):
        """Test the port from environment variables"""
        with patch.dict(os.environ, {'FLASK_RUN_PORT': '8080'}, clear=True):
            config_obj = Config()
            assert config_obj.RUN_PORT == '8080'
    
    def test_testing_mode_is_false_by_default(self):
        """Test the default testing mode"""
        config_obj = Config()
        assert config_obj.TESTING is False


class TestConfigDict:
    """Unit tests for the configuration dictionary"""
    
    def test_config_structure(self):
        """Test the structure of the configuration dictionary"""
        assert "default" in config
        assert hasattr(config["default"], 'SECRET_KEY')
    
    def test_config_default_is_config_instance(self):
        """Test that the default configuration is a Config instance"""
        assert isinstance(config["default"], Config)