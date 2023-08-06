from typing import Tuple

# Given a string that starts with an integer, returns the integer
def _extractInitialInt(source: str) -> int:
	if source.isnumeric():
		return int(source)

	# Get the index of the first non-numeric character
	firstNonNumeric = 0
	for i, char in enumerate(source):
		if not char.isnumeric():
			firstNonNumeric = i
			break
	
	if firstNonNumeric == 0:
		return 0

	return int(source[:firstNonNumeric])

def _checkIfFixedIsSigned(typeString: str) -> bool:
	if typeString[0] == "u":
		signed = False
	elif typeString[0] == "s":
		signed = True
	else:
		raise ValueError("Sign indication not found in type string")
	return signed

def _getWordLength(typeString: str) -> int:
	# Remove unneccessary data
	typeString = typeString[4:]
	splitTypeString = typeString.split("_")
	return int(splitTypeString[0])

# TODO: Check if negative total slopes possible?
def _getTotalSlope(typeString: str) -> int:
	totalSlope = 1
	if "S" in typeString:
		sIndex = typeString.index("S") + 1
		totalSlope = _extractInitialInt(typeString[sIndex:])
	elif "E" in typeString:
		eIndex = typeString.index("E") + 1
		totalSlope = 2 ** _extractInitialInt(typeString[eIndex:])
	return totalSlope

# TODO: Check if negative biases possible?
def _getBias(typeString: str) -> int:
	bias = 0
	if "B" in typeString:
		bIndex = typeString.index("B") + 1
		print(typeString[bIndex:])
		bias = _extractInitialInt(typeString[bIndex:])
	return bias

def _getFixedTypeParameters(typeString: str) -> Tuple[bool, int, int, int]:
	signed = _checkIfFixedIsSigned(typeString)
	wordLength = _getWordLength(typeString)
	totalSlope = _getTotalSlope(typeString)
	bias = _getBias(typeString)
	return signed, wordLength, totalSlope, bias

def decodeFixedTypeString(rawString: str) -> str:
	if rawString[0] != "s" and rawString[0] != "u":
		if "_sfix" in rawString:
			startIndex = rawString.index("_sfix") + 1
		elif "_ufix" in rawString:
			startIndex = rawString.index("_ufix") + 1
		else:
			raise ValueError(f"String {rawString} is not a valid fixdt")
		rawString = rawString[startIndex:]
	
	signed, wordLength, totalSlope, bias = _getFixedTypeParameters(rawString)
	# Convert the boolean of signed into a letter
	if signed:
		signedString = "s"
	else:
		signedString = "u"
	
	return f"{signedString}f{wordLength}S{totalSlope}B{bias}"
