
from sqlalchemy.dialects.mysql import insert as mysql_insert
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from ..models.models import Country
from sqlalchemy.sql import func



async def upsert_country_data(db_session: AsyncSession, country_objects_list: List[Country]) -> int:
    """
    Implements the Update or Insert (Upsert) logic using MySQL's 
    ON DUPLICATE KEY UPDATE clause for a seamless cache refresh.
    """
    
    if not country_objects_list:
        print("No country data provided to upsert.")
        return 0

    # 1. Convert ORM objects back into Dictionaries
    # The Core insert statement works with raw data dictionaries (rows).
    rows_to_insert: List[Dict[str, Any]] = [
        # Use ORM's built-in dictionary conversion
        {c.name: getattr(country, c.name) for c in country.__table__.columns if c.name not in ('id',)}
        for country in country_objects_list
    ]

    # 2. Define the Upsert Statement
    # Select the target table metadata from one of the ORM objects
    country_table = Country.__table__
    
    # Construct the base INSERT statement
    insert_stmt = mysql_insert(country_table).values(rows_to_insert)
    
    # 3. Define the ON DUPLICATE KEY UPDATE clause (The magic!)
    # This clause tells the database: "If the Primary Key (name) conflicts, 
    # then UPDATE the following columns instead of throwing an error."
    # We explicitly update all non-PK columns, plus the refresh timestamp.
    
    # Create a dictionary mapping columns to their new values from the data being inserted (excluded)
    update_mapping = {
        col.name: func.values(col)
        for col in country_table.columns
        # Exclude the Primary Key (name) and the auto-increment ID
        if col.name not in ('name', 'id')
    }
    
    # Ensure 'last_refreshed_at' is explicitly updated to the current time if it's not in the excluded list
    # update_mapping['last_refreshed_at'] = func.now() # Use if you want server-side time on update
    
    upsert_stmt = insert_stmt.on_duplicate_key_update(**update_mapping)

    # 4. Execute and Commit the Transaction
    try:
        # The session executes the Core statement asynchronously
        result = await db_session.execute(upsert_stmt)
        await db_session.commit()
        
        # NOTE: .rowcount on MySQL for upsert only returns 1 for inserts and 2 for updates. 
        # We rely on successful commit as the indicator.
        print(f"✅ Cache refreshed successfully. Processed {len(rows_to_insert)} records.")
        return len(rows_to_insert)

    except Exception as e:
        await db_session.rollback()
        print(f"🛑 CRITICAL ERROR during Upsert operation: {type(e).__name__} - {e}")
        raise

