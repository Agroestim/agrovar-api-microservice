from django.db import models


class VarietyOptionsModel(models.Model):
    class Meta:
        db_table = "variety_options"
        db_table_comment = "This model stores the crop varieties"

    id = models.AutoField(
        verbose_name="Identificado unico",
        primary_key=True,
    )

    tradename = models.CharField(
        verbose_name="Nombre comercial de la variante",
        max_length=25,
        blank=False,
        null=False,
        default="--Tipear--",
    )

    variant_name = models.CharField(
        verbose_name="Nombre especifico de la variante",
        max_length=25,
        default="--Tipear--",
    )

    def __str__(self) -> str:
        return f"{self.id} / {self.tradename} - {self.variant_name}"


class LocationOptionsModel(models.Model):
    class Meta:
        db_table = "location_options"
        db_table_comment = "This model stores the campaing locations"

    id = models.AutoField(
        verbose_name="Identificador unico",
        primary_key=True,
    )

    region_name = models.CharField(
        verbose_name="Nombre de la region",
        max_length=50,
        blank=False,
        null=False,
    )

    def __str__(self) -> str:
        return f"{self.id} / {self.region_name}"


class CampaignDocumentsModel(models.Model):

    class Meta:
        db_table = "campaign_documents"
        db_table_comment = "This model stores the capaign documents"

    id = models.AutoField(
        verbose_name="Identificador Unico",
        primary_key=True,
    )

    REFERENCES_CHOICES = [
        ("RED INTA 2022", "Red INTA 2022"),
        ("INTA LABOULAYE", "INTA Laboulaye"),
    ]

    reference = models.CharField(
        verbose_name="Org. de Referencia",
        max_length=50,
        null=False,
        blank=False,
        choices=REFERENCES_CHOICES,
        default="Seleccionar",
    )

    PAPER_TYPE_CHOICES = [
        ("VARIEDADES", "Variedades"),
    ]

    paper_type = models.CharField(
        verbose_name="Tipo de ensayo",
        max_length=50,
        null=False,
        blank=False,
        choices=PAPER_TYPE_CHOICES,
        default="Seleccionar",
    )

    paper_creation_year = models.DateField(
        verbose_name="Año de registro",
        auto_now=False,
    )

    location_origin = models.ForeignKey(
        to=LocationOptionsModel,
        on_delete=models.CASCADE,
        related_name="location_origin",
        verbose_name="Localidad de origen",
    )

    latitude = models.DecimalField(
        verbose_name="Coordenada de Latitud",
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=False,
    )

    longitude = models.DecimalField(
        verbose_name="Coordenada de Longitud",
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=False,
    )

    paper_repetition = models.IntegerField(
        verbose_name="Repeticiones del ensayo",
        blank=False,
        null=False,
        default=1,
    )

    crop_variety = models.ForeignKey(
        to=VarietyOptionsModel,
        on_delete=models.CASCADE,
        related_name="crop_variety",
        verbose_name="Variedad del cultivo",
    )

    humidity_percentage_stat = models.DecimalField(
        verbose_name="Porcentaje de humedad (%)",
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=False,
    )

    performance_stat = models.DecimalField(
        verbose_name="Rendimiento (Kg/Ha)",
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=False,
    )

    relative_performance_stat = models.DecimalField(
        verbose_name="Rendimiento relativo (kg/ha)",
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=False,
    )

    grain_count_crop_stat = models.IntegerField(
        verbose_name="Conteo de granos por cultivo",
        blank=False,
        null=False,
    )

    grain_count_per_spike_stat = models.IntegerField(
        verbose_name="Conteo de granos por espiga",
        blank=False,
        null=False,
    )

    weight_per_thousand_grains_stat = models.DecimalField(
        verbose_name="Peso por mil granos (g)",
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=False,
    )

    proteins_percentage_stat = models.DecimalField(
        verbose_name="Porcentaje de proteinas (%)",
        max_digits=4,
        decimal_places=2,
        blank=False,
        null=False,
    )

    ph_stat = models.DecimalField(
        verbose_name="Potencial de hidrogeno (ph)",
        max_digits=4,
        decimal_places=2,
        blank=False,
        null=False,
    )

    def __str__(self) -> str:
        return f"{self.id} / {self.paper_type} / {self.reference} - {self.location_origin.region_name} - {self.paper_creation_year} / {self.crop_variety.variant_name}"
