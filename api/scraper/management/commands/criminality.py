from django.core.management.base import BaseCommand
import pandas as pd
from reports.models import Country

class Command(BaseCommand):
    help = 'Update criminality index in the database from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')

    def handle(self, *args, **options):
        excel_file_path = options['excel_file']

        try:
            df = pd.read_excel(excel_file_path)
            # Read the Excel file into a DataFrame
            for index, row in df.iterrows():
                country_name = row['Country']
                criminality_index = row['Criminality avg,']

                # Update the database
                try:
                    country = Country.objects.get(name=country_name)
                    setattr(country, 'criminality_index', criminality_index)
                    country.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully updated {country_name}'))
                except Country.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Country {country_name} not found'))


        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.ERROR('Empty Excel file or no data found'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))