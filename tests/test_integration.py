"""
Integration test for the complete pyDIWASP workflow.

This test creates synthetic wave data and runs it through the full analysis pipeline.
"""
import numpy as np
import pytest
import sys
import os
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dirspec import dirspec
from private.check_data import check_data


class TestDirspecIntegration:
    """Integration tests for the main dirspec analysis function."""
    
    @pytest.fixture
    def synthetic_wave_data(self):
        """Create synthetic wave measurement data for testing."""
        # Sampling parameters
        fs = 2.0  # 2 Hz sampling frequency
        duration = 600  # 600 seconds (10 minutes)
        npts = int(fs * duration)
        t = np.arange(npts) / fs
        
        # Wave parameters
        H = 1.0  # 1 meter wave height
        T = 10.0  # 10 second period
        f = 1.0 / T
        omega = 2 * np.pi * f
        
        # Simulate elevation at two locations
        # Location 1: at origin
        # Location 2: 10 meters in x-direction
        phase_shift = 0.1  # Small phase shift due to spatial separation
        
        # Add some random noise
        np.random.seed(42)
        noise_level = 0.05
        
        eta1 = H/2 * np.sin(omega * t) + noise_level * np.random.randn(npts)
        eta2 = H/2 * np.sin(omega * t - phase_shift) + noise_level * np.random.randn(npts)
        
        # Create instrument data structure
        ID = {
            'layout': np.array([[0.0, 10.0], [0.0, 0.0], [0.0, 0.0]]),  # x, y, z positions
            'datatypes': ['elev', 'elev'],  # Both are elevation measurements
            'depth': 20.0,  # 20 meter water depth
            'fs': fs,
            'data': np.column_stack([eta1, eta2])
        }
        
        return ID
    
    @pytest.fixture
    def spectral_matrix_template(self):
        """Create a spectral matrix template for analysis."""
        SM = {
            'freqs': np.linspace(0.05, 0.5, 10),  # 0.05 to 0.5 Hz
            'dirs': np.linspace(-np.pi, np.pi, 36),  # -180 to 180 degrees
            'xaxisdir': 90  # Cartesian convention
        }
        return SM
    
    @pytest.fixture
    def estimation_parameters(self):
        """Create estimation parameters for analysis."""
        EP = {
            'method': 'IMLM',  # Iterative Maximum Likelihood Method
            'iter': 100,
            'smooth': 'OFF',  # Turn off smoothing for faster test
            'dres': 36,  # Directional resolution
            'nfft': 512  # FFT resolution - explicitly set to avoid bug in check_data
        }
        return EP
    
    def test_dirspec_basic_run(self, synthetic_wave_data, spectral_matrix_template, 
                               estimation_parameters):
        """Test that dirspec runs without errors on synthetic data."""
        import io
        from contextlib import redirect_stdout
        
        # Redirect stdout to suppress print statements
        f = io.StringIO()
        
        with redirect_stdout(f):
            SMout, EPout = dirspec(
                synthetic_wave_data, 
                spectral_matrix_template, 
                estimation_parameters,
                Options_=['MESSAGE', 0, 'PLOTTYPE', 0, 'FILEOUT', '']
            )
        
        # Check that output is valid
        assert SMout is not None, "Should return spectral matrix"
        assert EPout is not None, "Should return estimation parameters"
        assert SMout != [], "Spectral matrix should not be empty"
        assert EPout != [], "Estimation parameters should not be empty"
    
    def test_dirspec_output_structure(self, synthetic_wave_data, spectral_matrix_template,
                                     estimation_parameters):
        """Test that dirspec output has expected structure."""
        import io
        from contextlib import redirect_stdout
        
        f = io.StringIO()
        
        with redirect_stdout(f):
            SMout, EPout = dirspec(
                synthetic_wave_data,
                spectral_matrix_template,
                estimation_parameters,
                Options_=['MESSAGE', 0, 'PLOTTYPE', 0, 'FILEOUT', '']
            )
        
        # Check spectral matrix structure
        assert 'freqs' in SMout, "Output should contain frequencies"
        assert 'dirs' in SMout, "Output should contain directions"
        assert 'S' in SMout, "Output should contain spectral density"
        
        # Check dimensions
        nf = len(SMout['freqs'])
        nd = len(SMout['dirs'])
        assert SMout['S'].shape == (nf, nd), \
            f"Spectral density should have shape ({nf}, {nd})"
        
        # Check that spectral values are non-negative
        assert np.all(SMout['S'] >= 0), "Spectral density should be non-negative"
        
        # Check estimation parameters
        assert 'method' in EPout, "Should contain method"
        assert 'nfft' in EPout, "Should contain nfft"
        assert EPout['nfft'] > 0, "nfft should be positive"
    
    def test_dirspec_with_different_methods(self, synthetic_wave_data, 
                                           spectral_matrix_template):
        """Test dirspec with different estimation methods."""
        import io
        from contextlib import redirect_stdout
        
        methods = ['IMLM', 'EMEP']
        
        for method in methods:
            EP = {
                'method': method,
                'iter': 50,  # Reduce iterations for speed
                'smooth': 'OFF',
                'dres': 36,
                'nfft': 512  # Explicitly set to avoid bug
            }
            
            f = io.StringIO()
            with redirect_stdout(f):
                try:
                    SMout, EPout = dirspec(
                        synthetic_wave_data,
                        spectral_matrix_template,
                        EP,
                        Options_=['MESSAGE', 0, 'PLOTTYPE', 0, 'FILEOUT', '']
                    )
                    
                    assert SMout != [], f"Method {method} should produce output"
                    assert EPout['method'] == method, \
                        f"Output should confirm method {method} was used"
                except Exception as e:
                    pytest.fail(f"Method {method} failed with error: {e}")
    
    def test_dirspec_file_output(self, synthetic_wave_data, spectral_matrix_template,
                                estimation_parameters):
        """Test that dirspec can write output to file."""
        import io
        from contextlib import redirect_stdout
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_filename = f.name
        
        try:
            stdout_f = io.StringIO()
            with redirect_stdout(stdout_f):
                SMout, EPout = dirspec(
                    synthetic_wave_data,
                    spectral_matrix_template,
                    estimation_parameters,
                    Options_=['MESSAGE', 0, 'PLOTTYPE', 0, 'FILEOUT', temp_filename]
                )
            
            # Check that file was created
            assert os.path.exists(temp_filename), "Output file should be created"
            
            # Verify file has content
            with open(temp_filename, 'r') as f:
                content = f.read()
                assert len(content) > 0, "Output file should not be empty"
        
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
    
    def test_dirspec_detects_peak_frequency(self, synthetic_wave_data,
                                           spectral_matrix_template,
                                           estimation_parameters):
        """Test that dirspec correctly identifies the dominant frequency."""
        import io
        from contextlib import redirect_stdout
        
        f = io.StringIO()
        with redirect_stdout(f):
            SMout, EPout = dirspec(
                synthetic_wave_data,
                spectral_matrix_template,
                estimation_parameters,
                Options_=['MESSAGE', 0, 'PLOTTYPE', 0, 'FILEOUT', '']
            )
        
        # Find the peak frequency in the 1D spectrum
        S_1d = np.sum(np.real(SMout['S']), axis=1)
        peak_idx = np.argmax(S_1d)
        peak_freq = SMout['freqs'][peak_idx]
        
        # The input has a peak at 0.1 Hz (10 second period)
        # Allow some tolerance due to spectral resolution
        expected_freq = 0.1
        freq_tolerance = 0.05  # 0.05 Hz tolerance
        
        assert np.abs(peak_freq - expected_freq) < freq_tolerance, \
            f"Peak frequency {peak_freq:.3f} Hz should be near {expected_freq} Hz"


class TestDataValidationIntegration:
    """Integration tests for data validation in the workflow."""
    
    def test_invalid_instrument_data_rejected(self):
        """Test that invalid instrument data is properly rejected."""
        import io
        from contextlib import redirect_stdout
        
        # Invalid ID: missing required fields (depth and fs)
        # Use 3-row layout to avoid check_data bug with 2-row layouts
        ID_invalid = {
            'layout': np.array([[0, 1], [0, 0], [0, 0]]),
            'datatypes': ['elev', 'elev'],
            # Missing 'depth' and 'fs' - these are required
        }
        
        SM = {
            'freqs': np.linspace(0.05, 0.5, 10),
            'dirs': np.linspace(-np.pi, np.pi, 36)
        }
        
        EP = {'method': 'IMLM', 'nfft': 512}
        
        f = io.StringIO()
        with redirect_stdout(f):
            SMout, EPout = dirspec(ID_invalid, SM, EP,
                                  Options_=['MESSAGE', 0, 'PLOTTYPE', 0])
        
        # Should return empty results for invalid data
        assert SMout == [], "Invalid data should return empty result"
        assert EPout == [], "Invalid data should return empty result"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
