A Postcode Validator Library.

The initial releas includes validation for only UK Postcodes


## Install

postcode_validator is available on PyPI:

```bash
$ pip install postcode-validator
```


## Usage

```python
from postcode_validator.uk.uk_postcode_validator import UKPostcode

postcode = UKPostcode('w1a0ax')

postcode.postcode
# output
'W1A 0AX'

postcode.outward
# output
'W1A'

postcode.inward
# output
'0AX'

postcode.area
# output
'W'

postcode.district
# output
'1A'

postcode.sector
# output
'0'

postcode.unit
# output
'AX'
```
