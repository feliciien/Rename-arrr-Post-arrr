import os
import json

class LicenseManager:
    """
    LicenseManager handles the offline licensing system.

    - Checks for a license file in the installation directory.
    - Limits the number of renames to 50 without a license file.
    - Provides unlimited renames if the license file is present.
    """

    def __init__(self, license_file='license.key', counter_file='rename_count.json'):
        self.installation_directory = os.path.dirname(os.path.abspath(__file__))
        self.license_path = os.path.join(self.installation_directory, license_file)
        self.counter_path = os.path.join(self.installation_directory, counter_file)
        self.max_renames = 50
        self.rename_count = 0
        self.unlimited = False
        self.load_license()
        self.load_counter()

    def load_license(self):
        """Check for the presence of the license file."""
        if os.path.exists(self.license_path):
            self.unlimited = True
        else:
            self.unlimited = False

    def load_counter(self):
        """Load the current rename count."""
        if os.path.exists(self.counter_path):
            try:
                with open(self.counter_path, 'r') as f:
                    data = json.load(f)
                    self.rename_count = data.get('rename_count', 0)
            except (json.JSONDecodeError, FileNotFoundError):
                self.rename_count = 0
        else:
            self.rename_count = 0

    def save_counter(self):
        """Save the current rename count."""
        with open(self.counter_path, 'w') as f:
            json.dump({'rename_count': self.rename_count}, f)

    def can_rename(self):
        """Check if the user can perform a rename operation."""
        if self.unlimited:
            return True
        else:
            return self.rename_count < self.max_renames

    def increment_rename_count(self):
        """Increment the rename count after a successful rename operation."""
        if not self.unlimited:
            self.rename_count += 1
            self.save_counter()

    def remaining_renames(self):
        """Return the number of remaining renames."""
        if self.unlimited:
            return float('inf')
        else:
            return max(0, self.max_renames - self.rename_count)
