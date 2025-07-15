from django.db import models

class CrossData(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    handedness = models.CharField(max_length=1, choices=[('R', 'Right'), ('L', 'Left'), ('A', 'Ambidextrous')])
    age = models.IntegerField()
    educ = models.IntegerField(null=True, blank=True, help_text="Years of Education")
    ses = models.IntegerField(null=True, blank=True, help_text="Socioeconomic Status")
    mmse = models.FloatField(null=True, blank=True, help_text="Mini-Mental State Examination Score")
    cdr = models.FloatField(null=True, blank=True, help_text="Clinical Dementia Rating")
    etiv = models.FloatField(null=True, blank=True, help_text="Estimated Total Intracranial Volume")
    nwbv = models.FloatField(null=True, blank=True, help_text="Normalized Whole Brain Volume")
    asf = models.FloatField(null=True, blank=True, help_text="Atlas Scaling Factor")
    delay = models.IntegerField()

class LongData(models.Model):
    subject_id = models.CharField(max_length=50)
    mri_id = models.CharField(max_length=50, primary_key=True)
    group = models.CharField(max_length=20, null=True, blank=True)
    visit = models.IntegerField(help_text="Visit number (e.g., 1, 2, 3)")
    delay = models.IntegerField(help_text="Days between MRI scans")
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    handedness = models.CharField(max_length=1, choices=[('R', 'Right'), ('L', 'Left'), ('A', 'Ambidextrous')])
    age = models.IntegerField()
    educ = models.IntegerField(null=True, blank=True, help_text="Years of Education")
    ses = models.IntegerField(null=True, blank=True, help_text="Socioeconomic Status")
    mmse = models.FloatField(null=True, blank=True, help_text="Mini-Mental State Examination Score")
    cdr = models.FloatField(null=True, blank=True, help_text="Clinical Dementia Rating")
    etiv = models.FloatField(null=True, blank=True, help_text="Estimated Total Intracranial Volume")
    nwbv = models.FloatField(null=True, blank=True, help_text="Normalized Whole Brain Volume")
    asf = models.FloatField(null=True, blank=True, help_text="Atlas Scaling Factor")


class MergedData(models.Model):
    """Model storing merged records from cross and longitudinal studies."""
    source_id = models.CharField(max_length=50)
    subject_id = models.CharField(max_length=50, blank=True)
    group = models.CharField(max_length=20, null=True, blank=True)
    visit = models.IntegerField(null=True, blank=True)
    delay = models.IntegerField()
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    handedness = models.CharField(max_length=1, choices=[('R', 'Right'), ('L', 'Left'), ('A', 'Ambidextrous')])
    age = models.IntegerField()
    educ = models.IntegerField(null=True, blank=True)
    ses = models.IntegerField(null=True, blank=True)
    mmse = models.FloatField(null=True, blank=True)
    cdr = models.FloatField(null=True, blank=True)
    etiv = models.FloatField(null=True, blank=True)
    nwbv = models.FloatField(null=True, blank=True)
    asf = models.FloatField(null=True, blank=True)


class RFResult(models.Model):
    """Classification report for the trained model."""
    report = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class YProb(models.Model):
    """Probability predictions for the latest validation run."""
    y_prob = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
