"""
Integration tests for pyDIWASP main API functions.

These tests document the high-level API and expected workflow of the package.
"""
import numpy as np
import pytest
import tempfile
import io
import os
from contextlib import redirect_stdout

from infospec import infospec
from interpspec import interpspec
from writespec import writespec


class TestInfospec:
    """Tests for the infospec function."""
    
    def test_infospec_basic(self):
        """Test basic information extraction from a spectrum."""
        # Create a simple spectral matrix
        freqs = np.linspace(0.05, 0.5, 20)
        dirs = np.linspace(-np.pi, np.pi, 36)
        
        # Create a peaked spectrum at 0.1 Hz and 0 degrees
        S = np.zeros((len(freqs), len(dirs)))
        _ = np.argmin(np.abs(freqs - 0.1))
        _ = np.argmin(np.abs(dirs - 0.0))
        
        for i, f in enumerate(freqs):
            for j, d in enumerate(dirs):
                S[i, j] = np.exp(-((f - 0.1)**2) / 0.002) * np.exp(-((d)**2) / 0.5)
        
        SM = {
            'freqs': freqs,
            'dirs': dirs,
            'S': S,
            'xaxisdir': 90
        }
        
        # Capture output (infospec prints to console)
        f = io.StringIO()
        with redirect_stdout(f):
            Hsig, Tp, DTp, Dp = infospec(SM)
        
        assert Hsig > 0, "Significant wave height should be positive"
        assert 8 < Tp < 12, "Peak period should be around 10s (1/0.1 Hz)"
        assert isinstance(DTp, (float, np.floating)), "DTp should be a scalar"
        assert isinstance(Dp, (float, np.floating)), "Dp should be a scalar"
    
    def test_infospec_returns_four_values(self):
        """Test that infospec returns exactly four values."""
        freqs = np.linspace(0.05, 0.5, 10)
        dirs = np.linspace(-np.pi, np.pi, 36)
        S = np.random.rand(len(freqs), len(dirs)) * 0.1
        
        SM = {
            'freqs': freqs,
            'dirs': dirs,
            'S': S,
            'xaxisdir': 90
        }
        
        f = io.StringIO()
        with redirect_stdout(f):
            result = infospec(SM)
        
        assert len(result) == 4, "infospec should return 4 values"


class TestInterpspec:
    """Tests for the interpspec function."""
    
    def test_interpspec_basic(self):
        """Test basic spectral interpolation."""
        # Original spectrum
        freqs_in = np.linspace(0.05, 0.5, 10)
        dirs_in = np.linspace(-np.pi, np.pi, 18)
        S_in = np.random.rand(len(freqs_in), len(dirs_in))
        
        SMin = {
            'freqs': freqs_in,
            'dirs': dirs_in,
            'S': S_in,
            'xaxisdir': 90
        }
        
        # Target spectrum with different resolution
        freqs_out = np.linspace(0.05, 0.5, 20)
        dirs_out = np.linspace(-np.pi, np.pi, 36)
        
        SMout = {
            'freqs': freqs_out,
            'dirs': dirs_out,
            'xaxisdir': 90
        }
        
        result = interpspec(SMin, SMout)
        
        assert 'S' in result, "Result should contain spectral density"
        assert result['S'].shape == (len(freqs_out), len(dirs_out)), \
            "Output shape should match target dimensions"
        assert np.all(np.isfinite(result['S'])), "All values should be finite"
    
    def test_interpspec_preserves_energy(self):
        """Test that interpolation approximately preserves energy."""
        from private.hsig import hsig
        
        # Create a peaked spectrum
        freqs_in = np.linspace(0.05, 0.5, 15)
        dirs_in = np.linspace(-np.pi, np.pi, 36)
        
        S_in = np.zeros((len(freqs_in), len(dirs_in)))
        for i, f in enumerate(freqs_in):
            for j, d in enumerate(dirs_in):
                S_in[i, j] = np.exp(-((f - 0.1)**2) / 0.01) * np.exp(-((d)**2) / 1.0)
        
        SMin = {
            'freqs': freqs_in,
            'dirs': dirs_in,
            'S': S_in,
            'xaxisdir': 90
        }
        
        Hs_in = hsig(SMin)
        
        # Interpolate to finer grid
        freqs_out = np.linspace(0.05, 0.5, 30)
        dirs_out = np.linspace(-np.pi, np.pi, 72)
        
        SMout = {
            'freqs': freqs_out,
            'dirs': dirs_out,
            'xaxisdir': 90
        }
        
        result = interpspec(SMin, SMout)
        Hs_out = hsig(result)
        
        # Energy should be approximately preserved (within 5%)
        relative_error = np.abs(Hs_out - Hs_in) / Hs_in
        assert relative_error < 0.05, f"Energy should be preserved, got {relative_error:.2%} error"
    
    def test_interpspec_no_interpolation_needed(self):
        """Test interpspec when no interpolation is needed."""
        freqs = np.linspace(0.05, 0.5, 10)
        dirs = np.linspace(-np.pi, np.pi, 36)
        S = np.random.rand(len(freqs), len(dirs))
        
        SM = {
            'freqs': freqs,
            'dirs': dirs,
            'S': S,
            'xaxisdir': 90
        }
        
        # Same grid
        SMout = {
            'freqs': freqs.copy(),
            'dirs': dirs.copy(),
            'xaxisdir': 90
        }
        
        # Should warn about no interpolation needed
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = interpspec(SM, SMout)
            # May produce a warning about no interpolation needed
        
        assert 'S' in result, "Should still return a result"


class TestWritespec:
    """Tests for the writespec function."""
    
    def test_writespec_creates_file(self):
        """Test that writespec creates a file with expected format."""
        freqs = np.linspace(0.05, 0.5, 5)
        dirs = np.linspace(-np.pi, np.pi, 9)
        S = np.random.rand(len(freqs), len(dirs))
        
        SM = {
            'freqs': freqs,
            'dirs': dirs,
            'S': S,
            'xaxisdir': 90
        }
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_filename = f.name
        
        try:
            writespec(SM, temp_filename)
            
            # Check that file was created and has content
            assert os.path.exists(temp_filename), "File should be created"
            
            # Read and verify format
            data = np.loadtxt(temp_filename)
            
            # File should have: xaxisdir, nf, nd, freqs, dirs, 999 marker, S values
            expected_length = 1 + 1 + 1 + len(freqs) + len(dirs) + 1 + len(freqs) * len(dirs)
            assert len(data) == expected_length, \
                f"File should have {expected_length} values, got {len(data)}"
            
            # Check xaxisdir
            assert data[0] == 90, "First value should be xaxisdir"
            
            # Check dimensions
            assert data[1] == len(freqs), "Second value should be number of frequencies"
            assert data[2] == len(dirs), "Third value should be number of directions"
            
            # Check marker
            marker_idx = 3 + len(freqs) + len(dirs)
            assert data[marker_idx] == 999, "Marker should be 999"
            
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
    
    def test_writespec_handles_complex_spectrum(self):
        """Test writespec with complex spectral values."""
        freqs = np.linspace(0.05, 0.5, 5)
        dirs = np.linspace(-np.pi, np.pi, 9)
        # Create complex spectrum (though only real part should be written)
        S = np.random.rand(len(freqs), len(dirs)) + 1j * np.random.rand(len(freqs), len(dirs))
        
        SM = {
            'freqs': freqs,
            'dirs': dirs,
            'S': S,
            'xaxisdir': 90
        }
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_filename = f.name
        
        try:
            # Should write real part without error
            writespec(SM, temp_filename)
            assert os.path.exists(temp_filename), "File should be created"
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
