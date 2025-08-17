from django.core.management.base import BaseCommand
from core.models import Location

class Command(BaseCommand):
    help = 'Populate King\'s College locations'

    def handle(self, *args, **options):
        self.stdout.write('Creating King\'s College locations...')
        
        # Clear existing locations
        Location.objects.all().delete()
        
        locations_data = [
            # Parking Space
            {'location_type': 'parking', 'floor_area': 'other', 'specific_location': 'Main Parking Area'},
            
            # Ground Floor
            {'location_type': 'ground_floor', 'floor_area': 'library', 'specific_location': 'Main Library'},
            {'location_type': 'ground_floor', 'floor_area': 'it_lab', 'specific_location': 'IT Lab'},
            {'location_type': 'ground_floor', 'floor_area': 'kafe_kodes', 'specific_location': 'Kafe Kodes'},
            {'location_type': 'ground_floor', 'floor_area': 'bathroom', 'specific_location': 'Ground Floor Bathroom'},
            
            # First Floor (Admin Section)
            {'location_type': 'first_floor', 'floor_area': 'admin_section', 'specific_location': 'Main Admin Office'},
            {'location_type': 'first_floor', 'floor_area': 'academic_support', 'specific_location': 'Academic Support Center'},
            {'location_type': 'first_floor', 'floor_area': 'found_items_drop', 'specific_location': 'Found Items Drop-off Counter'},
            {'location_type': 'first_floor', 'floor_area': 'items_claim', 'specific_location': 'Items Claim Center'},
            {'location_type': 'first_floor', 'floor_area': 'bathroom', 'specific_location': 'First Floor Bathroom'},
            
            # Second Floor
            {'location_type': 'second_floor', 'floor_area': 'class_201', 'specific_location': 'Classroom 201'},
            {'location_type': 'second_floor', 'floor_area': 'class_202', 'specific_location': 'Classroom 202'},
            {'location_type': 'second_floor', 'floor_area': 'class_203', 'specific_location': 'Classroom 203'},
            {'location_type': 'second_floor', 'floor_area': 'class_204', 'specific_location': 'Classroom 204'},
            {'location_type': 'second_floor', 'floor_area': 'bathroom', 'specific_location': 'Second Floor Bathroom'},
            
            # Third Floor
            {'location_type': 'third_floor', 'floor_area': 'class_301', 'specific_location': 'Classroom 301'},
            {'location_type': 'third_floor', 'floor_area': 'class_302', 'specific_location': 'Classroom 302'},
            {'location_type': 'third_floor', 'floor_area': 'class_303', 'specific_location': 'Classroom 303'},
            {'location_type': 'third_floor', 'floor_area': 'class_304', 'specific_location': 'Classroom 304'},
            {'location_type': 'third_floor', 'floor_area': 'bathroom', 'specific_location': 'Third Floor Bathroom'},
            
            # Fourth Floor
            {'location_type': 'fourth_floor', 'floor_area': 'class_401', 'specific_location': 'Classroom 401'},
            {'location_type': 'fourth_floor', 'floor_area': 'class_402', 'specific_location': 'Classroom 402'},
            {'location_type': 'fourth_floor', 'floor_area': 'class_403', 'specific_location': 'Classroom 403'},
            {'location_type': 'fourth_floor', 'floor_area': 'class_404', 'specific_location': 'Classroom 404'},
            {'location_type': 'fourth_floor', 'floor_area': 'bathroom', 'specific_location': 'Fourth Floor Bathroom'},
            
            # Fifth Floor
            {'location_type': 'fifth_floor', 'floor_area': 'class_501', 'specific_location': 'Classroom 501'},
            {'location_type': 'fifth_floor', 'floor_area': 'class_502', 'specific_location': 'Classroom 502'},
            {'location_type': 'fifth_floor', 'floor_area': 'class_503', 'specific_location': 'Classroom 503'},
            {'location_type': 'fifth_floor', 'floor_area': 'class_504', 'specific_location': 'Classroom 504'},
            {'location_type': 'fifth_floor', 'floor_area': 'bathroom', 'specific_location': 'Fifth Floor Bathroom'},
            
            # Sixth Floor
            {'location_type': 'sixth_floor', 'floor_area': 'program_hall', 'specific_location': 'Program Hall'},
            {'location_type': 'sixth_floor', 'floor_area': 'dolab', 'specific_location': 'DoLab'},
            {'location_type': 'sixth_floor', 'floor_area': 'cipl', 'specific_location': 'CIPL'},
            {'location_type': 'sixth_floor', 'floor_area': 'table_tennis', 'specific_location': 'Table Tennis Board'},
            {'location_type': 'sixth_floor', 'floor_area': 'bathroom', 'specific_location': 'Sixth Floor Bathroom'},
            
            # Seventh Floor
            {'location_type': 'seventh_floor', 'floor_area': 'canteen', 'specific_location': 'Main Canteen'},
            {'location_type': 'seventh_floor', 'floor_area': 'bathroom', 'specific_location': 'Seventh Floor Bathroom'},
            
            # Club Rooms (various floors)
            {'location_type': 'ground_floor', 'floor_area': 'tech_club', 'specific_location': 'Tech Club Room'},
            {'location_type': 'ground_floor', 'floor_area': 'finance_club', 'specific_location': 'Finance Club Room'},
            {'location_type': 'ground_floor', 'floor_area': 'social_club', 'specific_location': 'Social Club Room'},
            {'location_type': 'ground_floor', 'floor_area': 'athletics_club', 'specific_location': 'Athletics Club Room'},
            {'location_type': 'ground_floor', 'floor_area': 'literature_club', 'specific_location': 'Literature Club Room'},
            {'location_type': 'ground_floor', 'floor_area': 'skillbee_club', 'specific_location': 'SkillBee Club Room'},
        ]
        
        created_locations = []
        for location_data in locations_data:
            location = Location.objects.create(**location_data)
            created_locations.append(location)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(created_locations)} King\'s College locations!'
            )
        )
        
        # Display created locations
        for location in created_locations:
            self.stdout.write(f'  - {location}')
