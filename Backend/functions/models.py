from django.db import models


class Route(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.route.name})"


#STEP 1 — Population
class Population(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    population = models.IntegerField()

    def __str__(self):
        return f"{self.city.name} - {self.population}"


# ✅ STEP 2 — Area Potential
class Potential(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    education = models.TextField()
    temples = models.TextField()
    tourism = models.TextField()
    industry = models.TextField()

    def __str__(self):
        return f"Potential - {self.city.name}"


# ✅ STEP 3 — Segmentation
class Segmentation(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    urban = models.BooleanField()
    industrial = models.BooleanField()
    pilgrimage = models.BooleanField()
    transit = models.BooleanField()

    def __str__(self):
        return f"Segmentation - {self.city.name}"


#  STEP 4 — Visitors
class Visitors(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    yearly = models.BigIntegerField()   # upgraded
    daily = models.IntegerField()
    festival = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Visitors - {self.city.name}"


#  Extra — Top Visitors to Route
class TopVisitors(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    state = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return f"{self.city.name} → {self.route.name}"


# ✅ STEP 5 — Distance (Fixed)
class Distance(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='from_distances')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='to_distances')
    km = models.IntegerField()

    def __str__(self):
        return f"{self.from_city.name} → {self.to_city.name} ({self.km} km)"


# ✅ STEP 6 — Transport Pattern
class Transport(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    bus = models.IntegerField()
    train = models.IntegerField()
    private = models.IntegerField()

    def __str__(self):
        return f"Transport - {self.route.name}"


# ✅ STEP 7 — Detailed Transport (Fixed)
class TransportDetail(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='transport_from')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='transport_to')
    mode = models.CharField(max_length=50)  # Bus / Train
    frequency = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.mode}: {self.from_city.name} → {self.to_city.name}"


# ✅ Extra — Parcel Services
class ParcelService(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=200)
    coverage = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.service_name} - {self.route.name}"


# ✅ Final Output — Suggested Route
class SuggestedRoute(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"Suggestion - {self.route.name}"