from typing import List

def _importFile(fileName: str) -> List[str]:
	with open(fileName, "r") as f:
		lines = f.readlines()
	return lines

# Take the whole a2l file and extract the lines containing measurement or characteristic sections
def _linesToSections(lines: List[str]) -> List[List[str]]:
	# Whether or not the current line is inside a section
	inSection = False
	output = []
	currentOutput = []
	for rawline in lines:
		# Remove leading and trailing whitespace
		line = rawline.strip()

		if line == "/begin CHARACTERISTIC" or line == "/begin MEASUREMENT":
			inSection = True
		elif line == "/end CHARACTERISTIC" or line == "/end MEASUREMENT":
			inSection = False
			currentOutput.append(line)
			output.append(currentOutput)
			currentOutput = []
		
		if inSection:
			currentOutput.append(line)

	return output

def fileToSections(fileName: str) -> List[List[str]]:
	lines = _importFile(fileName)
	return _linesToSections(lines)
