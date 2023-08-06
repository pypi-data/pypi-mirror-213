Temperature Converter Package
============================

The Temperature Converter Package provides a set of functions to convert temperatures between Celsius, Kelvin, Fahrenheit, and Rankine.

Installation
------------

You can install the package using pip. Open a terminal or command prompt and run the following command:

```
pip install temperature-converter
```

Usage
-----

To use the temperature conversion functions, you need to import the `temperature_converter` module. Here's an example:

```python
import temperature_converter

celsius = 25
fahrenheit = temperature_converter.celsius_to_fahrenheit(celsius)

print(f"The temperature in Fahrenheit is: {fahrenheit}")