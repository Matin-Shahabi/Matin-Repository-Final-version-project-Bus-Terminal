class AuditLog:
    def __init__(self, id, actor, action, timestamp):
        self.id = id
        self.actor = actor
        self.action = action
        self.timestamp = timestamp