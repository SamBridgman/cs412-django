from django.db import models

class Voter(models.Model):
    voter_id = models.CharField(max_length=50, primary_key=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=20)
    street_name = models.CharField(max_length=200)
    apartment_number = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50)
    precinct_number = models.CharField(max_length=50)
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    voter_score = models.FloatField(null=True, blank=True)



    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.voter_id})"

def load_data():
    filename = 'newton_voters.csv'
    f = open(filename, 'r')
    f.readline()

    for line in f:
        fields = line.split(',')
        try:
            def str_to_bool(value):
                return value.strip().upper() == 'TRUE'

            voter = Voter(
                voter_id=fields[0],
                last_name=fields[1],
                first_name=fields[2],
                street_number=fields[3],
                street_name=fields[4],
                apartment_number=fields[5],
                zip_code=fields[6],
                date_of_birth=fields[7],
                date_of_registration=fields[8],
                party_affiliation=fields[9],
                precinct_number=fields[10],
                v20state=str_to_bool(fields[11]),
                v21town=str_to_bool(fields[12]),
                v21primary=str_to_bool(fields[13]),
                v22general=str_to_bool(fields[14]),
                v23town=str_to_bool(fields[15]),
                voter_score=float(fields[16]) if fields[16].strip() else None
            )
            voter.save()
            print(f"Loaded voter: {voter.voter_id}")
        except Exception as e:
            print(f"Error loading voter: {e}")
    f.close()