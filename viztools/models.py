from django.db import models

# Create your models here.
class DataFile(models.Model):
    snap_file = models.FileField(upload_to='uploads/snap/')
    catalog_file = models.FileField(upload_to='uploads/catalog/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Snap: {self.snap_file.name}, Catalog: {self.catalog_file.name}"

