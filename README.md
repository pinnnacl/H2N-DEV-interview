## H2N-DEV-interview


# XML Processing, JSON Conversion, and Data Handling in Python

## Scenario
You are working on a project that involves **processing XML order files**. Your job is to **read these files, convert them into JSON format**, and handle any **errors gracefully** during processing. This task will test your **Python skills, error handling abilities**, and how well you **log events** for traceability. 

Some XML files may contain **missing elements, malformed structures, or unexpected fields**. Your solution should ensure that the system continues processing even when some files encounter issues.

---

## My Role

### 1. First Approch to create python code

The following Python script demonstrates how to parse an XML file and recursively convert it into a dictionary.

### Dependencies

- Python 3.x
- `xml.etree.ElementTree` (comes with Python by default)
- `json` (comes with Python by default)
- `os` (comes with Python by default)

### Code Overview

The script consists of two key functions:
1. `xml_to_dict(element)`: Recursively converts an XML element and its children into a dictionary format.
2. `check_xml_file(file)`: Reads an XML file, parses it, and converts the root element into a dictionary using the `xml_to_dict` function.



- **Program Execution error:**
  ```
    Cell In[62], line 38 in check_xml_file
    tree = ET.parse(f)

    File ~\AppData\Local\anaconda3\lib\xml\etree\ElementTree.py:1222 in parse
      tree.parse(source, parser)

    File ~\AppData\Local\anaconda3\lib\xml\etree\ElementTree.py:580 in parse
      self._root = parser._parse_whole(source)

    File <string>
  ParseError: not well-formed (invalid token): line 8, column 4
  ```

### 2. Modify the code to add below feature


- Extracts key fields (like OrderID, Customer, and Products).

- Converts the extracted data to JSON format.

- Handling errors and logging

### Error 

"Check for unexpected fields" not working as expected. The file order_010.xml have an additional field <Discount>10.00</Discount> which should be pointed out in the log


### 3. Made additional changes to the  "Check for unexpected fields" 

Got output as expected.