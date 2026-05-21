class WorkingMemory:

    def __init__(self):
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key, None)

    def clear(self):
        self.data = {}

    def as_context(self):
        if not self.data:
            return ""
        lines = ["Current context:"]
        for key, value in self.data.items():
            lines.append(f"  {key}: {value}")
        return "\n".join(lines)