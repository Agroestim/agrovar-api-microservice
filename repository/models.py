from django.db import models


class CampaignDocumentsModel(models.Model):

    class Meta:
        db_table = "campaign_documents"

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

    LOCATIONS_CHOICES = [
        ("ADELIA MARIA", "Adelia Maria"),
        ("BELL VILLE", "Bell Ville"),
        ("JUSTINIANO POSSE", "Justiniano Posse"),
        ("LA CARLOTA", "La Carlota"),
        ("LABOULAYE", "Laboulaye"),
        ("MARCOZ JUAREZ", "Marcos Juarez"),
        ("ONAGOITY", "Onagoity"),
    ]

    location_origing = models.CharField(
        verbose_name="Localidad de origen",
        max_length=50,
        null=False,
        blank=False,
        default="Seleccionar",
        choices=LOCATIONS_CHOICES,
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

    VARITIES_CHOICES = [
        ("BUCKSY200", "Buck SY 200"),
        ("LENOX", "Lenox"),
        ("ACA360", "ACA 360"),
        ("ACA365", "ACA 365"),
        ("ALGARROBO", "Algarrobo"),
        ("ARSLAK", "Arslak"),
        ("BAGUETTE601", "Baguette 601"),
        ("BASILIO", "Basilio"),
        ("BG620", "Bg 620"),
        ("BG750", "Bg 750"),
        ("BIOINTA2004", "Biointa 2004"),
        ("BIOINTA3005", "Biointa 3005"),
        ("BIOINTA3006", "Biointa 3006"),
        ("CEDRO", "Cedro"),
        ("FLORIPAND", "Floripan 200"),
        ("GUAYABO", "Guayabo"),
        ("MSINTA119", "MS INTA 119"),
        ("ÑANDUBAY", "Ñandubay"),
        ("SURSEM2330", "Sursem 2330"),
    ]

    crop_variety = models.CharField(
        verbose_name="Variedad del cultivo",
        max_length=50,
        blank=False,
        null=False,
        choices=VARITIES_CHOICES,
        default="--Seleccionar--",
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
        return f"{self.id} / {self.reference} - {self.paper_type} - {self.paper_creation_year} - {self.location_origing} - {self.crop_variety}"


class VarietyOptionsModel(models.Model):
    class Meta:
        db_table = "variety_options"

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
