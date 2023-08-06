def celsius_to_fahrenheit(celsius):
    """
    Convert temperature from Celsius to Fahrenheit.
    
    Args:
        celsius (float): Temperature in Celsius.
    
    Returns:
        float: Temperature in Fahrenheit.
    """
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit

def fahrenheit_to_celsius(fahrenheit):
    """
    Convert temperature from Fahrenheit to Celsius.
    
    Args:
        fahrenheit (float): Temperature in Fahrenheit.
    
    Returns:
        float: Temperature in Celsius.
    """
    celsius = (fahrenheit - 32) * 5/9
    return celsius

def celsius_to_kelvin(celsius):
    """
    Convert temperature from Celsius to Kelvin.
    
    Args:
        celsius (float): Temperature in Celsius.
    
    Returns:
        float: Temperature in Kelvin.
    """
    kelvin = celsius + 273.15
    return kelvin

def kelvin_to_celsius(kelvin):
    """
    Convert temperature from Kelvin to Celsius.
    
    Args:
        kelvin (float): Temperature in Kelvin.
    
    Returns:
        float: Temperature in Celsius.
    """
    celsius = kelvin - 273.15
    return celsius

def fahrenheit_to_kelvin(fahrenheit):
    """
    Convert temperature from Fahrenheit to Kelvin.
    
    Args:
        fahrenheit (float): Temperature in Fahrenheit.
    
    Returns:
        float: Temperature in Kelvin.
    """
    kelvin = (fahrenheit - 32) * 5/9 + 273.15
    return kelvin

def kelvin_to_fahrenheit(kelvin):
    """
    Convert temperature from Kelvin to Fahrenheit.
    
    Args:
        kelvin (float): Temperature in Kelvin.
    
    Returns:
        float: Temperature in Fahrenheit.
    """
    fahrenheit = (kelvin - 273.15) * 9/5 + 32
    return fahrenheit

def celsius_to_rankine(celsius):
    """
    Convert temperature from Celsius to Rankine.
    
    Args:
        celsius (float): Temperature in Celsius.
    
    Returns:
        float: Temperature in Rankine.
    """
    rankine = (celsius + 273.15) * 9/5
    return rankine

def rankine_to_celsius(rankine):
    """
    Convert temperature from Rankine to Celsius.
    
    Args:
        rankine (float): Temperature in Rankine.
    
    Returns:
        float: Temperature in Celsius.
    """
    celsius = (rankine - 491.67) * 5/9
    return celsius

def fahrenheit_to_rankine(fahrenheit):
    """
    Convert temperature from Fahrenheit to Rankine.
    
    Args:
        fahrenheit (float): Temperature in Fahrenheit.
    
    Returns:
        float: Temperature in Rankine.
    """
    rankine = fahrenheit + 459.67
    return rankine

def rankine_to_fahrenheit(rankine):
    """
    Convert temperature from Rankine to Fahrenheit.
    
    Args:
        rankine (float): Temperature in Rankine.
    
    Returns:
        float: Temperature in Fahrenheit.
    """
    fahrenheit = rankine - 459.67
    return fahrenheit
    
def kelvin_to_rankine(kelvin):
    """
    Convert temperature from Kelvin to Rankine.
    
    Args:
        kelvin (float): Temperature in Kelvin.
    
    Returns:
        float: Temperature in Rankine.
    """
    rankine = kelvin * 9/5
    return rankine

def rankine_to_kelvin(rankine):
    """
    Convert temperature from Rankine to Kelvin.
    
    Args:
        rankine (float): Temperature in Rankine.
    
    Returns:
        float: Temperature in Kelvin.
    """
    kelvin = rankine * 5/9
    return kelvin
