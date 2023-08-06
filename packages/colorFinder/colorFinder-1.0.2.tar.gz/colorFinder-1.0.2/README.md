# Common Colors Finder Website

Why color pick when you can grab the 5 most used colors inside a logo or an image and use them for your design and css!

Upload your image or provide an image url and check instantly.

# Usage

```python
from colorFinder import ColorFinder

color_finder = ColorFinder(image_url="https://warehouse-camo.ingress.cmh1.psfhosted.org/f10043f97c4efa219b0dca9bab54a6caf620718b/68747470733a2f2f7365637572652e67726176617461722e636f6d2f6176617461722f62306163633463623730383637613663373463306139653465656330356464653f73697a653d3430", num_colors=5)

colors_list = color_finder.get_common_colors()

print(colors_list)
```

## Output 

Returns a list of tuples containing the RGB value and color count matching your top num_colors
```text
[((113, 113, 113), 17), ((127, 127, 127), 14), ((117, 117, 117), 13), ((105, 105, 105), 12), ((166, 166, 166), 12)]
```
# Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request on [GitHub](https://github.com/danysrour/commonColorsFinder.git).

# License

This project is licensed under the MIT License

```text

You can now copy this code and use it as your README.md file.
```