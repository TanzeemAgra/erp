from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
from crm.models import (
    Client, ContactPerson, ClientInteraction, Opportunity, Task,
    ClientCategory, ClientStatus, IndustryType, InteractionType, OpportunityStage
)
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample CRM data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clients',
            type=int,
            default=15,
            help='Number of clients to create',
        )

    def handle(self, *args, **options):
        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()

        # Sample company data
        companies = [
            {'name': 'TechCorp Solutions', 'industry': 'technology', 'contact': 'John Smith'},
            {'name': 'HealthCare Plus', 'industry': 'healthcare', 'contact': 'Sarah Johnson'},
            {'name': 'EduTech Systems', 'industry': 'education', 'contact': 'Michael Brown'},
            {'name': 'RetailMax Inc', 'industry': 'retail', 'contact': 'Lisa Wilson'},
            {'name': 'FinanceHub LLC', 'industry': 'finance', 'contact': 'David Chen'},
            {'name': 'ManufacturePro', 'industry': 'manufacturing', 'contact': 'Emily Davis'},
            {'name': 'ConsultExperts', 'industry': 'consulting', 'contact': 'Robert Taylor'},
            {'name': 'Global Innovations', 'industry': 'technology', 'contact': 'Jessica Lee'},
            {'name': 'MedicalCare Group', 'industry': 'healthcare', 'contact': 'Thomas Anderson'},
            {'name': 'Learning Dynamics', 'industry': 'education', 'contact': 'Amanda Miller'},
            {'name': 'Shopping Central', 'industry': 'retail', 'contact': 'Kevin White'},
            {'name': 'Investment Partners', 'industry': 'finance', 'contact': 'Michelle Garcia'},
            {'name': 'Production Systems', 'industry': 'manufacturing', 'contact': 'Christopher Martin'},
            {'name': 'Strategic Advisors', 'industry': 'consulting', 'contact': 'Nicole Thompson'},
            {'name': 'Digital Ventures', 'industry': 'technology', 'contact': 'Andrew Jackson'},
        ]

        cities = [
            ('New York', 'NY'), ('Los Angeles', 'CA'), ('Chicago', 'IL'),
            ('Houston', 'TX'), ('Phoenix', 'AZ'), ('Philadelphia', 'PA'),
            ('San Antonio', 'TX'), ('San Diego', 'CA'), ('Dallas', 'TX'),
            ('San Jose', 'CA'), ('Austin', 'TX'), ('Jacksonville', 'FL'),
            ('San Francisco', 'CA'), ('Columbus', 'OH'), ('Indianapolis', 'IN'),
        ]

        self.stdout.write('Creating sample clients...')

        for i, company_data in enumerate(companies[:options['clients']]):
            city, state = cities[i % len(cities)]
            
            # Create client
            client = Client.objects.create(
                company_name=company_data['name'],
                contact_person=company_data['contact'],
                email=f"{company_data['contact'].lower().replace(' ', '.')}@{company_data['name'].lower().replace(' ', '').replace(',', '').replace('.', '')}.com",
                phone=f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}",
                website=f"https://www.{company_data['name'].lower().replace(' ', '').replace(',', '').replace('.', '')}.com",
                industry=company_data['industry'],
                company_size=random.randint(10, 1000),
                annual_revenue=random.randint(100000, 10000000),
                address_line1=f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'Cedar', 'Elm'])} St",
                city=city,
                state=state,
                postal_code=f"{random.randint(10000, 99999)}",
                country='United States',
                category=random.choice([choice[0] for choice in ClientCategory.choices]),
                status=random.choice([choice[0] for choice in ClientStatus.choices]),
                source=random.choice(['Website', 'Referral', 'Cold Call', 'Trade Show', 'Social Media']),
                account_manager=admin_user,
                assigned_to=admin_user,
                credit_limit=random.randint(10000, 100000),
                payment_terms=random.choice(['Net 30', 'Net 15', 'COD', 'Net 60']),
                notes=f"Sample client created for {company_data['name']}. Lorem ipsum dolor sit amet.",
                tags='sample, demo, test',
                created_by=admin_user,
                last_contact_date=timezone.now() - timedelta(days=random.randint(1, 30)),
                next_follow_up=timezone.now() + timedelta(days=random.randint(1, 30)),
            )

            # Create contact persons
            for j in range(random.randint(1, 3)):
                ContactPerson.objects.create(
                    client=client,
                    first_name=random.choice(['John', 'Jane', 'Mike', 'Sarah', 'David', 'Lisa']),
                    last_name=random.choice(['Smith', 'Johnson', 'Brown', 'Davis', 'Wilson', 'Miller']),
                    job_title=random.choice(['CEO', 'CTO', 'CFO', 'Manager', 'Director', 'VP Sales']),
                    email=f"contact{j}@{company_data['name'].lower().replace(' ', '').replace(',', '').replace('.', '')}.com",
                    phone=f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}",
                    is_primary=j == 0,
                    is_decision_maker=random.choice([True, False]),
                )

            # Create interactions
            for j in range(random.randint(1, 5)):
                ClientInteraction.objects.create(
                    client=client,
                    interaction_type=random.choice([choice[0] for choice in InteractionType.choices]),
                    subject=f"Discussion about {random.choice(['project requirements', 'pricing', 'timeline', 'proposal', 'contract'])}",
                    description=f"Had a productive conversation with {client.contact_person} regarding their business needs and potential collaboration opportunities.",
                    interaction_date=timezone.now() - timedelta(days=random.randint(1, 60)),
                    duration_minutes=random.randint(15, 120),
                    outcome=random.choice(['Positive', 'Neutral', 'Needs follow-up', 'Interested', 'Not interested']),
                    next_action=f"Follow up with {random.choice(['proposal', 'pricing', 'demo', 'meeting', 'contract'])}",
                    next_action_date=timezone.now() + timedelta(days=random.randint(1, 14)),
                    handled_by=admin_user,
                )

            # Create opportunities
            if random.choice([True, False]):
                for j in range(random.randint(1, 2)):
                    Opportunity.objects.create(
                        client=client,
                        title=f"{company_data['name']} - {random.choice(['Software Implementation', 'Consulting Services', 'System Upgrade', 'Training Program', 'Support Contract'])}",
                        description=f"Potential opportunity to provide services to {company_data['name']}. Initial discussions are promising.",
                        estimated_value=random.randint(10000, 500000),
                        probability=random.randint(20, 90),
                        stage=random.choice([choice[0] for choice in OpportunityStage.choices if choice[0] not in ['closed_won', 'closed_lost']]),
                        expected_close_date=(timezone.now() + timedelta(days=random.randint(30, 180))).date(),
                        owner=admin_user,
                        competitors=random.choice(['CompetitorA', 'CompetitorB', 'Internal team', 'None identified']),
                        notes=f"Good opportunity with {company_data['name']}. Client seems interested in our solutions.",
                    )

            # Create tasks
            for j in range(random.randint(1, 3)):
                Task.objects.create(
                    client=client,
                    title=f"{random.choice(['Follow up with', 'Send proposal to', 'Schedule demo for', 'Review contract with', 'Call'])} {client.contact_person}",
                    description=f"Important task related to {client.company_name} business development.",
                    priority=random.choice([choice[0] for choice in Task.PRIORITY_CHOICES]),
                    status=random.choice([choice[0] for choice in Task.STATUS_CHOICES]),
                    assigned_to=admin_user,
                    due_date=timezone.now() + timedelta(days=random.randint(1, 30)),
                    created_by=admin_user,
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {options["clients"]} sample clients with related data!')
        )
        self.stdout.write('You can now log in with username: admin, password: admin123')
