# Gerenciamento de releases
class ReleasesManager:
    def __init__(self):
        self.releases = []
        self.archived = []

    def add_release(self, release):
        self.releases.append(release)

    def filter_releases(self, category):
        return [release for release in self.releases if category.lower() in release['subject'].lower()]

    def archive_release(self, release_id):
        release = self.releases.pop(release_id)
        self.archived.append(release)

    def get_archived(self):
        return self.archived