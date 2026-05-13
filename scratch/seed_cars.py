import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carboncraftstudio.settings')
django.setup()

from products.models import CarBrand, CarModel

def seed_cars():
    cars_data = {
        'Suzuki': ['Mehran', 'Alto', 'Cultus', 'Swift', 'WagonR', 'Bolan', 'Ravi', 'Vitara', 'Jimny'],
        'Toyota': ['Corolla', 'Yaris', 'Fortuner', 'Hilux', 'Camry', 'Land Cruiser', 'Prius', 'Rush'],
        'Honda': ['Civic', 'City', 'BR-V', 'Accord', 'HR-V', 'CR-V'],
        'Kia': ['Sportage', 'Picanto', 'Stonic', 'Sorento', 'Carnival'],
        'Hyundai': ['Tucson', 'Elantra', 'Sonata', 'Porter', 'Santa Fe'],
        'Changan': ['Alsvin', 'Karvaan', 'M9'],
        'MG': ['HS', 'ZS', 'ZS EV'],
        'Haval': ['H6', 'Jolion'],
        'Prince': ['Pearl', 'Glory 580'],
        'United': ['Bravo', 'Alpha'],
        'Proton': ['Saga', 'X70'],
    }

    for brand_name, models in cars_data.items():
        brand, created = CarBrand.objects.get_or_create(name=brand_name)
        if created:
            print(f"Created Brand: {brand_name}")
        
        for model_name in models:
            model, created = CarModel.objects.get_or_create(brand=brand, name=model_name)
            if created:
                print(f"  Created Model: {model_name}")

if __name__ == '__main__':
    print("Starting car data seeding...")
    seed_cars()
    print("Seeding completed!")
