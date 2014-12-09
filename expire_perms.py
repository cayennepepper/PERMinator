#Changes the status of PERMs whose expiration date is in the past to "Expired"

from models import PERM
from datetime import datetime, timedelta
import time
from server import db

while(True):
	perms = db.session.query(PERM).all()
	now = datetime.now()
	for perm in perms:
		if perm.status=="Approved" and perm.expirationTime - now <=timedelta(0):
			#expired
			db.session.query(PERM).filter(PERM.id==perm.id).update({PERM.status:"Expired"})
	db.session.commit()
	time.sleep(86000)