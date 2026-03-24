# costar

Cleans up CoStar spreadsheet exports and converts them into spatial point layers (GeoPackage).

## Usage

1. Place one or more CoStar export spreadsheets (`.xlsx`, `.xls`, or `.csv`) in the `data/` folder.
2. Run the script:
   ```
   uv run costar_to_spatial_layer.py
   ```
3. Output `.gpkg` files are written to `output/`, one per "secondary type".

## Configuration

All settings live in `configs/`