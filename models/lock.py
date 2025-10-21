class Lock:
    def __init__(self, id: int, resource_type: str, resource_id: int, locked_by: int, created_at):
        self.id = id
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.locked_by = locked_by
        self.created_at = created_at