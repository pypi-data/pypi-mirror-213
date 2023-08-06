<div align="center">
<h1>Somnium</h1>
Create beautiful artwork using the power of AI
<br/><br/><img src="https://static.pepy.tech/personalized-badge/somnium?period=total&amp;units=none&amp;left_color=black&amp;right_color=blue&amp;left_text=Total Downloads" alt="Downloads">
</div>


<h2>Installation:</h2>

```bash
>>> python3 -m pip install somnium
```

<h2>Examples:</h2>

<h3>somnium:</h3>

```python
from somnium import Somnium

# Get Styles (url)
print(Somnium.StylesGraph())

# Get Styles (list)
print(Somnium.Styles())

# Generate Artwork
print(Somnium.Generate('Hunter Schafer', 2009))
```

<h3>somnium.sync:</h3>

```python
import asyncio
from somnium.sync import Somnium

async def my_test():
    # Get Styles (url)
    print(await Somnium.StylesGraph())

    # Get Styles (list)
    print(await Somnium.Styles())

    # Generate Artwork
    print(await Somnium.Generate('Hunter Schafer', 2009))
    
asyncio.run(my_test())
```
