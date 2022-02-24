from depart.db import tables, session_scope


if __name__ == '__main__':
    with session_scope() as session:
        result = (
            session.query(tables.Worker)
            .join(tables.WorkerSkill, tables.Worker.id == tables.WorkerSkill.worker_id)
            .join(tables.Skill, tables.WorkerSkill.skill_id == tables.Skill.id)
            .filter(tables.Skill.name == "Stress tolerance")
            .all()
        )
        print(result)
