from django.core.management.base import BaseCommand
from core.models import NotificationTemplate

class Command(BaseCommand):
    help = 'Fix email templates with problematic patterns'

    def handle(self, *args, **options):
        self.stdout.write('Fixing email templates...')
        
        templates = NotificationTemplate.objects.all()
        fixed_count = 0
        
        for template in templates:
            if template.html_template:
                # Fix the problematic pattern
                old_pattern = "{user.first_name or 'there'}"
                new_pattern = "{user.first_name}"
                
                if old_pattern in template.html_template:
                    template.html_template = template.html_template.replace(old_pattern, new_pattern)
                    template.save()
                    fixed_count += 1
                    self.stdout.write(f'  - Fixed {template.template_type}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully fixed {fixed_count} email templates!'
            )
        )
