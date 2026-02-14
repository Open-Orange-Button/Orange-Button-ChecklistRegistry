import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class AnswerTypeItemTypeEnum(models.TextChoices):
    Text = ('Text', _('Text'))
    EnumeratedSingle = ('EnumeratedSingle', _('EnumeratedSingle'))
    EnumeratedMultiple = ('EnumeratedMultiple', _('EnumeratedMultiple'))
    Numeric = ('Numeric', _('Numeric'))
    Date = ('Date', _('Date'))
    URL = ('URL', _('URL'))
    File = ('File', _('File'))

class ContactTypeItemTypeEnum(models.TextChoices):
    Other = ('Other', _('Other'))
    FireMarshal = ('FireMarshal', _('FireMarshal'))
    Owner = ('Owner', _('Owner'))
    OffTaker = ('OffTaker', _('OffTaker'))
    Inspector = ('Inspector', _('Inspector'))
    Engineer = ('Engineer', _('Engineer'))
    Originator = ('Originator', _('Originator'))
    Installer = ('Installer', _('Installer'))
    Investor = ('Investor', _('Investor'))
    PermittingOfficial = ('PermittingOfficial', _('PermittingOfficial'))
    ProjectManager = ('ProjectManager', _('ProjectManager'))
    Salesperson = ('Salesperson', _('Salesperson'))
    ReportPreparer = ('ReportPreparer', _('ReportPreparer'))
    Referrer = ('Referrer', _('Referrer'))
    Security = ('Security', _('Security'))
    Safety = ('Safety', _('Safety'))
    Technician = ('Technician', _('Technician'))
    Occupant = ('Occupant', _('Occupant'))

class EntityRoleItemTypeEnum(models.TextChoices):
    Originator = ('Originator', _('Originator'))
    Installer = ('Installer', _('Installer'))
    AuthorityHavingJurisdiction = ('AuthorityHavingJurisdiction', _('Authority Having Jurisdiction (AHJ)'))
    Manufacturer = ('Manufacturer', _('Manufacturer'))
    Surety = ('Surety', _('Surety'))
    Insurer = ('Insurer', _('Insurer'))
    TestLab = ('TestLab', _('Test Lab'))
    CertificationAgency = ('CertificationAgency', _('Certification Agency'))
    Aggregator = ('Aggregator', _('Aggregator'))
    PropertyOwner = ('PropertyOwner', _('Property Owner'))
    Financier = ('Financier', _('Financier'))
    QualifyingAgency = ('QualifyingAgency', _('Qualifying Agency'))

class IdentifierTypeItemTypeEnum(models.TextChoices):
    Other = ('Other', _('Other'))
    UUID = ('UUID', _('UUID'))
    UPC = ('UPC', _('UPC'))
    ProdCode = ('ProdCode', _('ProdCode'))
    LEI = ('LEI', _('Legal Entity Identifier'))
    PEN = ('PEN', _('Private Enterprise Number'))
    DID = ('DID', _('Decentralized Identifier'))
    DUNS = ('DUNS', _('DUNS'))
    DPP_EU = ('DPP_EU', _('EU Digital Product Passport'))
    FEIN = ('FEIN', _('Federal Employer Identification Number'))
    UEI = ('UEI', _('Unique Entity Identifier'))

class LengthItemTypeUnit(models.TextChoices):
    ft = ('ft', _('Foot'))
    in_ = ('in', _('Inch'))
    mi = ('mi', _('Mile'))
    nmi = ('nmi', _('Nautical Mile'))
    yd = ('yd', _('Yard'))
    cm = ('cm', _('Centimetre'))
    dm = ('dm', _('Decimetre'))
    km = ('km', _('Kilometre'))
    m = ('m', _('Metre'))
    mm = ('mm', _('Millimetre'))

class LocationDeterminationMethodItemTypeEnum(models.TextChoices):
    Unknown = ('Unknown', _('Unknown'))
    GPS = ('GPS', _('GPS'))
    Survey = ('Survey', _('Survey'))
    AerialImage = ('AerialImage', _('AerialImage'))
    EngineeringReport = ('EngineeringReport', _('EngineeringReport'))
    AddressGeocoding = ('AddressGeocoding', _('AddressGeocoding'))

class LocationTypeItemTypeEnum(models.TextChoices):
    DeviceSpecific = ('DeviceSpecific', _('DeviceSpecific'))
    SiteEntrance = ('SiteEntrance', _('SiteEntrance'))
    GeneralProximity = ('GeneralProximity', _('GeneralProximity'))
    Warehouse = ('Warehouse', _('Warehouse'))

