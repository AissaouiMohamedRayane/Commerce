from django.core.management.base import BaseCommand
from auctions.models import Category

class Command(BaseCommand):
    help = 'Import categories from a file'

    def handle(self, *args, **options):
        file_path = 'auctions/text/category.txt'

        with open(file_path) as lines:
            for line in lines:
                c = Category(category=line.strip())
                c.save()

        self.stdout.write(self.style.SUCCESS('Categories imported successfully.'))
