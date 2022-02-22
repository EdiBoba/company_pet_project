from depart.db import tables, session_scope


if __name__ == '__main__':
    with session_scope() as session:
        result = session.query(tables.Position).first()
        print(result.id)