class PlaneAngleItemTypeUnit(models.TextChoices):
    Degree = ('Degree', _('Degree'))
    rad = ('rad', _('Radian'))

class PreferredContactMethodItemTypeEnum(models.TextChoices):
    Email = ('Email', _('Email'))
    WorkPhone = ('WorkPhone', _('WorkPhone'))
    CellPhone = ('CellPhone', _('CellPhone'))
    HomePhone = ('HomePhone', _('HomePhone'))
    CellTextMessage = ('CellTextMessage', _('CellTextMessage'))

class RequirementLevelItemTypeEnum(models.TextChoices):
    Required = ('Required', _('Required'))
    Optional = ('Optional', _('Optional'))
    ConditionallyRequired = ('ConditionallyRequired', _('ConditionallyRequired'))

class ScopeTypeItemTypeEnum(models.TextChoices):
    Project = ('Project', _('Project'))
    PVSystem = ('PVSystem', _('PVSystem'))
    Site = ('Site', _('Site'))
    Device = ('Device', _('Device'))
    Portfolio = ('Portfolio', _('Portfolio'))
    GeoRegion = ('GeoRegion', _('GeoRegion'))
    Task = ('Task', _('Task'))
    Assembly = ('Assembly', _('Assembly'))
    Component = ('Component', _('Component'))

class Entity(models.Model):
    Description_Value = models.CharField(blank=True, max_length=500)
    Email_Value = models.EmailField(blank=True)
    EntityRole_Value = models.CharField(max_length=max(map(len, EntityRoleItemTypeEnum)), choices=EntityRoleItemTypeEnum)
    LegalEntityIdentifier_Value = models.CharField(blank=True, max_length=20)
    TaxID_Value = models.CharField(blank=True, max_length=50)
    URL_Value = models.URLField(blank=True)
    WorkPhone_Value = models.CharField(blank=True, max_length=15)
    Addresses = models.ManyToManyField('Address')
    AlternativeIdentifiers = models.ManyToManyField('AlternativeIdentifier')
    Contacts = models.ManyToManyField('Contact')
    CreditRatings = models.ManyToManyField('CreditRating')
    PaymentMethods = models.ManyToManyField('PaymentMethod')

class Address(models.Model):
    AddrLine1_Value = models.CharField(blank=True, max_length=500)
    AddrLine2_Value = models.CharField(blank=True, max_length=500)
    AddrLine3_Value = models.CharField(blank=True, max_length=500)
    AddressID_Value = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    AddressType_Value = models.CharField(blank=True, max_length=500)
    City_Value = models.CharField(blank=True, max_length=500)
    Country_Value = models.CharField(blank=True, max_length=500)
    County_Value = models.CharField(blank=True, max_length=500)
    Description_Value = models.CharField(blank=True, max_length=500)
    StateProvince_Value = models.CharField(blank=True, max_length=500)
    ZipPostalCode_Value = models.CharField(blank=True, max_length=500)
    Location = models.ForeignKey('Location', on_delete=models.CASCADE)

class AlternativeIdentifier(models.Model):
    Description_Value = models.CharField(blank=True, max_length=500)
    Identifier_Value = models.CharField(blank=True, max_length=500)
    IdentifierType_Value = models.CharField(max_length=max(map(len, IdentifierTypeItemTypeEnum)), choices=IdentifierTypeItemTypeEnum)
    SourceName_Value = models.CharField(blank=True, max_length=500)

class ChecklistTemplate(models.Model):
    ChecklistTemplateID_Value = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    ChecklistTemplateName_Value = models.CharField(blank=True, max_length=500)
    ChecklistTemplateVersion_Value = models.CharField(blank=True, max_length=500)
    Description_Value = models.CharField(blank=True, max_length=500)
    ChecklistTemplateMaintainer = models.ForeignKey('ChecklistTemplateMaintainer', on_delete=models.CASCADE)
    Tags = models.ManyToManyField('Tag')
    Questions = models.ManyToManyField('Question')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'ChecklistTemplateID_Value',
                    'ChecklistTemplateVersion_Value',
                ],
                name='unique_checklist_template_id_version',
            )
        ]

class ChecklistTemplateMaintainer(Entity):
    ChecklistTemplateMaintainerID_Value = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    ChecklistTemplateMaintainerName_Value = models.CharField(blank=True, max_length=500)

class Comment(models.Model):
    CommentDate_Value = models.DateTimeField(blank=True, null=True)
    CommentID_Value = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    CommentText_Value = models.CharField(blank=True, max_length=500)
    Scope = models.ForeignKey('Scope', on_delete=models.CASCADE)
    Tags = models.ManyToManyField('Tag')
    Contacts = models.ManyToManyField('Contact')

