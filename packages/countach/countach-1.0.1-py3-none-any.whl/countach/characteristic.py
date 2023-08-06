from dataclasses import dataclass
from typing import Dict

@dataclass
class Characteristic:
	name: str
	longIdentifier: str
	vcuType: str
	address: int
	recordLayout: str
	maxDifference: int
	dataType: str
	lowerLimit: float
	upperLimit: float

def characteristicFromDict(d) -> Characteristic:
	return Characteristic(
		d["name"],
		d["longIdentifier"],
		d["vcuType"],
		d["address"],
		d["recordLayout"],
		d["maxDifference"],
		d["dataType"],
		d["lowerLimit"],
		d["upperLimit"]
	)
