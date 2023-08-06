from countach import types

def test_getTypeFromRawString_uint8():
	assert types.getTypeFromRawString("VCU_CM_uint8") == "uint8"

def test_getTypeFromRawString_uint16():
	assert types.getTypeFromRawString("VCU_CM_uint16") == "uint16"

def test_getTypeFromRawString_uint32():
	assert types.getTypeFromRawString("VCU_CM_uint32") == "uint32"

def test_getTypeFromRawString_int8():
	assert types.getTypeFromRawString("VCU_CM_int8") == "int8"

def test_getTypeFromRawString_int16():
	assert types.getTypeFromRawString("VCU_CM_int16") == "int16"

def test_getTypeFromRawString_int32():
	assert types.getTypeFromRawString("VCU_CM_int32") == "int32"

def test_getTypeFromRawString_single():
	assert types.getTypeFromRawString("VCU_CM_single") == "single"

def test_getTypeFromRawString_boolean():
	assert types.getTypeFromRawString("VCU_CM_boolean") == "boolean"

def test_getTypeFromRawString_fixed():
	assert types.getTypeFromRawString("VCU_CM_sfix16_E5_B1") == "sf16S32B1"
