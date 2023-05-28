from unittest import mock
import pytest
from weathercli import app


class TestCLI:
    def test_valid_city(self, runner):
        result = runner.invoke(app, ["pune"])
        assert result.exit_code == 0
        assert "CURRENT WEATHER |" in result.output
        assert "FORECAST FOR THE NEXT 5 DAYS" in result.output
    
    def test_invalid_city(self, runner):
        result = runner.invoke(app, ["invalid"])
        assert result.exit_code == 0
        assert "🚨 Error: Failed to retrieve weather data. Please enter a valid city." in result.output
    
    def test_no_city_passed(self, runner):
        result = runner.invoke(app)
        assert result.exit_code == 2
        assert "Missing argument 'CITY'" in result.output