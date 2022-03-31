# Generated by Django 3.2.12 on 2022-03-30 14:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='kwgActorRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('SU', 'Fournisseur'), ('MA', 'Fabricant'), ('CO', 'Prestataire'), ('SB', 'Sous traitant'), ('AR', 'Architecte'), ('SE', 'Ingénieur Structure/Stabilité'), ('CE', 'Ingénieur Coûts'), ('CL', 'Client'), ('BP', 'Propriétaire du bâtiment'), ('BO', 'Opérateur du bâtiment'), ('ME', 'Ingénieur mécanique'), ('EE', 'Ingénieur électricité'), ('PM', 'Chef de projet'), ('FM', 'Facility Manager'), ('CI', 'Ingénieur civil'), ('CN', 'Ingénieur mise en service'), ('IR', 'Ingénieur'), ('PR', 'Propriétaire'), ('CS', 'Consultant'), ('CP', 'Directeur des travaux'), ('CC', 'Chef de chantier'), ('RV', 'Revendeur'), ('UD', "Défini par l'utilisateur")], help_text='The name of the role played by an actor', max_length=2)),
                ('user_defined_role', models.CharField(blank=True, help_text='Allows for specification of user defined roles beyond the enumeration values provided by Role attribute of type IfcRoleEnum', max_length=255)),
                ('description', models.TextField(blank=True, help_text='A textual description rzelating the nature of the role played by an actor')),
            ],
            options={
                'verbose_name': "Rôle d'acteur",
                'verbose_name_plural': "Rôles d'acteur",
            },
        ),
        migrations.CreateModel(
            name='kwgPerson',
            fields=[
                ('identification', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('middle_name', models.CharField(blank=True, help_text='Additional names given to a person that enable their identification apart from others who may have the same or similar family and given names', max_length=255, null=True, verbose_name='Autre(s) prénom(s)')),
                ('prefix_titles', models.CharField(blank=True, help_text="The word, or group of words, which specify the person's social and/or professional standing and appear before his/her names", max_length=5, null=True)),
                ('suffix_titles', models.CharField(blank=True, help_text="The word, or group of words, which specify the person's social and/or professional standing and appear before his/her names", max_length=5, null=True)),
                ('image', models.ImageField(default='default.jpg', upload_to='avatars/')),
                ('roles', models.ManyToManyField(to='utilisateur.kwgActorRole')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Personne',
            },
        ),
    ]
