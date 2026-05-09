from django.db import models

class Route(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):  

        return f"{self.name} ({self.route.name})"
class Population(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    population = models.IntegerField()

    def __str__(self):
        return f"{self.city.name} - {self.population}"

class Potential(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    education = models.TextField()
    temples = models.TextField()
    tourism = models.TextField()
    industry = models.TextField()

    def __str__(self):
        return f"Potential - {self.city.name}"

class Segmentation(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    urban = models.BooleanField()
    industrial = models.BooleanField()
    pilgrimage = models.BooleanField()
    transit = models.BooleanField()

    def __str__(self):
        return f"Segmentation - {self.city.name}"

class Visitors(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    yearly = models.BigIntegerField()
    daily = models.IntegerField()
    festival = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Visitors - {self.city.name}"

class TopVisitors(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    state = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return f"{self.city.name} → {self.route.name}"

class Distance(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='from_distances')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='to_distances')
    km = models.IntegerField()

    def __str__(self):
        return f"{self.from_city.name} → {self.to_city.name} ({self.km} km)"

class Transport(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    bus = models.IntegerField()
    train = models.IntegerField()
    private = models.IntegerField()

    def __str__(self):
        return f"Transport - {self.route.name}"

class TransportDetail(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='transport_from')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='transport_to')
    mode = models.CharField(max_length=50)
    frequency = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.mode}: {self.from_city.name} → {self.to_city.name}"

class ParcelService(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=200)
    coverage = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.service_name} - {self.route.name}"

class SuggestedRoute(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"Suggestion - {self.route.name}"

class RouteAnalysisCache(models.Model):
    source_city = models.CharField(max_length=100)
    dest_city = models.CharField(max_length=100)
    via_city = models.CharField(max_length=100, blank=True, null=True)
    analysis_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cache: {self.source_city} to {self.dest_city} ({'via ' + self.via_city if self.via_city else 'Direct'})"

class PopularSearch(models.Model):
    route_text = models.CharField(max_length=255, unique=True)
    search_count = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-search_count', '-updated_at']

    def __str__(self):
        return f"{self.route_text} ({self.search_count})"