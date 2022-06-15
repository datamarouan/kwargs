# Generated by Django 3.2.12 on 2022-06-14 15:19

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('utilisateur', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='kwgApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=12)),
                ('application_full_name', models.CharField(max_length=124)),
                ('application_identifier', models.CharField(max_length=124, unique=True)),
            ],
            options={
                'verbose_name': 'Application',
            },
        ),
        migrations.CreateModel(
            name='kwgOrganization',
            fields=[
                ('identification', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('roles', models.ManyToManyField(to='utilisateur.kwgActorRole')),
            ],
            options={
                'verbose_name': 'Organisation',
                'verbose_name_plural': 'Organisations',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='kwgPostalAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purpose', models.CharField(choices=[('O', 'Bureau'), ('S', 'Site'), ('H', 'Domicile'), ('D', 'Point de distribution postal'), ('UD', "Défini par l'utilisateur")], help_text='Identifies the logical location of the address', max_length=2)),
                ('description', models.TextField(blank=True, null=True)),
                ('user_defined_purpose', models.CharField(blank=True, max_length=255, null=True)),
                ('internal_location', models.CharField(blank=True, help_text='An organization defined address for internal mail delivery', max_length=255, null=True)),
                ('addresses_lines', models.CharField(blank=True, max_length=255, null=True, verbose_name='Adresse')),
                ('postal_box', models.CharField(blank=True, max_length=255, null=True, verbose_name='Boîte postale')),
                ('town', models.CharField(blank=True, max_length=255, null=True, verbose_name='Localité')),
                ('region', models.CharField(blank=True, max_length=255, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='Code postal')),
                ('country', models.CharField(blank=True, default='Belgique', max_length=255, null=True, verbose_name='Pays')),
                ('of_organization', models.ManyToManyField(blank=True, to='catalogue.kwgOrganization')),
                ('of_person', models.ManyToManyField(blank=True, to='utilisateur.kwgPerson')),
            ],
            options={
                'verbose_name': 'Adresse Postale',
                'verbose_name_plural': 'Adresses postales',
                'ordering': ('postal_code', 'addresses_lines'),
            },
        ),
        migrations.CreateModel(
            name='EtablissementEnseignement',
            fields=[
                ('kwgorganization_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='catalogue.kwgorganization')),
                ('fase', models.CharField(blank=True, max_length=6, null=True)),
                ('bce', models.CharField(blank=True, max_length=15, null=True)),
                ('reseau', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': "Etablissement d'enseignement",
                'verbose_name_plural': "Etablissements d'enseignement",
            },
            bases=('catalogue.kwgorganization',),
        ),
        migrations.CreateModel(
            name='GeoRefPostalAddress',
            fields=[
                ('kwgpostaladdress_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='catalogue.kwgpostaladdress')),
                ('latitude', models.FloatField(default=0, editable=False)),
                ('longitude', models.FloatField(default=0, editable=False)),
            ],
            options={
                'verbose_name': 'Adresse postale géoréférencée',
                'verbose_name_plural': 'Adresses postales géoréférencées',
            },
            bases=('catalogue.kwgpostaladdress',),
        ),
        migrations.CreateModel(
            name='kwgTelecomAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purpose', models.CharField(choices=[('O', 'Bureau'), ('S', 'Site'), ('H', 'Domicile'), ('D', 'Point de distribution postal'), ('UD', "Défini par l'utilisateur")], help_text='Identifies the logical location of the address', max_length=2)),
                ('description', models.TextField(blank=True, null=True)),
                ('user_defined_purpose', models.CharField(blank=True, max_length=255, null=True)),
                ('telephone_numbers', models.CharField(blank=True, max_length=255, null=True)),
                ('mobile_numbers', models.CharField(blank=True, max_length=255, null=True)),
                ('electronic_mail_addresses', models.EmailField(blank=True, max_length=254, null=True)),
                ('www_home_page_url', models.URLField(blank=True, null=True)),
                ('of_organization', models.ManyToManyField(blank=True, to='catalogue.kwgOrganization')),
                ('of_person', models.ManyToManyField(blank=True, to='utilisateur.kwgPerson')),
            ],
            options={
                'verbose_name': 'Adresse Telecom',
                'verbose_name_plural': 'Adresses Telecom',
            },
        ),
        migrations.CreateModel(
            name='kwgPersonAndOrganization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roles', models.ManyToManyField(blank=True, to='utilisateur.kwgActorRole')),
                ('the_organization', models.ManyToManyField(related_name='engages', to='catalogue.kwgOrganization', verbose_name='Organisation(s)')),
                ('the_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='engaged_in', to='utilisateur.kwgperson', verbose_name='Personne')),
            ],
            options={
                'verbose_name': "Personne agissant au nom d'une Organisation",
                'verbose_name_plural': "Personnes agissant au nom d'une Organisation",
            },
        ),
        migrations.CreateModel(
            name='kwgOwnerHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(choices=[(1, 'Readwrite'), (2, 'Readonly'), (3, 'Locked'), (4, 'Readwritelocked'), (5, 'Readonlylocked')], default=1)),
                ('change_action', models.IntegerField(choices=[(1, 'Nochange'), (2, 'Modified'), (3, 'Added'), (4, 'Deleted'), (5, 'Notdefined')], default=5)),
                ('last_modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modifying_application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='app_modifer', to='catalogue.kwgapplication')),
                ('last_modifying_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_modifer', to='catalogue.kwgpersonandorganization')),
                ('owning_application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='app_owning', to='catalogue.kwgapplication')),
                ('owning_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_owning', to='catalogue.kwgpersonandorganization')),
            ],
            options={
                'verbose_name': 'Historique Utilisateur',
                'verbose_name_plural': 'Historiques Utilisateur',
            },
        ),
        migrations.CreateModel(
            name='kwgOrganizationRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='A name used to identify or qualify the relationship.', max_length=255, null=True)),
                ('description', models.TextField(blank=True)),
                ('related_organization', models.ManyToManyField(related_name='is_related_by', to='catalogue.kwgOrganization')),
                ('relating_organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relates', to='catalogue.kwgorganization')),
            ],
            options={
                'verbose_name': 'Relation entre organisations',
                'verbose_name_plural': 'Relations entre organisations',
            },
        ),
        migrations.AddField(
            model_name='kwgapplication',
            name='application_developper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='catalogue.kwgorganization'),
        ),
        migrations.CreateModel(
            name='ImplantationScolaire',
            fields=[
                ('georefpostaladdress_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='catalogue.georefpostaladdress')),
                ('fase_imp', models.CharField(blank=True, max_length=6, null=True)),
                ('niveau', models.IntegerField(choices=[(1, 'Fondamental'), (2, 'Secondaire'), (3, 'Superieur')])),
                ('genre', models.IntegerField(choices=[(1, 'Ordinaire'), (2, 'Specialise')])),
                ('type_enseignement', models.CharField(choices=[('prom_soc_sec', 'Promotion sociale secondaire'), ('prom_soc_sup', 'Promotion sociale supérieur'), ('art_hor_red', 'Artistique à horaire réduit'), ('mat_spe', 'Maternel spécialisé'), ('prim_spe', 'Primaire spécialisé'), ('mat_ord', 'Maternel ordinaire'), ('prim_ord', 'Primaire ordinaire'), ('sec_ord', 'Secondaire ordinaire'), ('sec_cefa', 'Secondaire CEFA'), ('sec_spe', 'Secondaire spécialisé'), ('eco_sup_art', 'École supérieure des Arts'), ('prom_soc_cefa', 'Promotion Sociale CEFA'), ('unif', 'Université'), ('he', 'Haute École')], max_length=24)),
            ],
            options={
                'abstract': False,
            },
            bases=('catalogue.georefpostaladdress',),
        ),
        migrations.AddConstraint(
            model_name='kwgapplication',
            constraint=models.UniqueConstraint(fields=('application_full_name', 'version'), name='unique_application'),
        ),
    ]
