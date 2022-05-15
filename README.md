# Quadtree-Image-Compression
Python image compression using quadtree data structure
# Install
1. `python -m venv venv` - create virtual environment for project
2. Run `Activate` script in `./venv/Scripts`
3. `pip install -r requirements.txt`
# Usage
Run `main.py`
CLI arguments:
1. `--input` - input file
2. `--output` - output file (optional, if specified - shows result in new window)
3. `--gif` - should generate gif.gif file, that shows compression process
4. `--level` - compression level (integer, greater level means greater compression)
5. `--multithread` - use threading to speed up compression
6. `--outline` - create red outline between quads on result
# Examples
`python main.py --input=Octocat.png --gif --level=100 --output=result.png`
<table>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/73060327/168464604-bec1341d-4f9b-488d-af87-57a40464dae3.png" style="max-width: 30%"></td>
    <td><img src="https://user-images.githubusercontent.com/73060327/168464723-cd40e10a-7a75-4e00-ae8b-2d3a03dd7cf3.gif" style="max-width: 30%"></td>
    <td><img src="https://user-images.githubusercontent.com/73060327/168464625-c3f1d6fd-6594-4103-9d8a-3a5294914cd9.png" style="max-width: 30%"></td>
  </tr>
</table>
