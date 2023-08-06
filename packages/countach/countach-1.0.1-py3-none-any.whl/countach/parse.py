from countach import characteristic as ch
from countach import measurement as mea 
from countach import types, fileops
from typing import Union, List, Dict

def _parseLongID(rawText: str) -> str:
	if rawText == '""':
		return ""
	else:
		return rawText

# Parse a CHARACTERISTIC section
def parseCSection(section: List[str]) -> ch.Characteristic:
	dictVersion: Dict[str, Union[str, int, float]] = {}
	for rawLine in section:
		line = rawLine.split()
		if line[1] == "Name":
			dictVersion["name"] = line[3]
		elif line[1] == "Long":
			dictVersion["longIdentifier"] = _parseLongID(line[4])
		elif line[1] == "Type":
			dictVersion["vcuType"] = line[3]
		elif line[1] == "ECU":
			dictVersion["address"] = int(line[4], 16)
		elif line[1] == "Record":
			dictVersion["recordLayout"] = line[4]
		elif line[1] == "Maximum":
			dictVersion["maxDifference"] = int(line[4])
		elif line[1] == "Conversion":
			dictVersion["dataType"] = types.getTypeFromRawString(line[4])
		elif line[1] == "Lower":
			dictVersion["lowerLimit"] = float(line[4])
		elif line[1] == "Upper":
			dictVersion["upperLimit"] = float(line[4])
	return ch.characteristicFromDict(dictVersion)

# Parse a MEASUREMENT section
def parseMSection(section: List[str]) -> mea.Measurement:
	dictVersion: Dict[str, Union[str, int, float]] = {}
	for rawLine in section:
		line = rawLine.split()
		if line[1] == "Name":
			dictVersion["name"] = line[3]
		elif line[1] == "Long":
			dictVersion["longIdentifier"] = _parseLongID(line[4])
		elif line[1] == "Data":
			dictVersion["vcuType"] = line[4]
		elif line[1] == "Conversion":
			dictVersion["dataType"] = types.getTypeFromRawString(line[4])
		elif line[1] == "Resolution":
			dictVersion["resolution"] = int(line[5])
		elif line[1] == "Accuracy":
			dictVersion["accuracy"] = int(line[5])
		elif line[1] == "Lower":
			dictVersion["lowerLimit"] = float(line[4])
		elif line[1] == "Upper":
			dictVersion["upperLimit"] = float(line[4])
		elif line[0] == "ECU_ADDRESS":
			dictVersion["address"] = int(line[1], 16)
	return mea.measurementFromDict(dictVersion)

def _parseSection(section: List[str]) -> Union[ch.Characteristic, mea.Measurement]:
	sectionType = section[0].split()[1]
	if sectionType == "CHARACTERISTIC":
		return parseCSection(section)
	elif sectionType == "MEASUREMENT":
		return parseMSection(section)
	else:
		raise RuntimeError("parseSection only accepts CHARACTERISTIC or MEASUREMENT sections")

def parseFile(fileName: str) -> List[Union[ch.Characteristic, mea.Measurement]]:
	sections = fileops.fileToSections(fileName)
	output = []
	for section in sections:
		output.append(_parseSection(section))
	return output