class Contact(models.Model):
    ContactID_Value = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    ContactType_Value = models.CharField(max_length=max(map(len, ContactTypeItemTypeEnum)), choices=ContactTypeItemTypeEnum)
    Description_Value = models.CharField(blank=True, max_length=500)
    Email_Value = models.EmailField(blank=True)
    FirstName_Value = models.CharField(blank=True, max_length=500)
    HomePhone_Value = models.CharField(blank=True, max_length=15)
    LastName_Value = models.CharField(blank=True, max_length=500)
    MiddleName_Value = models.CharField(blank=True, max_length=500)
    MobilePhone_Value = models.CharField(blank=True, max_length=15)
    PreferredContactMethod_Value = models.CharField(max_length=max(map(len, PreferredContactMethodItemTypeEnum)), choices=PreferredContactMethodItemTypeEnum)
    Timezone_Value = models.CharField(blank=True, max_length=500)
    Title_Value = models.CharField(blank=True, max_length=500)
    URL_Value = models.URLField(blank=True)
    WorkPhone_Value = models.CharField(blank=True, max_length=15)
    Address = models.ForeignKey('Address', on_delete=models.CASCADE)

class CreditRating(models.Model):
    CreditScore_Value = models.CharField(blank=True, max_length=500)
    CreditScoreSource_Value = models.CharField(blank=True, max_length=500)

class Location(models.Model):
    Altitude_Unit = models.CharField(max_length=max(map(len, LengthItemTypeUnit)), choices=LengthItemTypeUnit)
    Altitude_Value = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    Description_Value = models.CharField(blank=True, max_length=500)
    Elevation_Unit = models.CharField(max_length=max(map(len, LengthItemTypeUnit)), choices=LengthItemTypeUnit)
    Elevation_Value = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    Latitude_Unit = models.CharField(max_length=max(map(len, PlaneAngleItemTypeUnit)), choices=PlaneAngleItemTypeUnit)
    Latitude_Value = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    LocationDeterminationMethod_Value = models.CharField(max_length=max(map(len, LocationDeterminationMethodItemTypeEnum)), choices=LocationDeterminationMethodItemTypeEnum)
    LocationID_Value = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    LocationType_Value = models.CharField(max_length=max(map(len, LocationTypeItemTypeEnum)), choices=LocationTypeItemTypeEnum)
    Longitude_Unit = models.CharField(max_length=max(map(len, PlaneAngleItemTypeUnit)), choices=PlaneAngleItemTypeUnit)
    Longitude_Value = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)

class PaymentMethod(models.Model):
    PaymentMethodName_Value = models.CharField(blank=True, max_length=500)
    PaymentToken_Value = models.CharField(blank=True, max_length=500)
    Tags = models.ManyToManyField('Tag')
    AlternativeIdentifiers = models.ManyToManyField('AlternativeIdentifier')
    Comments = models.ManyToManyField('Comment')

class Question(models.Model):
    AnswerRangeMax_Value = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    AnswerRangeMin_Value = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    AnswerType_Value = models.CharField(max_length=max(map(len, AnswerTypeItemTypeEnum)), choices=AnswerTypeItemTypeEnum)
    DisplaySeqNumber_Value = models.IntegerField(blank=True, null=True)
    QuestionHelp_Value = models.CharField(blank=True, max_length=500)
    QuestionID_Value = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    QuestionLabel_Value = models.CharField(blank=True, max_length=500)
    QuestionUnits_Value = models.CharField(blank=True, max_length=500)
    RequirementLevel_Value = models.CharField(max_length=max(map(len, RequirementLevelItemTypeEnum)), choices=RequirementLevelItemTypeEnum)
    RequirementNotes_Value = models.CharField(blank=True, max_length=500)
    SectionName_Value = models.CharField(blank=True, max_length=500)
    AnswerOptions = models.ManyToManyField('AnswerOption')

class Scope(models.Model):
    Description_Value = models.CharField(blank=True, max_length=500)
    FileFolderURL_Value = models.URLField(blank=True)
    ScopeID_Value = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    ScopeType_Value = models.CharField(max_length=max(map(len, ScopeTypeItemTypeEnum)), choices=ScopeTypeItemTypeEnum)
    Location = models.ForeignKey('Location', on_delete=models.CASCADE)

class AnswerOption(models.Model):
    Value = models.CharField(blank=True, unique=True, max_length=500)

    def __str__(self):
        return self.Value

class Tag(models.Model):
    Value = models.CharField(blank=True, unique=True, max_length=500)

    def __str__(self):
        return self.Value
