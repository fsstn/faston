# Practice 5: RegEx Receipt Parser

## Overview
This script uses Python's `re` module to parse unstructured receipt data from `raw.txt`.

## Extracted Data
- **Date/Time**: Parsed using `\d{2}/\d{2}/\d{4}`.
- **Products**: Identified via multiline anchors and non-greedy text matching.
- **Prices**: Captured as floats for mathematical operations.
- **Totals**: Calculated by summing extracted item prices.