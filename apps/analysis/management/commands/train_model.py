from django.core.management.base import BaseCommand
from analysis.pipeline import train_and_store

class Command(BaseCommand):
    help = 'Train ML models and store results in MongoDB'

    def add_arguments(self, parser):
        parser.add_argument('-d', '--dir', type=str, default='', help='Relative path to data directory')

    def handle(self, *args, **options):
        dir = options['dir']
        self.stdout.write('Starting training pipeline...')
        train_and_store(self, dir)
        self.stdout.write('Training completed.')

    def write_suc(self, text):
        self.stdout.write(self.style.SUCCESS(text))

    def write_warn(self, text):
        self.stdout.write(self.style.WARNING(text))

    def write_err(self, text):
        self.stderr.write(self.style.ERROR(text))

