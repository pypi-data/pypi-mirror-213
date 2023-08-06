import countach.parse
import testdata.output as data

def test_parseFile():
	output = countach.parse.parseFile("tests/testdata/newvcu_2.a2l")
	assert output == data.output
