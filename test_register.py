#!/usr/bin/env python3

from ti.features.detector.detector_path_register import DetectorPathRegister
from ti.features.intervention.intervention_path_register import INV_PathRegister
from ti.model.symbol_models import SymbolType

def test_detector_register():
    """Test detector path register functionality"""
    print("Testing DetectorPathRegister...")
    register = DetectorPathRegister()
    
    # Test getting all symbols
    symbols = register.get_symbol_model()
    print(f"Loaded {len(symbols)} detector symbols")
    
    # Test searching by type
    functions = register.search_symbol_data(symbol_type=SymbolType.FUNCTION)
    print(f"Found {len(functions)} functions")
    
    # Test searching by domain
    detector_symbols = register.search_symbol_data(domain="detector")
    print(f"Found {len(detector_symbols)} detector symbols")
    
    print("Detector register test passed!\n")

def test_intervention_register():
    """Test intervention path register functionality"""
    print("Testing InterventionPathRegister...")
    register = INV_PathRegister()
    
    # Test getting all symbols
    symbols = register.get_symbol_model()
    print(f"Loaded {len(symbols)} intervention symbols")
    
    # Test searching by type
    classes = register.search_symbol_data(symbol_type=SymbolType.CLASS)
    print(f"Found {len(classes)} classes")
    
    # Test searching by domain
    intervention_symbols = register.search_symbol_data(domain="intervention")
    print(f"Found {len(intervention_symbols)} intervention symbols")
    
    print("Intervention register test passed!\n")

if __name__ == "__main__":
    test_detector_register()
    test_intervention_register()
    print("All tests passed!")