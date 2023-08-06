from countach import fixed

def test_extractInitialInt():
	assert fixed._extractInitialInt("16_S3_B1") == 16

def test_checkIfFixedIsSigned_signedCase():
	assert fixed._checkIfFixedIsSigned("sfix15") == True

def test_checkIfFixedIsSigned_unsignedCase():
	assert fixed._checkIfFixedIsSigned("ufix15") == False

def test_getWordLength():
	assert fixed._getWordLength("sfix16_E20_B1") == 16

def test_getTotalSlope_unspec():
	assert fixed._getTotalSlope("sfix15") == 1

def test_getTotalSlope_specified():
	assert fixed._getTotalSlope("sfix16_S3_B1") == 3

def test_getTotalSlope_exponent():
	assert fixed._getTotalSlope("sfix16_E8_B1") == 256

def test_getBias_unspec():
	assert fixed._getBias("sfix16_S3") == 0

def test_getBias_specified():
	assert fixed._getBias("sfix16_E4_B1") == 1

def test_getFixedTypeParameters():
	assert fixed._getFixedTypeParameters("sfix16_E4_B1") == (True, 16, 16, 1)

def test_decodeFixedTypeString():
	assert fixed.decodeFixedTypeString("sfix16_E5_B1") == "sf16S32B1"
