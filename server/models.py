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

class Entity(models.Model):
    Description_Value = models.CharField(max_length=500, blank=True)
    Email_Value = models.CharField(max_length=500, blank=True)
    EntityRole_Value = models.CharField(max_length=max(map(len, EntityRoleItemTypeEnum)), choices=EntityRoleItemTypeEnum)
    LegalEntityIdentifier_Value = models.CharField(max_length=20, blank=True)
    TaxID_Value = models.CharField(max_length=500, blank=True)
    URL_Value = models.CharField(max_length=500, blank=True)
    WorkPhone_Value = models.CharField(max_length=500, blank=True)
    Addresses = models.ManyToManyField('Address')
    AlternativeIdentifiers = models.ManyToManyField('AlternativeIdentifier')
    Contacts = models.ManyToManyField('Contact')
    CreditRatings = models.ManyToManyField('CreditRating')
    PaymentMethods = models.ManyToManyField('PaymentMethod')

class Address(models.Model):
    AddrLine1_Value = models.CharField(max_length=500, blank=True)
    AddrLine2_Value = models.CharField(max_length=500, blank=True)
    AddrLine3_Value = models.CharField(max_length=500, blank=True)
    AddressID_Value = models.CharField(max_length=500, blank=True)
    AddressType_Value = models.CharField(max_length=500, blank=True)
    City_Value = models.CharField(max_length=500, blank=True)
    Country_Value = models.CharField(max_length=500, blank=True)
    County_Value = models.CharField(max_length=500, blank=True)
    Description_Value = models.CharField(max_length=500, blank=True)
    StateProvince_Value = models.CharField(max_length=500, blank=True)
    ZipPostalCode_Value = models.CharField(max_length=500, blank=True)
    Location = models.ForeignKey('Location', on_delete=models.CASCADE)

class AlternativeIdentifier(models.Model):
    Description_Value = models.CharField(max_length=500, blank=True)
    Identifier_Value = models.CharField(max_length=500, blank=True)
    IdentifierType_Value = models.CharField(max_length=500, blank=True)
    SourceName_Value = models.CharField(max_length=500, blank=True)

class ChecklistTemplate(models.Model):
    ChecklistTemplateID_Value = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    ChecklistTemplateName_Value = models.CharField(max_length=500, blank=True)
    ChecklistTemplateVersion_Value = models.CharField(max_length=500, blank=True)
    Description_Value = models.CharField(max_length=500, blank=True)
    ChecklistTemplateMaintainer = models.ForeignKey('ChecklistTemplateMaintainer', on_delete=models.CASCADE)
    Questions = models.ManyToManyField('Question')

class ChecklistTemplateMaintainer(Entity):
    ChecklistTemplateMaintainerID_Value = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    ChecklistTemplateMaintainerName_Value = models.CharField(max_length=500, blank=True)

class Comment(models.Model):
    CommentDate_Value = models.CharField(max_length=500, blank=True)
    CommentID_Value = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    CommentText_Value = models.CharField(max_length=500, blank=True)
    Scope = models.ForeignKey('Scope', on_delete=models.CASCADE)
    Tags = models.ManyToManyField('Tag')
    Contacts = models.ManyToManyField('Contact')

class Contact(models.Model):
    ContactID_Value = models.CharField(max_length=500, blank=True)
    ContactType_Value = models.CharField(max_length=500, blank=True)
    Description_Value = models.CharField(max_length=500, blank=True)
    Email_Value = models.CharField(max_length=500, blank=True)
    FirstName_Value = models.CharField(max_length=500, blank=True)
    HomePhone_Value = models.CharField(max_length=500, blank=True)
    LastName_Value = models.CharField(max_length=500, blank=True)
    MiddleName_Value = models.CharField(max_length=500, blank=True)
    MobilePhone_Value = models.CharField(max_length=500, blank=True)
    PreferredContactMethod_Value = models.CharField(max_length=500, blank=True)
    Timezone_Value = models.CharField(max_length=500, blank=True)
    Title_Value = models.CharField(max_length=500, blank=True)
    URL_Value = models.CharField(max_length=500, blank=True)
    WorkPhone_Value = models.CharField(max_length=500, blank=True)
    Address = models.ForeignKey('Address', on_delete=models.CASCADE)

class CreditRating(models.Model):
    CreditScore_Value = models.CharField(max_length=500, blank=True)
    CreditScoreSource_Value = models.CharField(max_length=500, blank=True)

class Location(models.Model):
    Altitude_Value = models.CharField(max_length=500, blank=True)
    Description_Value = models.CharField(max_length=500, blank=True)
    Elevation_Value = models.CharField(max_length=500, blank=True)
    Latitude_Value = models.CharField(max_length=500, blank=True)
    LocationDeterminationMethod_Value = models.CharField(max_length=500, blank=True)
    LocationID_Value = models.CharField(max_length=500, blank=True)
    LocationType_Value = models.CharField(max_length=500, blank=True)
    Longitude_Value = models.CharField(max_length=500, blank=True)

class PaymentMethod(models.Model):
    PaymentMethodName_Value = models.CharField(max_length=500, blank=True)
    PaymentToken_Value = models.CharField(max_length=500, blank=True)
    Tags = models.ManyToManyField('Tag')
    AlternativeIdentifiers = models.ManyToManyField('AlternativeIdentifier')
    Comments = models.ManyToManyField('Comment')

class Question(models.Model):
    AnswerRangeMax_Value = models.DecimalField(max_digits=3, decimal_places=3, blank=True, null=True)
    AnswerRangeMin_Value = models.DecimalField(max_digits=3, decimal_places=3, blank=True, null=True)
    AnswerType_Value = models.CharField(max_length=max(map(len, AnswerTypeItemTypeEnum)), choices=AnswerTypeItemTypeEnum)
    DisplaySeqNumber_Value = models.IntegerField(blank=True, null=True)
    QuestionID_Value = models.CharField(max_length=500, blank=True)
    QuestionLabel_Value = models.CharField(max_length=500, blank=True)
    QuestionUnits_Value = models.CharField(max_length=500, blank=True)
    RequirementLevel_Value = models.CharField(max_length=500, blank=True)
    RequirementNotes_Value = models.CharField(max_length=500, blank=True)
    SectionName_Value = models.CharField(max_length=500, blank=True)
    AnswerOptions = models.ManyToManyField('AnswerOption')

class Scope(models.Model):
    Description_Value = models.CharField(max_length=500, blank=True)
    FileFolderURL_Value = models.CharField(max_length=500, blank=True)
    ScopeID_Value = models.CharField(max_length=500, blank=True)
    ScopeType_Value = models.CharField(max_length=500, blank=True)
    Location = models.ForeignKey('Location', on_delete=models.CASCADE)

class AnswerOption(models.Model):
    Value = models.CharField(max_length=500, blank=True)

class Tag(models.Model):
    Value = models.CharField(max_length=500, blank=True)
