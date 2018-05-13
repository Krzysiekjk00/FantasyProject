from import_export import resources

from Ekstraklasa.models import Players


class PlayerResource(resources.ModelResource):
    class Meta:
        model = Players
        fields = ['id', 'name', 'position', 'is_specific', 'overall_points']