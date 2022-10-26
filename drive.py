from deta import Deta
from settings import PROJECT_KEY

deta = Deta(PROJECT_KEY)
drive_pengungsian = deta.Drive("drive_pengungsian")

