from jobs.models import Sectors

def allSectors(request):
    all_sectors=Sectors.object.all()
    return dict(sectors=all_sectors)