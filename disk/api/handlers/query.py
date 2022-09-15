from sqlalchemy import and_, func, select

from disk.db.schema import files_table



NODES_QUERY = select([
    files_table.c.id,
    files_table.c.type,
    files_table.c.url,
    files_table.c.size,
    files_table.c.parent_id,
    files_table.c.update_date,
])