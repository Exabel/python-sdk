import itertools

_CSV_EXTENSIONS = {".csv"}
_CSV_COMPRESSION_EXTENSIONS = {".gz", ".bz2", ".zip", ".xz", ".zst", ""}
FULL_CSV_EXTENSIONS = set(
    csv_ext + comp_ext
    for csv_ext, comp_ext in itertools.product(_CSV_EXTENSIONS, _CSV_COMPRESSION_EXTENSIONS)
)
EXCEL_EXTENSIONS = {".xlsx"}
GLOBAL_ENTITY_TYPE = "global"
GLOBAL_ENTITY_NAME = f"entityTypes/{GLOBAL_ENTITY_TYPE}/entities/global"
