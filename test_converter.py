"""
Test script to verify BPM to milliseconds conversion logic
"""

def test_bpm_conversion():
    """Test the BPM conversion logic"""
    
    def convert_bpm_to_ms(bpm, note_multiplier=1.0):
        """Convert BPM to milliseconds"""
        ms_per_quarter_note = 60000 / bpm
        return ms_per_quarter_note * note_multiplier
    
    # Test cases
    test_cases = [
        (120, 1.0, 500.0),    # 120 BPM quarter note = 500ms
        (60, 1.0, 1000.0),    # 60 BPM quarter note = 1000ms
        (120, 0.5, 250.0),    # 120 BPM eighth note = 250ms
        (140, 1.0, 428.57),   # 140 BPM quarter note ≈ 428.57ms
        (90, 2.0, 1333.33),   # 90 BPM half note ≈ 1333.33ms
    ]
    
    print("BPM Conversion Test Results:")
    print("=" * 40)
    
    all_passed = True
    
    for bpm, multiplier, expected in test_cases:
        result = convert_bpm_to_ms(bpm, multiplier)
        passed = abs(result - expected) < 0.1  # Allow small floating point differences
        
        note_type = {
            4.0: "Whole",
            2.0: "Half", 
            1.0: "Quarter",
            0.5: "Eighth",
            0.25: "Sixteenth",
            0.125: "Thirty-second"
        }.get(multiplier, f"Custom ({multiplier})")
        
        status = "PASS" if passed else "FAIL"
        print(f"{bpm} BPM {note_type} Note: {result:.2f}ms (expected {expected}ms) - {status}")
        
        if not passed:
            all_passed = False
    
    print("=" * 40)
    print(f"Overall Result: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    
    return all_passed

if __name__ == "__main__":
    test_bpm_conversion()
