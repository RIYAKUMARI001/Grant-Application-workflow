from django.core.management.base import BaseCommand
from core.models import Rubric

class Command(BaseCommand):
    help = 'Create default rubrics for the grant system'

    def handle(self, *args, **options):
        # Create default rubrics
        rubrics_data = [
            {'name': 'Innovation', 'max_score': 10, 'weight': 30.00},
            {'name': 'Feasibility', 'max_score': 10, 'weight': 25.00},
            {'name': 'Impact', 'max_score': 10, 'weight': 25.00},
            {'name': 'Budget Clarity', 'max_score': 10, 'weight': 20.00},
        ]

        for rubric_data in rubrics_data:
            rubric, created = Rubric.objects.get_or_create(
                name=rubric_data['name'],
                defaults={
                    'max_score': rubric_data['max_score'],
                    'weight': rubric_data['weight'],
                    'active': True
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created rubric: {rubric.name}')
                )
            else:
                self.stdout.write(
                    f'Rubric already exists: {rubric.name}'
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully created/updated rubrics')
        )