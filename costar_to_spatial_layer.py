import re
from pathlib import Path

import geopandas as gpd
import pandas as pd
import yaml

ROOT = Path(__file__).parent
CONFIGS = ROOT / "configs"
DATA = ROOT / "data"
OUTPUT = ROOT / "output"


def load_yaml(path: Path) -> dict | list:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def read_spreadsheets(folder: Path) -> pd.DataFrame:
    """Read all spreadsheet files in *folder* and concatenate into one DataFrame."""
    frames = []
    for p in sorted(folder.iterdir()):
        if p.suffix in (".xlsx", ".xls", ".csv"):
            if p.suffix == ".csv":
                frames.append(pd.read_csv(p))
            else:
                frames.append(pd.read_excel(p))
    return pd.concat(frames, ignore_index=True)


def rename_and_trim(df: pd.DataFrame, renames: dict[str, str]) -> pd.DataFrame:
    """Rename columns per *renames* dict (old -> new) and drop everything else."""
    df = df.rename(columns=renames)
    keep = list(renames.values())
    return df[[c for c in keep if c in df.columns]]


def normalize_text_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Create normalized copies of specified columns with a _norm suffix."""
    for col in columns:
        if col in df.columns:
            df[col + "_norm"] = df[col].str.lower().str.replace(r"[^a-z0-9]", "", regex=True)
    return df


def fix_secondary_types(df: pd.DataFrame, fixes: list[dict]) -> pd.DataFrame:
    """Apply secondary-type overrides based on key-field lookups."""
    for rule in fixes:
        for key_fields, mappings in rule.items():
            key_fields = [k.strip() for k in key_fields.split(",")]
            for mapping in mappings:
                for value, new_type in mapping.items():
                    normalized_value = re.sub(r"[^a-z0-9]", "", value.lower())
                    mask = pd.Series(False, index=df.index)
                    for col in key_fields:
                        norm_col = col + "_norm"
                        if norm_col in df.columns:
                            mask |= df[norm_col].str.contains(normalized_value, na=False)
                        else:
                            mask |= df[col].str.contains(normalized_value, na=False)
                    df.loc[mask, "secondary_type"] = new_type
    return df


def filter_secondary_types(df: pd.DataFrame, allowed: list[str]) -> pd.DataFrame:
    return df[df["secondary_type"].isin(allowed)].copy()


def to_spatial(df: pd.DataFrame, target_epsg: int) -> gpd.GeoDataFrame:
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
        crs="EPSG:4326",
    )
    return gdf.to_crs(epsg=target_epsg)


def save_by_type(gdf: gpd.GeoDataFrame, output_folder: Path) -> None:
    output_folder.mkdir(parents=True, exist_ok=True)
    for sec_type, group in gdf.groupby("secondary_type"):
        today = pd.Timestamp.today().strftime("%Y_%m_%d")
        filename = "costar_" + sec_type.replace(" ", "_").lower() + f"s_{today}.gpkg"
        group.to_file(output_folder / filename, driver="GPKG")


def main() -> None:
    column_renames = load_yaml(CONFIGS / "column_renames.yaml")
    secondary_type_fixes = load_yaml(CONFIGS / "secondary_type_fixes.yaml")
    settings = load_yaml(CONFIGS / "settings.yaml")

    df = read_spreadsheets(DATA)
    df = rename_and_trim(df, column_renames)
    df = df.drop_duplicates(subset=["latitude", "longitude", "property_name"])
    df = normalize_text_columns(df, ["property_name", "anchor_tenants"])
    df = fix_secondary_types(df, secondary_type_fixes)
    df = filter_secondary_types(df, settings["secondary_types"])

    df = df.drop(columns=[c for c in df.columns if c.endswith("_norm")])
    gdf = to_spatial(df, settings["epsg"])
    save_by_type(gdf, OUTPUT)


if __name__ == "__main__":
    main()
