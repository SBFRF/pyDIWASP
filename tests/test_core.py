"""
Test suite for pyDIWASP core functionality.

This test suite documents the existing capabilities of the pyDIWASP package
by testing the main functions and their expected behavior.
"""
import numpy as np
import pytest

try:
    from private.wavenumber import wavenumber
    from private.hsig import hsig
    from private.check_data import check_data
except ImportError as exc:
    raise ImportError(
        "Could not import pyDIWASP modules. Ensure the package is installed, "
        "for example with 'pip install -e .' from the project root, before "
        "running the tests."
    ) from exc
class TestWavenumber:
    """Tests for the wavenumber calculation function."""
    
    def test_wavenumber_basic(self):
        """Test basic wavenumber calculation."""
        # Test with scalar inputs
        sigma = 2 * np.pi * 0.1  # 0.1 Hz frequency
        h = 10.0  # 10 meter depth
        k = wavenumber(sigma, h)
        
        assert k > 0, "Wavenumber should be positive"
        assert isinstance(k, (float, np.ndarray)), "Should return numeric type"
    
    def test_wavenumber_array(self):
        """Test wavenumber with array inputs."""
        # Test with array inputs
        sigma = 2 * np.pi * np.array([0.1, 0.2, 0.3])
        h = np.array([10.0, 10.0, 10.0])
        k = wavenumber(sigma, h)
        
        assert len(k) == 3, "Should return array of same length"
        assert np.all(k > 0), "All wavenumbers should be positive"
        assert k[0] < k[1] < k[2], "Wavenumber should increase with frequency"
    
    def test_wavenumber_deep_water(self):
        """Test wavenumber in deep water conditions."""
        sigma = 2 * np.pi * 0.1
        h = 1000.0  # Deep water
        k = wavenumber(sigma, h)
        
        # In deep water: k ≈ σ²/g
        g = 9.81
        k_deep = sigma**2 / g
        
        # Should be close to deep water approximation
        assert np.abs(k - k_deep) / k_deep < 0.01, "Should match deep water approximation"


class TestHsig:
    """Tests for the significant wave height calculation."""
    
    def test_hsig_basic(self):
        """Test basic Hsig calculation with synthetic spectrum."""
        # Create a simple spectral matrix
        freqs = np.linspace(0.05, 0.5, 10)
        dirs = np.linspace(-np.pi, np.pi, 36)
        df = freqs[1] - freqs[0]
        ddir = dirs[1] - dirs[0]
        
        # Create a simple Gaussian-like spectrum
        S = np.zeros((len(freqs), len(dirs)))
        for i, f in enumerate(freqs):
            for j, d in enumerate(dirs):
                S[i, j] = np.exp(-((f - 0.1)**2) / 0.01) * np.exp(-((d)**2) / 1.0)
        
        SM = {
            'freqs': freqs,
            'dirs': dirs,
            'S': S
        }
        
        Hs = hsig(SM)
        
        assert Hs > 0, "Significant wave height should be positive"
        assert isinstance(Hs, (float, np.floating)), "Should return a scalar"
    
    def test_hsig_zero_spectrum(self):
        """Test Hsig with zero spectrum."""
        freqs = np.linspace(0.05, 0.5, 10)
        dirs = np.linspace(-np.pi, np.pi, 36)
        
        SM = {
            'freqs': freqs,
            'dirs': dirs,
            'S': np.zeros((len(freqs), len(dirs)))
        }
        
        Hs = hsig(SM)
        
        assert Hs == 0, "Hsig should be zero for zero spectrum"


class TestCheckData:
    """Tests for the data validation function."""
    
    def test_check_instrument_data_valid(self):
        """Test validation of valid instrument data structure."""
        ID = {
            'layout': np.array([[0, 1], [0, 0], [0, 0]]),
            'datatypes': ['elev', 'elev'],
            'depth': 10.0,
            'fs': 2.0,
            'data': np.random.randn(100, 2)
        }
        
        result = check_data(ID, 1)
        
        assert result != [], "Valid data should pass validation"
        assert 'layout' in result, "Should contain layout"
        assert 'datatypes' in result, "Should contain datatypes"
    
    def test_check_instrument_data_invalid_depth(self):
        """Test validation catches invalid depth."""
        ID = {
            'layout': np.array([[0, 1], [0, 0], [0, 0]]),
            'datatypes': ['elev', 'elev'],
            'depth': 'invalid',  # Invalid type
            'fs': 2.0,
            'data': np.random.randn(100, 2)
        }
        
        result = check_data(ID, 1)
        
        assert result == [], "Invalid depth should fail validation"
    
    def test_check_spectral_matrix_valid(self):
        """Test validation of valid spectral matrix structure."""
        SM = {
            'freqs': np.linspace(0.05, 0.5, 10),
            'dirs': np.linspace(-np.pi, np.pi, 36),
            'S': np.random.randn(10, 36)
        }
        
        result = check_data(SM, 2)
        
        assert result != [], "Valid data should pass validation"
        assert 'xaxisdir' in result, "Should add default xaxisdir"
        assert result['xaxisdir'] == 90, "Default xaxisdir should be 90"
    
    def test_check_estimation_parameters_defaults(self):
        """Test that default estimation parameters are set correctly."""
        EP = {}
        
        result = check_data(EP, 3)
        
        assert result != [], "Empty EP should get defaults"
        assert result['dres'] == 180, "Default dres should be 180"
        assert result['method'] == 'IMLM', "Default method should be IMLM"
        assert result['iter'] == 100, "Default iter should be 100"
        assert result['smooth'] == 'ON', "Default smooth should be ON"
    
    def test_check_estimation_parameters_invalid_method(self):
        """Test validation catches invalid estimation method."""
        EP = {
            'method': 'INVALID_METHOD'
        }
        
        result = check_data(EP, 3)
        
        assert result == [], "Invalid method should fail validation"


class TestTransferFunctions:
    """Tests for the transfer functions in the private module."""
    
    def test_elev_transfer_function(self):
        """Test elevation transfer function."""
        from private.elev import elev
        
        # Test parameters
        w = 2 * np.pi * np.array([0.1, 0.2])  # Angular frequencies
        dirs = np.array([0, np.pi/4, np.pi/2])  # Directions
        k = wavenumber(w, np.array([10.0, 10.0]))  # Wavenumbers
        z = 0.0  # Surface elevation
        h = 10.0  # Water depth
        
        result = elev(w, dirs, k, z, h)
        
        assert result.shape == (len(w), len(dirs)), "Should have shape (nfreq, ndir)"
        assert np.all(np.isfinite(result)), "All values should be finite"
    
    def test_pres_transfer_function(self):
        """Test pressure transfer function."""
        from private.pres import pres
        
        w = 2 * np.pi * np.array([0.1, 0.2])
        dirs = np.array([0, np.pi/4, np.pi/2])
        k = wavenumber(w, np.array([10.0, 10.0]))
        z = -2.0  # 2 meters below surface
        h = 10.0
        
        result = pres(w, dirs, k, z, h)
        
        assert result.shape == (len(w), len(dirs)), "Should have shape (nfreq, ndir)"
        assert np.all(np.isfinite(result)), "All values should be finite"
        # Pressure response should be attenuated compared to surface
        assert np.all(np.abs(result) <= 1.1), "Pressure response should be attenuated at depth"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
