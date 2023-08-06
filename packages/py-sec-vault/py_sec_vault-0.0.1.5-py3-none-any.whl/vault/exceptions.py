class VaultClientImproperlyConfiguredError(Exception):
    def __init__(self, message="Vault client is improperly configured."):
        self.message = message
        super().__init__(self.message)
