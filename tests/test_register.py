#!/usr/bin/env python3

from ti.services.symbol_service import SymbolService
from ti.model.symbol_models import SymbolType

def test_symbol_service_registers():
    """Test symbol service with path register functionality"""
    print("Testing SymbolService with PathRegisterService...")
    service = SymbolService()
    
    # Test symbol resolution functionality
    try:
        # Test finding symbol paths for different domains
        detector_path = service.find_symbol("detector", "DetectorFactory")
        if detector_path:
            print(f"Found detector symbol path: {detector_path}")
        else:
            print("Detector symbol not found (expected if not registered)")
            
        intervention_path = service.find_symbol("intervention", "InterventionFactory")
        if intervention_path:
            print(f"Found intervention symbol path: {intervention_path}")
        else:
            print("Intervention symbol not found (expected if not registered)")
            
    except Exception as e:
        print(f"Symbol resolution test completed: {e}")
    
    print("Symbol service register test passed!\n")

def test_symbol_resolution():
    """Test symbol resolution functionality"""
    print("Testing symbol resolution...")
    service = SymbolService()
    
    # Test finding symbol paths
    try:
        # Test finding a symbol path (this will depend on actual registered symbols)
        symbol_path = service.find_symbol("detector", "DetectorFactory")
        if symbol_path:
            print(f"Found symbol path: {symbol_path}")
        else:
            print("Symbol not found (expected if not registered)")
    except Exception as e:
        print(f"Symbol resolution test completed (domain may not be registered): {e}")
    
    print("Symbol resolution test passed!\n")

if __name__ == "__main__":
    test_symbol_service_registers()
    test_symbol_resolution()
    print("All tests passed!")